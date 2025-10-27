import matplotlib.pyplot as plt
import matplotlib.patches as patches

def create_future_trends_figure():
    """
    Generates a 1x2 figure showing two future trends:
    (a) Sensor Fusion and (b) Real-time Edge Computing.
    """
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    fig.suptitle('Fig. 4. Conceptual diagrams of future trends in ML for marine analysis.', 
                 fontsize=16, y=0.98)

    # --- (a) Sensor Fusion ---
    ax = axes[0]
    ax.set_title("(a) Sensor Fusion", fontsize=14)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Define styles
    input_style = dict(boxstyle='round,pad=0.4', fc='lightblue', ec='darkblue')
    model_style = dict(boxstyle='round,pad=0.4', fc='lightgreen', ec='darkgreen', lw=2)
    output_style = dict(boxstyle='round,pad=0.4', fc='lightcoral', ec='darkred')
    arrow_style = dict(arrowstyle='-|>', facecolor='gray', edgecolor='gray', lw=1.5, mutation_scale=20)

    # Input nodes
    ax.text(0.15, 0.8, "Acoustic Data", ha='center', va='center', bbox=input_style)
    ax.text(0.15, 0.5, "Optical Data\n(Video/Stills)", ha='center', va='center', bbox=input_style)
    ax.text(0.15, 0.2, "Chemical Data\n(eDNA/MS)", ha='center', va='center', bbox=input_style)
    
    # Model node
    ax.text(0.5, 0.5, "Unified ML Model\n(Sensor Fusion)", ha='center', va='center', bbox=model_style)
    
    # Output node
    ax.text(0.85, 0.5, "Integrated\nBiomass\nAssessment", ha='center', va='center', bbox=output_style)

    # Arrows
    ax.add_patch(patches.FancyArrowPatch((0.28, 0.8), (0.38, 0.55), connectionstyle="arc3,rad=-0.2", **arrow_style))
    ax.add_patch(patches.FancyArrowPatch((0.28, 0.5), (0.38, 0.5), **arrow_style))
    ax.add_patch(patches.FancyArrowPatch((0.28, 0.2), (0.38, 0.45), connectionstyle="arc3,rad=0.2", **arrow_style))
    ax.add_patch(patches.FancyArrowPatch((0.62, 0.5), (0.73, 0.5), **arrow_style))

    # --- (b) Real-time Edge Computing ---
    ax = axes[1]
    ax.set_title("(b) Real-time Edge Computing", fontsize=14)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # AUV/Trawler body
    ax.add_patch(patches.Rectangle((0.1, 0.2), 0.8, 0.6, fc='lightgray', ec='black', lw=2))
    ax.text(0.5, 0.85, "AUV / Smart Trawler", ha='center', va='center', fontsize=12)
    
    # On-board AI
    ax.text(0.5, 0.6, "On-Board AI\n(Edge CPU/GPU)", ha='center', va='center', bbox=model_style)
    
    # Input Data
    ax.text(0.1, 0.4, "Raw Sensor Data\n(Video, Sonar)", ha='center', va='center', bbox=input_style)
    ax.add_patch(patches.FancyArrowPatch((0.2, 0.4), (0.38, 0.55), connectionstyle="arc3,rad=0.2", **arrow_style))
    
    # Output Decision
    ax.text(0.8, 0.4, "Real-time Decision:\n'Species X Count: 42'", ha='center', va='center', bbox=output_style)
    ax.add_patch(patches.FancyArrowPatch((0.62, 0.55), (0.7, 0.4), connectionstyle="arc3,rad=0.2", **arrow_style))

    # --- Final Touches ---
    plt.tight_layout(rect=[0, 0, 1, 0.93])
    plt.savefig("figures/future_trends_figure.png", dpi=300)    
    plt.show()

# Run the function
create_future_trends_figure()