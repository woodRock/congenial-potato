import matplotlib.pyplot as plt
import collections
import numpy as np
import os # Import os to check/create directory

# --- Data based on the 44 papers provided in the bib file ---

# 1. Publication Years
years_data = [
    2024, 2022, 2022, 2025, 2025, 2025, 2023, 2021, 2023, 2025, 2025, 2020, 2023, 2023, 2025, 2020, 2021, 2024, 2021, 2024, 2023, 2023, 2024, 2024, 2023, 2021, 2025, 2023, 2022, 2024, 2020, 2021, 2022, 2022, 2025, 2024, 2024, 2025, 2024, 2022, 2023, 2025, 2024, 2020
]
year_counts = collections.Counter(years_data)
years = sorted(year_counts.keys())
counts_years = [year_counts[year] for year in years]

# 2. ML Methods (Simplified Categories based on primary focus/mention)
# Categories: CNN/U-Net, Transformer, YOLO, Trad. Supervised (SVM/RF/Boost/Prob), Unsupervised, Self-Supervised, Symbolic Regression, Review/Meta, Other/General ML
methods_data = [
    'CNN/U-Net', 'Unsupervised', 'Review/Meta', 'CNN/U-Net', 'Self-Supervised', 'Review/Meta', 'Other/General ML', 'Unsupervised', 'Other/General ML', 'Symbolic Regression', 'CNN/U-Net', 'CNN/U-Net', 'CNN/U-Net', 'CNN/U-Net', 'Trad. Supervised', 'Trad. Supervised', 'Trad. Supervised', 'Trad. Supervised', 'CNN/U-Net', 'Self-Supervised', 'Trad. Supervised', 'YOLO', 'Transformer', 'YOLO', 'Other/General ML', 'CNN/U-Net', 'Trad. Supervised', 'CNN/U-Net', 'CNN/U-Net', 'Other/General ML', 'CNN/U-Net', 'Other/General ML', 'CNN/U-Net', 'Trad. Supervised', 'Transformer', 'Other/General ML', 'Other/General ML', 'Transformer', 'CNN/U-Net', 'Trad. Supervised', 'Trad. Supervised', 'Review/Meta', 'Trad. Supervised', 'Trad. Supervised'
]

method_counts = collections.Counter(methods_data)
# Sort methods for consistent pie chart ordering
sorted_methods = sorted(method_counts.keys())
counts_methods = [method_counts[key] for key in sorted_methods]
labels_methods = sorted_methods

# 3. Application Focus
applications_data = [
    'Aquaculture', 'Plankton Analysis', 'Plankton Analysis', 'Fisheries Assessment', 'Plankton Analysis', 'Remote Sensing', 'Underwater Acoustics', 'Plankton Analysis', 'Fisheries Management', 'Food Authenticity', 'Aquaculture', 'Plankton Analysis', 'Underwater Acoustics', 'Underwater Acoustics', 'Plankton Analysis', 'Plankton Analysis', 'Plankton Analysis', 'Food Authenticity', 'Plankton Analysis', 'Plankton Analysis', 'Underwater Acoustics', 'Aquaculture', 'Aquaculture', 'Fisheries Management', 'Plankton Analysis', 'Plankton Analysis', 'Algal Biomass', 'Plankton Analysis', 'Fisheries Assessment', 'Fisheries Management', 'Plankton Analysis', 'Plankton Analysis', 'Underwater Acoustics', 'Food Authenticity', 'Food Authenticity', 'Plankton Analysis', 'Food Authenticity', 'Plankton Analysis', 'Aquaculture', 'Food Authenticity', 'Food Authenticity', 'Food Authenticity', 'Food Authenticity', 'Food Authenticity'
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
