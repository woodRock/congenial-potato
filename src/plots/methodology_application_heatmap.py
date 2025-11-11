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
plt.style.use('seaborn-v0_8-talk')
fig, ax = plt.subplots(figsize=(12, 9))

sns.heatmap(cross_tab,
            annot=True,
            fmt="d",
            cmap="Blues",
            linewidths=.5,
            cbar=True,
            ax=ax)

ax.set_title('Frequency of ML Methodologies Applied Across Application Areas', pad=20)
ax.set_xlabel('Machine Learning Methodology')
ax.set_ylabel('Application Area')
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)

# --- Save Figure ---
output_dir = 'figures'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Created directory: {output_dir}")

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'methodology_vs_application_heatmap.png'), bbox_inches='tight')
print(f"Saved {os.path.join(output_dir, 'methodology_vs_application_heatmap.png')}")

plt.close(fig)