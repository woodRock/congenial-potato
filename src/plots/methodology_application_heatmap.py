import matplotlib.pyplot as plt
import collections
import numpy as np
import pandas as pd # Import pandas for crosstab
import seaborn as sns # Import seaborn for heatmap
import os

# --- Data based on the 44 papers provided in the bib file ---

# ML Methods (Simplified Categories) - Should have 44 entries
methods_data = [
    'CNN/U-Net', 'Unsupervised', 'Review/Meta', 'CNN/U-Net', 'Self-Supervised', 'Review/Meta', 'Other/General ML', 'Unsupervised', 'Other/General ML', 'Symbolic Regression', 'CNN/U-Net', 'CNN/U-Net', 'CNN/U-Net', 'CNN/U-Net', 'Trad. Supervised', 'Trad. Supervised', 'Trad. Supervised', 'Trad. Supervised', 'CNN/U-Net', 'Self-Supervised', 'Trad. Supervised', 'YOLO', 'Transformer', 'YOLO', 'Other/General ML', 'CNN/U-Net', 'Trad. Supervised', 'CNN/U-Net', 'CNN/U-Net', 'Other/General ML', 'CNN/U-Net', 'Other/General ML', 'CNN/U-Net', 'Trad. Supervised', 'Transformer', 'Other/General ML', 'Other/General ML', 'Transformer', 'CNN/U-Net', 'Trad. Supervised', 'Trad. Supervised', 'Review/Meta', 'Trad. Supervised', 'Trad. Supervised'
]

# Application Focus (Should have 44 entries)
applications_data = [
    'Aquaculture', 'Plankton Analysis', 'Plankton Analysis', 'Fisheries Assessment', 'Plankton Analysis', 'Remote Sensing', 'Underwater Acoustics', 'Plankton Analysis', 'Fisheries Management', 'Food Authenticity', 'Aquaculture', 'Plankton Analysis', 'Underwater Acoustics', 'Underwater Acoustics', 'Plankton Analysis', 'Plankton Analysis', 'Plankton Analysis', 'Food Authenticity', 'Plankton Analysis', 'Plankton Analysis', 'Underwater Acoustics', 'Aquaculture', 'Aquaculture', 'Fisheries Management', 'Plankton Analysis', 'Plankton Analysis', 'Algal Biomass', 'Plankton Analysis', 'Fisheries Assessment', 'Fisheries Management', 'Plankton Analysis', 'Plankton Analysis', 'Underwater Acoustics', 'Food Authenticity', 'Food Authenticity', 'Plankton Analysis', 'Food Authenticity', 'Plankton Analysis', 'Aquaculture', 'Food Authenticity', 'Food Authenticity', 'Food Authenticity', 'Food Authenticity', 'Food Authenticity'
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