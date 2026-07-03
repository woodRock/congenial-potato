import matplotlib.pyplot as plt
import collections
import numpy as np
import os
import re
import json

import json

# --- Read the categorized papers ---
with open('/Users/woodj/Desktop/congenial-potato/src/categorized_papers.json', 'r') as f:
    categorized_papers = json.load(f)

methods_data = [paper['methodology_category'] for paper in categorized_papers]
applications_data = [paper['application_category'] for paper in categorized_papers]

# --- Read and parse the bib file for years ---
with open('/Users/woodj/Desktop/congenial-potato/refs.bib', 'r') as f:
    content = f.read()

entries = content.split('\n@')
years_data = []
for entry in entries:
    if not entry.strip():
        continue
    year_match = re.search(r'year\s*=\s*[{"](\d{4})["}]', entry, re.IGNORECASE)
    if year_match:
        years_data.append(int(year_match.group(1)))


# --- The rest of the plotting code remains the same ---
year_counts = collections.Counter(years_data)
years = sorted(year_counts.keys())
counts_years = [year_counts[year] for year in years]

method_counts = collections.Counter(methods_data)
# Sort methods for consistent pie chart ordering
sorted_methods = sorted(method_counts.keys())
counts_methods = [method_counts[key] for key in sorted_methods]
labels_methods = sorted_methods

app_counts = collections.Counter(applications_data)
print(app_counts)
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

plt.style.use('seaborn-v0_8-white')
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 14
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12
plt.rcParams['legend.fontsize'] = 12

# 1. Bar Chart: Papers per Year
fig1, ax1 = plt.subplots(figsize=(8, 6))
ax1.bar(years, counts_years, color='#4C72B0', edgecolor='black', width=0.6, linewidth=0.8)
ax1.set_xlabel('Publication Year', fontsize=14, fontweight='bold')
ax1.set_ylabel('Number of Papers', fontsize=14, fontweight='bold')
ax1.set_title('Distribution of Included Papers by Year', pad=20, fontweight='bold', fontsize=16)
ax1.set_xticks(years)
ax1.tick_params(axis='both', labelsize=14)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.yaxis.grid(True, linestyle='--', alpha=0.6, zorder=0)
ax1.set_axisbelow(True) # Ensure grid is behind bars
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'papers_per_year.pdf'), dpi=300, bbox_inches='tight')
plt.savefig(os.path.join(output_dir, 'papers_per_year.png'), dpi=300, bbox_inches='tight')
print(f"Saved {os.path.join(output_dir, 'papers_per_year.pdf/.png')}")

# 2. Pie Chart: ML Method Distribution
fig2, ax2 = plt.subplots(figsize=(8, 8))
def func(pct, allvals):
    return "{:.1f}%".format(pct) if pct > 3 else ''

# Use a professional color palette
colors = ['#4C72B0', '#55A868', '#C44E52', '#8172B3', '#CCB974', '#64B5CD']

wedges, texts, autotexts = ax2.pie(counts_methods,
                                   autopct=lambda pct: func(pct, counts_methods),
                                   startangle=90,
                                   pctdistance=0.75,
                                   colors=colors[:len(labels_methods)],
                                   wedgeprops={'edgecolor': 'white', 'linewidth': 1.5}
                                   )

ax2.set_title('Distribution of Primary ML Methodologies', pad=20, fontweight='bold', fontsize=16)

legend = ax2.legend(wedges, labels_methods,
                    title="ML Methods",
                    loc="lower center",
                    bbox_to_anchor=(0.5, -0.15),
                    ncol=2,
                    frameon=True,
                    fontsize=12)

plt.setp(autotexts, size=12, weight="bold", color="white")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'ml_method_distribution.pdf'),
            dpi=300,
            bbox_inches='tight',
            pad_inches=0.1)
print(f"Saved {os.path.join(output_dir, 'ml_method_distribution.pdf')}")


# 3. Bar Chart: Application Focus Distribution
fig3, ax3 = plt.subplots(figsize=(8, 7))
bars = ax3.bar(labels_apps, counts_apps, color='#C44E52', edgecolor='black', width=0.6, linewidth=0.8)
ax3.set_xlabel('Application Area', fontsize=14, fontweight='bold')
ax3.set_ylabel('Number of Papers', fontsize=14, fontweight='bold')
ax3.set_title('Distribution of Papers by Primary Application Focus', pad=20, fontweight='bold', fontsize=16)
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)
ax3.yaxis.grid(True, linestyle='--', alpha=0.6, zorder=0)
ax3.set_axisbelow(True)
plt.xticks(rotation=45, ha='right', fontsize=13)
ax3.tick_params(axis='y', labelsize=13)
ax3.bar_label(bars, padding=3, fontweight='bold', fontsize=13)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'application_focus_distribution.pdf'), dpi=300, bbox_inches='tight')
plt.savefig(os.path.join(output_dir, 'application_focus_distribution.png'), dpi=300, bbox_inches='tight')
print(f"Saved {os.path.join(output_dir, 'application_focus_distribution.pdf/.png')}")

plt.close(fig1)
plt.close(fig2)
plt.close(fig3)

plt.close(fig1)
plt.close(fig2)
plt.close(fig3)