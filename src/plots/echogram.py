"""
Generate a publication-quality echogram from a Simrad EK60/EK80 .raw file.

Usage
-----
Replace RAW_FILE below with your local path to a CRIMAC sandeel survey .raw file
obtained from the Norwegian Marine Data Centre (nmdc.no, search "sandeel acoustic").

If you don't yet have the CRIMAC file, the script falls back to downloading a small
open-access EK60 file from the NOAA Water-Column Sonar Data archive to verify
everything works (same .raw format, same code path).
"""

import os
import pathlib
import urllib.request
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import echopype as ep

# ---------------------------------------------------------------------------
# Configuration — set this to your local .raw path when you have CRIMAC data
# ---------------------------------------------------------------------------
RAW_FILE = None   # e.g. "/path/to/S2019847_0511.raw"

FREQUENCY_KHZ = 38          # 38 kHz is the standard sandeel survey frequency
DEPTH_MIN_M   = 0
DEPTH_MAX_M   = 200         # sandeel live in the upper ~150 m
SV_MIN_DB     = -80         # colour scale floor (dB re 1 m⁻¹)
SV_MAX_DB     = -34         # colour scale ceiling

OUTPUT_DIR = pathlib.Path("figures")
OUTPUT_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# Fallback: small open-access EK60 file from NOAA NCEI WCSD archive
# (Pacific hake survey, same EK60 .raw format as CRIMAC)
# ---------------------------------------------------------------------------
FALLBACK_URL = (
    "https://ncei-wcsd-archive.s3.amazonaws.com/data/raw/"
    "Bell_M._Shimada/SH1707/EK60/Summer2017-D20170728-T181619.raw"
)
FALLBACK_PATH = OUTPUT_DIR / "demo_EK60.raw"

def ensure_raw_file() -> pathlib.Path:
    if RAW_FILE and pathlib.Path(RAW_FILE).exists():
        return pathlib.Path(RAW_FILE)
    print("RAW_FILE not set or not found — downloading NOAA demo file …")
    if not FALLBACK_PATH.exists():
        urllib.request.urlretrieve(FALLBACK_URL, FALLBACK_PATH)
        print(f"  saved {FALLBACK_PATH}")
    else:
        print(f"  using cached {FALLBACK_PATH}")
    return FALLBACK_PATH

# ---------------------------------------------------------------------------
# Parse → calibrate → Sv
# ---------------------------------------------------------------------------
raw_path = ensure_raw_file()
is_crimac = RAW_FILE is not None

print(f"Opening {raw_path} …")
ed = ep.open_raw(str(raw_path), sonar_model="EK60")

print("Calibrating to volume backscatter strength (Sv) …")
ds_Sv = ep.calibrate.compute_Sv(ed)

# Pick the channel closest to the target frequency
freq_labels = ds_Sv.channel.values          # e.g. "GPT 38 kHz ..."
target_hz   = FREQUENCY_KHZ * 1000
freq_values = np.array([
    float(str(lbl).split()[1]) * 1000       # parse "GPT 38 kHz …" → 38000
    for lbl in freq_labels
])
chan_idx  = int(np.argmin(np.abs(freq_values - target_hz)))
chan_name = str(freq_labels[chan_idx])
print(f"  using channel: {chan_name}")

# Extract Sv array: dims are (channel, ping_time, range_sample)
sv_da = ds_Sv["Sv"].isel(channel=chan_idx)          # (ping_time, range_sample)

# echo_range is (ping_time, range_sample); average across pings for a stable depth axis
range_m = ds_Sv["echo_range"].isel(channel=chan_idx).mean(dim="ping_time").values

# Trim depth range using the 1-D mean range
depth_mask = (range_m >= DEPTH_MIN_M) & (range_m <= DEPTH_MAX_M)
sv_2d    = sv_da.values[:, depth_mask].T          # shape (depth, ping)
range_2d = range_m[depth_mask]
times    = sv_da.ping_time.values.astype("datetime64[s]").astype(float)  # seconds

# ---------------------------------------------------------------------------
# Plot
# ---------------------------------------------------------------------------
plt.style.use("seaborn-v0_8-white")
plt.rcParams["font.family"] = "serif"

fig, ax = plt.subplots(figsize=(10, 5))

cmap = plt.colormaps["viridis_r"].copy()
cmap.set_bad(color="white")

sv_masked = np.ma.masked_where(~np.isfinite(sv_2d), sv_2d)

mesh = ax.pcolormesh(
    times,
    range_2d,
    sv_masked,
    cmap=cmap,
    vmin=SV_MIN_DB,
    vmax=SV_MAX_DB,
    shading="auto",
    rasterized=True,
)

# Colourbar
cbar = fig.colorbar(mesh, ax=ax, pad=0.01, fraction=0.03)
cbar.set_label(r"$S_v$ (dB re 1 m$^{-1}$)", fontsize=12)
cbar.ax.tick_params(labelsize=11)

# Axes decoration
ax.set_ylim(DEPTH_MAX_M, DEPTH_MIN_M)          # depth increases downward
ax.set_ylabel("Depth (m)", fontsize=13, fontweight="bold")
ax.set_xlabel("Ping time (s, UTC)", fontsize=13, fontweight="bold")
ax.tick_params(labelsize=12)

title = (
    f"Echogram — {FREQUENCY_KHZ} kHz"
    + (" (CRIMAC sandeel survey)" if is_crimac else " (NOAA SH1707 demo)")
)
ax.set_title(title, fontsize=14, fontweight="bold", pad=12)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()

out_pdf = OUTPUT_DIR / "echogram.pdf"
out_png = OUTPUT_DIR / "echogram.png"
fig.savefig(out_pdf, dpi=300, bbox_inches="tight")
fig.savefig(out_png, dpi=300, bbox_inches="tight")
plt.close(fig)
print(f"Saved {out_pdf} and {out_png}")
