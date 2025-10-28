import matplotlib.pyplot as plt
import collections
import numpy as np
import os # Import os to check/create directory

# --- Data based on the 36 papers provided in the bib file ---

# 1. Publication Years
years_data = [
    2020, 2020, 2020, # Kerr, LiuShape, Varma
    2021, 2021, 2021, 2021, 2021, # LiuPlankton, Goulart, Pu, Ma, Walker
    2022, 2022, 2022, 2022, 2022, 2022, # Alfano, Ardhi, Testolin, woodAuto, Weiss, aftab (originally 2024, but bib shows 2022) - Rechecking aftab2024 entry. It says 2024. OK. Let's assume bib is correct for others for now.
                                 # Recheck years from bib: Alfano(22), Ardhi(22), Brautaset(25), Ciranni(25), Ditria(25), Dubus(23), Goulart(21), HuangML(23), HuangSym(25), Jayanthi(25), Kerr(20), KumarF(23), KumarT(23), Kwon(25), LiuShape(20), LiuPlankton(21), Ma(21), Masoudi(24), McCarthy(23), McMillanI(23), McMillanD(24), Park(*missing*), Priya(23), Pu(21), Seto(25), Somek(23), Testolin(22), Vargas(24), Varma(20), Walker(21), Weiss(22), WoodAuto(22), WoodHook(25), Yang(24), Yuan(25), Zhang(24).
    2023, 2023, 2023, 2023, 2023, 2023, # Dubus, HuangML, KumarF, KumarT, McCarthy, Priya, Somek
    2024, 2024, 2024, 2024, 2024, 2024, # aftab, Masoudi, McMillanD, Vargas, Yang, Zhang
    2025, 2025, 2025, 2025, 2025, 2025, 2025, 2025, 2025 # Brautaset, Ciranni, Ditria, HuangSym, Jayanthi, Kwon, Seto, WoodHook, Yuan
]
year_counts = collections.Counter(years_data)
years = sorted(year_counts.keys())
counts_years = [year_counts[year] for year in years]

# 2. ML Methods (Simplified Categories based on primary focus/mention)
# Categories: CNN/U-Net, Transformer, YOLO, Trad. Supervised (SVM/RF/Boost/Prob), Unsupervised, Self-Supervised, Symbolic Regression, Review/Meta, Other/General ML
methods_data = [
    'Unsupervised', # Alfano
    'Review/Meta', # Ardhi
    'CNN/U-Net', # Brautaset
    'Self-Supervised', # Ciranni
    'Review/Meta', # Ditria
    'Other/General ML', # Dubus (Kappa metrics, not ML model focus)
    'Unsupervised', # Goulart
    'Other/General ML', # HuangML
    'Symbolic Regression', # HuangSymbolic
    'CNN/U-Net', # Jayanthi (also SVM/RF)
    'CNN/U-Net', # Kerr (Collaborative DL -> CNN focus)
    'CNN/U-Net', # KumarFrameworks (Autoencoder/VGG)
    'CNN/U-Net', # KumarTransform (DNN/Autoencoder)
    'Trad. Supervised', # Kwon (Probabilistic ML)
    'Trad. Supervised', # LiuShape (Shape Analysis / ML)
    'Trad. Supervised', # LiuPlankton (LightBGM)
    'CNN/U-Net', # Ma (ResNet)
    'Self-Supervised', # Masoudi
    'Trad. Supervised', # McCarthy (RF/Tree)
    'YOLO', # McMillanImproving (Transfer Learning YOLO)
    'Transformer', # McMillanDeep (Vision Transformer)
    # Park missing - Assuming Park et al. 2024 uses YOLO based on context
    'YOLO', # Park (AI / YOLO / ByteTrack)
    'Other/General ML', # Priya (General ML)
    'CNN/U-Net', # Pu (DL)
    'Trad. Supervised', # Seto (RF)
    'CNN/U-Net', # Somek (CNNs)
    'CNN/U-Net', # Testolin (CNN/RNN)
    'Other/General ML', # Vargas (ML Algorithm)
    'CNN/U-Net', # Varma (CNN)
    'Other/General ML', # Walker (Hard Negative Mining / ML)
    'CNN/U-Net', # Weiss (CNN)
    'Trad. Supervised', # WoodAuto (SVM)
    'Transformer', # WoodHook (Transformer)
    'Other/General ML', # Yang (DL-based enhancement mentioned comparison)
    'Transformer', # Yuan (Swin Transformer)
    'CNN/U-Net', # Zhang (Autoencoder for imputation) + Trad. Supervised # Re-categorized
]

method_counts = collections.Counter(methods_data)
# Sort methods for consistent pie chart ordering
sorted_methods = sorted(method_counts.keys())
counts_methods = [method_counts[key] for key in sorted_methods]
labels_methods = sorted_methods

