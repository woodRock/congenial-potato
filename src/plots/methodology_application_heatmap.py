import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import os

import json

# --- Read the categorized papers ---
with open('/Users/woodj/Desktop/congenial-potato/src/categorized_papers.json', 'r') as f:
    categorized_papers = json.load(f)

methods_data = [paper['methodology_category'] for paper in categorized_papers]
applications_data = [paper['application_category'] for paper in categorized_papers]

# --- Verify data alignment ---
print(f"Length of methods_data: {len(methods_data)}")
print(f"Length of applications_data: {len(applications_data)}")
if len(methods_data) != len(applications_data):
    raise ValueError(f"CRITICAL ERROR: Mismatch in length between methods_data ({len(methods_data)}) and applications_data ({len(applications_data)})")
else:
    print(f"Data lists correctly aligned with {len(methods_data)} entries each.")

# --- Create DataFrame and Cross-Tabulation ---
df = pd.DataFrame({'Method': methods_data, 'Application': applications_data})
cross_tab = pd.crosstab(df['Application'], df['Method'])

# --- Reorder columns/rows for better visualization (optional) ---
method_order = [
    'Traditional supervised',
    'Deep learning - CNN & Variants',
    'Deep learning - transformers',
    'Unsupervised and self-supervised',
    'Evolutionary computation',
    'Other'
]
app_order = [
    'Fisheries management & stock assessment',
    'Aquaculture & automated monitoring',
    'Plankton & phytoplankton analysis',
    'Molecular level analysis & food science',
    'Other'
]

# Ensure all categories are present and reindex
cross_tab = cross_tab.reindex(index=app_order, columns=method_order, fill_value=0)

# --- Create Heatmap ---
plt.style.use('seaborn-v0_8-white')
plt.rcParams['font.family'] = 'serif'
plt.rcParams['axes.labelweight'] = 'bold'
fig, ax = plt.subplots(figsize=(12, 9))

# Use a professional colormap
sns.heatmap(cross_tab,
            annot=True,
            fmt="d",
            cmap="YlGnBu",
            linewidths=.8,
            cbar_kws={'label': 'Number of Papers'},
            ax=ax)

ax.set_title('Frequency of ML Methodologies Across Application Areas', pad=25, fontsize=14, fontweight='bold')
ax.set_xlabel('Machine Learning Methodology', fontsize=12, labelpad=10)
ax.set_ylabel('Application Area', fontsize=12, labelpad=10)
plt.xticks(rotation=35, ha='right', fontsize=10)
plt.yticks(rotation=0, fontsize=10)

# --- Save Figure ---
output_dir = 'figures'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Created directory: {output_dir}")

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'methodology_vs_application_heatmap.pdf'), dpi=300, bbox_inches='tight')
print(f"Saved {os.path.join(output_dir, 'methodology_vs_application_heatmap.pdf')}")

plt.close(fig)