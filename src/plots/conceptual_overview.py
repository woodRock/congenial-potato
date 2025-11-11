

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np

def create_conceptual_overview_figure():
    fig, ax = plt.subplots(figsize=(14, 10))

    # --- 1. Define Nodes and Connections ---

    # Data Source Nodes (Left)
    data_sources = {
        "Environmental": (0.1, 0.85, "Environmental Data\n(e.g., Temp, Salinity)"),
        "Acoustic": (0.1, 0.65, "Acoustic Data\n(e.g., Sonar, Echosounder)"),
        "Optical": (0.1, 0.45, "Optical Data\n(e.g., Images, Video)"),
        "Chemical": (0.1, 0.25, "Chemical Data\n(e.g., Mass Spec, eDNA)"),
    }

    # ML Model Node (Center)
    ml_model_center_x = 0.5
    ml_model_node = (ml_model_center_x, 0.5, "Machine Learning\nModels")

    # Application Nodes (Right)
    applications = {
        "Fisheries": (0.9, 0.8, "Fisheries management & stock assessment"),
        "Aquaculture": (0.9, 0.6, "Aquaculture & automated monitoring"),
        "Plankton": (0.9, 0.4, "Plankton & phytoplankton analysis"),
        "Molecular": (0.9, 0.2, "Molecular level analysis & food science"),
    }

    # --- 2. Draw Nodes (Boxes) ---
    box_width = 0.25
    box_height = 0.12
    text_props = dict(ha='center', va='center', fontsize=10, color='black')

    # Draw Data Source boxes
    data_source_boxes = {}
    for key, (x, y, label) in data_sources.items():
        rect = patches.Rectangle((x - box_width/2, y - box_height/2), box_width, box_height,
                                 linewidth=1.5, edgecolor='darkblue', facecolor='lightblue', zorder=2)
        ax.add_patch(rect)
        ax.text(x, y, label, **text_props)
        data_source_boxes[key] = (x + box_width/2, y)

    # Draw ML Model box
    ml_rect = patches.Rectangle((ml_model_node[0] - box_width/2, ml_model_node[1] - box_height/2), box_width, box_height,
                                linewidth=2, edgecolor='darkgreen', facecolor='lightgreen', zorder=2)
    ax.add_patch(ml_rect)
    ax.text(ml_model_node[0], ml_model_node[1], ml_model_node[2], **text_props)
    ml_model_left_edge = ml_model_node[0] - box_width/2
    ml_model_right_edge = ml_model_node[0] + box_width/2

    # Draw Application boxes
    application_boxes = {}
    for key, (x, y, label) in applications.items():
        rect = patches.Rectangle((x - box_width/2, y - box_height/2), box_width, box_height,
                                 linewidth=1.5, edgecolor='darkred', facecolor='lightcoral', zorder=2)
        ax.add_patch(rect)
        ax.text(x, y, label, **text_props)
        application_boxes[key] = (x - box_width/2, y)

    # --- 3. Draw Arrows ---
    arrow_props = dict(facecolor='gray', edgecolor='gray', arrowstyle='-|>', linewidth=1.5, mutation_scale=15, zorder=1)

    # Arrows from Data Sources to ML Model
    for key, (x_start, y_start) in data_source_boxes.items():
        x_end = ml_model_left_edge
        y_end = ml_model_node[1]
        ax.annotate("", xy=(x_end, y_end), xytext=(x_start, y_start), arrowprops=arrow_props)

    # Arrows from ML Model to Applications
    for key, (x_end, y_end) in application_boxes.items():
        x_start = ml_model_right_edge
        y_start = ml_model_node[1]
        ax.annotate("", xy=(x_end, y_end), xytext=(x_start, y_start), arrowprops=arrow_props)

    # --- 4. Figure Styling ---
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.1, 1)
    ax.axis('off')
    ax.set_title("Fig. 1. A conceptual overview of machine learning for marine biomass analysis.", fontsize=14, pad=20)
    
    plt.tight_layout()
    plt.savefig("figures/conceptual_overview_figure.png", dpi=300)
    plt.show()

# Run the function to generate the plot
create_conceptual_overview_figure()
