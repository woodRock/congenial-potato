import matplotlib.pyplot as plt
import collections
import numpy as np
import pandas as pd # Import pandas for crosstab
import seaborn as sns # Import seaborn for heatmap
import os

# --- Data based on the 37 papers (including Park et al. placeholder) ---
# --- ENSURING BOTH LISTS HAVE EXACTLY 37 ITEMS, ALIGNED ---

# ML Methods (Simplified Categories) - Should have 37 entries
methods_data = [
    'CNN/U-Net',        # Aftab
    'Unsupervised',     # Alfano
    'Review/Meta',      # Ardhi
    'CNN/U-Net',        # Brautaset
    'Self-Supervised',  # Ciranni
    'Review/Meta',      # Ditria
    'Other/General ML', # Dubus
    'Unsupervised',     # Goulart
    'Other/General ML', # HuangML  <-- Corrected entry added in correct position
    'Symbolic Regression',# HuangSymbolic
    'CNN/U-Net',        # Jayanthi
    'CNN/U-Net',        # Kerr
    'CNN/U-Net',        # KumarFrameworks
    'CNN/U-Net',        # KumarTransform
    'Trad. Supervised', # Kwon
    'Trad. Supervised', # LiuShape
    'Trad. Supervised', # LiuPlankton
    'CNN/U-Net',        # Ma
    'Self-Supervised',  # Masoudi
    'Trad. Supervised', # McCarthy
    'YOLO',             # McMillanImproving
    'Transformer',      # McMillanDeep
    'YOLO',             # Park
    'Other/General ML', # Priya
    'CNN/U-Net',        # Pu
    'Trad. Supervised', # Seto
    'CNN/U-Net',        # Somek
    'CNN/U-Net',        # Testolin
    'Other/General ML', # Vargas
    'CNN/U-Net',        # Varma
    'Other/General ML', # Walker
    'CNN/U-Net',        # Weiss
    'Trad. Supervised', # WoodAuto
    'Transformer',      # WoodHook
    'Other/General ML', # Yang
    'Transformer',      # Yuan
    'CNN/U-Net'         # Zhang (Re-categorized Autoencoder as NN type)
]

# Application Focus (Should have 37 entries)
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

# --- Verify data alignment ---
print(f"Length of methods_data: {len(methods_data)}")
print(f"Length of applications_data: {len(applications_data)}")
if len(methods_data) != len(applications_data):
    # Added f-string for clearer error message
    raise ValueError(f"CRITICAL ERROR: Mismatch in length between methods_data ({len(methods_data)}) and applications_data ({len(applications_data)})")
else:
    print(f"Data lists correctly aligned with {len(methods_data)} entries each.")

# --- Create DataFrame and Cross-Tabulation ---
df = pd.DataFrame({'Method': methods_data, 'Application': applications_data})
cross_tab = pd.crosstab(df['Application'], df['Method'])

# --- Reorder columns/rows for better visualization (optional) ---
# Order methods roughly by complexity/type
method_order = [
    'Review/Meta',
    'Trad. Supervised',
    'Symbolic Regression',
    'Unsupervised',
    'Self-Supervised',
    'CNN/U-Net',
    'YOLO',
    'Transformer',
    'Other/General ML'
]
# Order applications by frequency (as determined earlier) or logically
app_order = [
    'Plankton Analysis',
    'Aquaculture',
    'Underwater Acoustics',
    'Fisheries Management',
    'Food Authenticity',
    'Fisheries Assessment',
    'Remote Sensing',
    'Algal Biomass',
]

# Ensure all categories are present and reindex
cross_tab = cross_tab.reindex(index=app_order, columns=method_order, fill_value=0)

# --- Create Heatmap ---
plt.style.use('seaborn-v0_8-talk')
fig, ax = plt.subplots(figsize=(12, 9)) # Adjust figsize as needed

sns.heatmap(cross_tab,
            annot=True,       # Show counts in cells
            fmt="d",          # Format counts as integers
            cmap="Blues",     # Choose a colormap (e.g., 'Blues', 'Greens', 'YlGnBu')
            linewidths=.5,    # Add lines between cells
            cbar=True,        # Show the color bar
            ax=ax)

ax.set_title('Frequency of ML Methodologies Applied Across Application Areas', pad=20)
ax.set_xlabel('Machine Learning Methodology')
ax.set_ylabel('Application Area')
plt.xticks(rotation=45, ha='right') # Rotate x-axis labels if needed
plt.yticks(rotation=0) # Ensure y-axis labels are horizontal

# --- Save Figure ---
output_dir = 'figures'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Created directory: {output_dir}")

plt.tight_layout()
# Save with bbox_inches='tight' to minimize whitespace
plt.savefig(os.path.join(output_dir, 'methodology_vs_application_heatmap.png'), bbox_inches='tight')
print(f"Saved {os.path.join(output_dir, 'methodology_vs_application_heatmap.png')}")

plt.close(fig) # Close the figure to free memory