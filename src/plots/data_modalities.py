import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches

def create_data_modalities_figure():
    """
    Generates a 2x2 figure showing four simulated data modalities
    for marine biomass analysis.
    """
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.labelweight'] = 'bold'
    plt.rcParams['axes.titlesize'] = 12
    plt.rcParams['axes.labelsize'] = 10
    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10
    plt.rcParams['legend.fontsize'] = 10

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('Fig. 2. Examples of data modalities used in ML-based biomass analysis.', 
                 y=0.98, fontweight='bold')

    # --- (a) Acoustic Echogram ---
    ax = axes[0, 0]
    # Create synthetic echogram data
    np.random.seed(42)
    echogram_data = np.random.rand(100, 200) * 0.2  # Background noise
    # Add a "seabed"
    echogram_data[80:, :] += 0.8
    # Add a "fish school"
    x_school, y_school = 120, 45
    y, x = np.ogrid[-y_school:100 - y_school, -x_school:200 - x_school]
    school = 0.7 * np.exp(-(x * x + y * y) / (2 * 8**2))
    echogram_data += school
    
    im = ax.imshow(echogram_data, aspect='auto', cmap='viridis', vmin=0, vmax=1)
    ax.set_title('(a) Acoustic Data (Echogram)', fontweight='bold')
    ax.set_xlabel('Ping Number (Time)')
    ax.set_ylabel('Depth (m)')
    cbar = fig.colorbar(im, ax=ax, orientation='vertical', fraction=0.046, pad=0.04)
    cbar.set_label('Signal Strength (dB)', fontweight='bold')
    ax.set_xticks([])
    ax.set_yticks([])


    # --- (b) Remote Sensing Data ---
    ax = axes[0, 1]
    # Create synthetic satellite data
    x = np.linspace(-5, 5, 200)
    y = np.linspace(-5, 5, 200)
    xx, yy = np.meshgrid(x, y)
    # Create a "bloom" with swirl patterns
    bloom_data = np.sin(xx) * np.cos(yy) * 0.5 + 0.5
    # Add a "coastline"
    bloom_data[:80, :60] = -0.5  # Land
    
    im = ax.imshow(bloom_data, cmap='GnBu_r', origin='lower')
    ax.set_title('(b) Remote Sensing Data (Chlorophyll-a)', fontweight='bold')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    cbar = fig.colorbar(im, ax=ax, orientation='vertical', fraction=0.046, pad=0.04)
    cbar.set_label('Chlorophyll-a (mg/m³)', fontweight='bold')
    ax.set_xticks([])
    ax.set_yticks([])


    # --- (c) In-situ Optical Data (with ML Detection) ---
    ax = axes[1, 0]
    ax.set_facecolor('#E6F3F7') # Light blue-green water
    
    # Simulate fish (ellipses)
    fish1 = patches.Ellipse((0.3, 0.6), 0.25, 0.1, angle=20, color='#708090', alpha=0.8) # SlateGray
    fish2 = patches.Ellipse((0.7, 0.3), 0.3, 0.12, angle=-30, color='#2F4F4F', alpha=0.8) # DarkSlateGray
    ax.add_patch(fish1)
    ax.add_patch(fish2)
    
    # Simulate ML bounding boxes
    bbox1 = patches.Rectangle((0.15, 0.5), 0.3, 0.2, linewidth=2, 
                              edgecolor='#C44E52', facecolor='none', linestyle='-')
    bbox2 = patches.Rectangle((0.5, 0.18), 0.4, 0.25, linewidth=2, 
                              edgecolor='#C44E52', facecolor='none', linestyle='-')
    ax.add_patch(bbox1)
    ax.add_patch(bbox2)
    ax.text(0.15, 0.72, 'fish (98%)', color='#C44E52', fontweight='bold')
    ax.text(0.5, 0.45, 'fish (95%)', color='#C44E52', fontweight='bold')
    
    ax.set_title('(c) In-situ Optical Data (ML Detection)', fontweight='bold')
    ax.set_xlabel('x-pixel')
    ax.set_ylabel('y-pixel')
    ax.set_xticks([])
    ax.set_yticks([])


    # --- (d) Mass Spectrometry Data ---
    ax = axes[1, 1]
    # Create synthetic spectral data
    x = np.linspace(200, 800, 1000)
    y = np.random.rand(1000) * 0.05 # Baseline noise
    
    # Add characteristic peaks
    peaks_x = [250, 310, 450, 620, 780]
    peaks_h = [0.8, 0.6, 1.0, 0.4, 0.7]
    peaks_w = [2, 1.5, 3, 2, 2.5]
    for (px, ph, pw) in zip(peaks_x, peaks_h, peaks_w):
        y += ph * np.exp(-(x - px)**2 / (2 * pw**2))
        
    ax.plot(x, y, color='#4C72B0', linewidth=1.5)
    ax.set_title('(d) Mass Spectrometry Data (Spectrum)', fontweight='bold')
    ax.set_xlabel('Mass/Charge (m/z)')
    ax.set_ylabel('Relative Intensity')
    ax.set_ylim(0, 1.2)
    ax.set_yticks([0, 0.5, 1.0])
    ax.grid(True, linestyle='--', alpha=0.4)

    # --- Final Touches ---
    plt.tight_layout(rect=[0, 0.03, 1, 0.95]) # Adjust layout for suptitle
    plt.savefig("figures/data_modalities_figure.pdf", dpi=300, bbox_inches='tight')
    # plt.show()

# Run the function to generate the plot
create_data_modalities_figure()