import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches

def create_taxonomy_figure():
    """
    Generates a tree diagram for the methodology taxonomy.
    """
    fig, ax = plt.subplots(figsize=(10, 7))
    fig.suptitle('Fig. 3. A taxonomy of machine learning methodologies reviewed in this survey.', 
                 fontsize=16, y=0.98)

    # --- 1. Define Node Styles ---
    
    # Bounding box for text nodes
    node_style = dict(boxstyle='round,pad=0.5', fc='w', ec='k', lw=1)
    
    # Line style for connectors
    line_style = dict(color='gray', linestyle='-', linewidth=1.5, zorder=0)

    # --- 2. Define Node Positions (x, y) and Labels ---

    # We use a 3-level hierarchy
    x_level_0 = 0.05
    x_level_1 = 0.4
    x_level_2 = 0.8
    
    # Level 0 (Root)
    level0 = {
        "ML": {"label": "Machine Learning\nMethodologies", "pos": (x_level_0, 0.5)}
    }

    # Level 1 (Main Categories)
    l1_y_pos = np.linspace(0.9, 0.1, 4)
    level1 = {
        "Supervised": {"label": "Supervised Learning", "pos": (x_level_1, l1_y_pos[0])},
        "Deep":       {"label": "Deep Learning", "pos": (x_level_1, l1_y_pos[1])},
        "Unsupervised": {"label": "Unsupervised Learning", "pos": (x_level_1, l1_y_pos[2])},
        "EvoComp":    {"label": "Evolutionary Computation &\nSymbolic Regression", "pos": (x_level_1, l1_y_pos[3])}
    }

    # Level 2 (Sub-categories)
    l2_sup_y = np.linspace(level1["Supervised"]["pos"][1] + 0.05, level1["Supervised"]["pos"][1] - 0.05, 2)
    l2_deep_y = np.linspace(level1["Deep"]["pos"][1] + 0.05, level1["Deep"]["pos"][1] - 0.05, 2)
    
    level2 = {
        "Regression":     {"label": "Regression Models\n(RF, SVR, ...)", "pos": (x_level_2, l2_sup_y[0])},
        "Classification": {"label": "Classification Models\n(SVM, k-NN, ...)", "pos": (x_level_2, l2_sup_y[1])},
        
        "CNNs":           {"label": "Convolutional Neural Networks\n(CNNs)", "pos": (x_level_2, l2_deep_y[0])},
        "Advanced":       {"label": "Advanced Architectures\n(YOLO, Transformers)", "pos": (x_level_2, l2_deep_y[1])},
        
        "Clustering":     {"label": "Clustering\n(K-Means, DBSCAN, ...)", "pos": (x_level_2, level1["Unsupervised"]["pos"][1])},
        
        "GP":             {"label": "Genetic Programming\n(GP)", "pos": (x_level_2, level1["EvoComp"]["pos"][1])}
    }

    # Connections
    connections_l0_l1 = ["Supervised", "Deep", "Unsupervised", "EvoComp"]
    connections_l1_l2 = {
        "Supervised": ["Regression", "Classification"],
        "Deep":       ["CNNs", "Advanced"],
        "Unsupervised": ["Clustering"],
        "EvoComp":    ["GP"]
    }

    # --- 3. Draw Nodes ---
    all_nodes = {**level0, **level1, **level2}
    for key, val in all_nodes.items():
        ax.text(val["pos"][0], val["pos"][1], val["label"], 
                ha='left', va='center', bbox=node_style, zorder=5)

    # --- 4. Draw Connectors ---
    
    # Function to draw a right-angled connector
    def draw_connector(p_pos, c_pos):
        # p_pos = parent (x, y)
        # c_pos = child (x, y)
        mid_x = (p_pos[0] + c_pos[0]) / 2.0
        
        # Horizontal line from parent
        ax.plot([p_pos[0] + 0.09, mid_x], [p_pos[1], p_pos[1]], **line_style) 
        # Horizontal line to child
        ax.plot([mid_x, c_pos[0] - 0.09], [c_pos[1], c_pos[1]], **line_style)
        # Vertical connector
        ax.plot([mid_x, mid_x], [p_pos[1], c_pos[1]], **line_style)

    # L0 -> L1 connectors
    parent_node = level0["ML"]
    for key in connections_l0_l1:
        child_node = level1[key]
        draw_connector(parent_node["pos"], child_node["pos"])

    # L1 -> L2 connectors
    for parent_key, child_keys in connections_l1_l2.items():
        parent_node = level1[parent_key]
        for child_key in child_keys:
            child_node = level2[child_key]
            draw_connector(parent_node["pos"], child_node["pos"])

    # --- 5. Final Styling ---
    ax.axis('off')
    ax.set_ylim(0, 1)
    ax.set_xlim(0, 1)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig("figures/methodology_taxonomy_figure.png", dpi=300)
    plt.show()

# Run the function to generate the plot
create_taxonomy_figure()