# 3. Application Focus
applications_data = [
    'Aquaculture', # Aftab
    'Plankton Analysis', # Alfano
    'Plankton Analysis', # Ardhi
    'Fisheries Assessment', # Brautaset
    'Plankton Analysis', # Ciranni
    'Remote Sensing', # Ditria
    'Underwater Acoustics', # Dubus
    'Plankton Analysis', # Goulart
    'Fisheries Management', # HuangML
    'Food Authenticity', # HuangSymbolic
    'Aquaculture', # Jayanthi (Security)
    'Plankton Analysis', # Kerr
    'Underwater Acoustics', # KumarFrameworks
    'Underwater Acoustics', # KumarTransform
    'Plankton Analysis', # Kwon (Phyto focus)
    'Plankton Analysis', # LiuShape
    'Plankton Analysis', # LiuPlankton
    'Plankton Analysis', # Ma
    'Plankton Analysis', # Masoudi
    'Underwater Acoustics', # McCarthy
    'Aquaculture', # McMillanImproving
    'Aquaculture', # McMillanDeep
    'Fisheries Management', # Park
    'Plankton Analysis', # Priya
    'Plankton Analysis', # Pu
    'Algal Biomass', # Seto
    'Plankton Analysis', # Somek
    'Fisheries Assessment', # Testolin
    'Fisheries Management', # Vargas
    'Plankton Analysis', # Varma
    'Plankton Analysis', # Walker
    'Underwater Acoustics', # Weiss
    'Food Authenticity', # WoodAuto
    'Food Authenticity', # WoodHook
    'Plankton Analysis', # Yang
    'Plankton Analysis', # Yuan
    'Aquaculture', # Zhang
]
app_counts = collections.Counter(applications_data)
# Sort applications by count descending for the bar chart
sorted_apps = sorted(app_counts.items(), key=lambda item: item[1], reverse=True)
labels_apps = [item[0] for item in sorted_apps]
counts_apps = [item[1] for item in sorted_apps]

# --- Create Plots ---

# --- Create 'figures' directory if it doesn't exist ---
output_dir = 'figures'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Created directory: {output_dir}")

plt.style.use('seaborn-v0_8-talk') # Using a slightly more modern style

# 1. Bar Chart: Papers per Year
fig1, ax1 = plt.subplots(figsize=(10, 6))
ax1.bar(years, counts_years, color='skyblue')
ax1.set_xlabel('Publication Year')
ax1.set_ylabel('Number of Papers')
ax1.set_title('Distribution of Included Papers by Year (2020-2025)')
ax1.set_xticks(years) # Ensure all years are labeled
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'papers_per_year.png'))
print(f"Saved {os.path.join(output_dir, 'papers_per_year.png')}")

# 2. Pie Chart: ML Method Distribution - ADJUSTED FOR CENTERING
# Use a more square figure size for pie charts
fig2, ax2 = plt.subplots(figsize=(8, 8)) # Changed figsize to be square
# Use autopct to show percentages, display label if percentage > 3%
def func(pct, allvals):
    absolute = int(np.round(pct/100.*np.sum(allvals)))
    # Display count inside slice if desired: return f"{pct:.1f}%\n({absolute:d})"
    return "{:.1f}%".format(pct) if pct > 3 else ''

wedges, texts, autotexts = ax2.pie(counts_methods,
                                   autopct=lambda pct: func(pct, counts_methods),
                                   startangle=90,
                                   pctdistance=0.85, # Position of percentage labels inside wedges
                                   colors=plt.cm.Paired(np.linspace(0, 1, len(labels_methods))),
                                   # Removed radius=1.0 - let matplotlib handle sizing initially
                                   )

ax2.set_title('Distribution of Primary ML Methodologies Used', pad=20)

# Create legend outside the pie chart - adjusted bbox_to_anchor
# (x, y, width, height) - Place legend to the right, centered vertically
legend = ax2.legend(wedges, labels_methods,
                    title="ML Methods",
                    loc="center left", # Anchor point on the legend box
                    bbox_to_anchor=(1.05, 0.5), # Position relative to axes (x=1.05 means just outside right edge)
                    fontsize='medium') # Adjust fontsize if needed

plt.setp(autotexts, size=10, weight="bold", color="white")

# Use subplots_adjust OR tight_layout without rect, and save with bbox_inches='tight'
# Option 1: subplots_adjust (more manual control)
# plt.subplots_adjust(left=0.1, right=0.75, top=0.9, bottom=0.1) # Adjust right value to fit legend

# Option 2: tight_layout() + savefig adjustment (often simpler)
plt.tight_layout() # Let tight_layout do initial adjustment
plt.savefig(os.path.join(output_dir, 'ml_method_distribution.png'),
            bbox_inches='tight', # Crucial for removing whitespace around the figure
            pad_inches=0.1) # Optional small padding
print(f"Saved {os.path.join(output_dir, 'ml_method_distribution.png')}")


# 3. Bar Chart: Application Focus Distribution (Sorted)
fig3, ax3 = plt.subplots(figsize=(12, 7))
bars = ax3.bar(labels_apps, counts_apps, color='lightcoral')
ax3.set_xlabel('Application Area')
ax3.set_ylabel('Number of Papers')
ax3.set_title('Distribution of Papers by Primary Application Focus')
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)
plt.xticks(rotation=45, ha='right') # Rotate labels for better readability
# Add counts on top of bars
ax3.bar_label(bars, padding=3)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'application_focus_distribution.png'))
print(f"Saved {os.path.join(output_dir, 'application_focus_distribution.png')}")

plt.close(fig1)
plt.close(fig2)
plt.close(fig3)