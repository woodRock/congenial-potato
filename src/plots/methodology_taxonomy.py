

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches

def create_taxonomy_figure():
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.size'] = 12
    fig, ax = plt.subplots(figsize=(10, 7))
    fig.suptitle('Fig. 3. A taxonomy of machine learning methodologies reviewed in this survey.', 
                 y=0.98, fontweight='bold', fontsize=14)

    node_style = dict(boxstyle='round,pad=0.4', fc='#F9F9F9', ec='#333333', lw=1.5, alpha=0.9)
    line_style = dict(color='#555555', linestyle='-', linewidth=2.0, zorder=0)

    x_level_0 = 0.02
    x_level_1 = 0.5

    level0 = {
        "ML": {"label": "Machine Learning\nMethodologies", "pos": (x_level_0, 0.5)}
    }

    l1_y_pos = np.linspace(0.9, 0.1, 5)
    level1 = {
        "Traditional":    {"label": "Traditional Supervised", "pos": (x_level_1, l1_y_pos[0])},
        "CNN":            {"label": "Deep Learning - CNNs", "pos": (x_level_1, l1_y_pos[1])},
        "Transformers":   {"label": "Deep Learning - Transformers", "pos": (x_level_1, l1_y_pos[2])},
        "Unsupervised":   {"label": "Unsupervised & Self-Supervised", "pos": (x_level_1, l1_y_pos[3])},
        "Evolutionary":   {"label": "Evolutionary Computation", "pos": (x_level_1, l1_y_pos[4])}
    }

    connections_l0_l1 = ["Traditional", "CNN", "Transformers", "Unsupervised", "Evolutionary"]

    all_nodes = {**level0, **level1}
    for key, val in all_nodes.items():
        ax.text(val["pos"][0], val["pos"][1], val["label"], 
                ha='left', va='center', bbox=node_style, zorder=5, fontweight='bold', fontsize=12)

    def draw_connector(p_pos, c_pos):
        mid_x = (p_pos[0] + c_pos[0]) / 2.0 + 0.05
        # Horizontal line from parent
        ax.plot([p_pos[0] + 0.22, mid_x], [p_pos[1], p_pos[1]], **line_style)
        # Horizontal line to child
        ax.plot([mid_x, c_pos[0] - 0.01], [c_pos[1], c_pos[1]], **line_style)
        # Vertical line connecting them
        ax.plot([mid_x, mid_x], [p_pos[1], c_pos[1]], **line_style)

    parent_node = level0["ML"]
    for key in connections_l0_l1:
        child_node = level1[key]
        draw_connector(parent_node["pos"], child_node["pos"])

    ax.axis('off')
    ax.set_ylim(-0.1, 1)
    ax.set_xlim(0, 1)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig("figures/methodology_taxonomy_figure.pdf", dpi=300, bbox_inches='tight')
    # plt.show()

create_taxonomy_figure()
