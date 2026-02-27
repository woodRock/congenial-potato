import matplotlib.pyplot as plt
import matplotlib.patches as patches

def create_future_trends_figure():
    """
    Generates a 1x2 figure showing two future trends:
    (a) Sensor Fusion and (b) Real-time Edge Computing.
    """
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.size'] = 10
    fig, axes = plt.subplots(1, 2, figsize=(14, 7))
    fig.suptitle('Fig. 4. Conceptual diagrams of future trends in ML for marine analysis.', 
                 y=0.98, fontweight='bold', fontsize=12)

    # Professional colors
    color_input = '#4C72B0' # Blue
    color_model = '#55A868' # Green
    color_output = '#C44E52' # Red
    arrow_color = '#444444'

    # --- (a) Sensor Fusion ---
    ax = axes[0]
    ax.set_title("(a) Sensor Fusion", fontweight='bold', pad=15)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Define styles
    input_style = dict(boxstyle='round,pad=0.4', fc=color_input, ec='#2E4469', alpha=0.8)
    model_style = dict(boxstyle='round,pad=0.4', fc=color_model, ec='#33643E', lw=2, alpha=0.8)
    output_style = dict(boxstyle='round,pad=0.4', fc=color_output, ec='#762F31', alpha=0.8)
    arrow_style = dict(arrowstyle='-|>', facecolor=arrow_color, edgecolor=arrow_color, lw=1.5, mutation_scale=20)

    # Input nodes
    text_props = dict(ha='center', va='center', fontsize=10, color='white', fontweight='bold')
    ax.text(0.18, 0.8, "Acoustic Data", bbox=input_style, **text_props)
    ax.text(0.18, 0.5, "Optical Data\n(Video/Stills)", bbox=input_style, **text_props)
    ax.text(0.18, 0.2, "Chemical Data\n(eDNA/MS)", bbox=input_style, **text_props)
    
    # Model node
    ax.text(0.5, 0.5, "Unified ML Model\n(Sensor Fusion)", bbox=model_style, **text_props)
    
    # Output node
    ax.text(0.85, 0.5, "Integrated\nBiomass\nAssessment", bbox=output_style, **text_props)

    # Arrows
    ax.add_patch(patches.FancyArrowPatch((0.32, 0.8), (0.38, 0.55), connectionstyle="arc3,rad=-0.2", **arrow_style))
    ax.add_patch(patches.FancyArrowPatch((0.32, 0.5), (0.38, 0.5), **arrow_style))
    ax.add_patch(patches.FancyArrowPatch((0.32, 0.2), (0.38, 0.45), connectionstyle="arc3,rad=0.2", **arrow_style))
    ax.add_patch(patches.FancyArrowPatch((0.62, 0.5), (0.73, 0.5), **arrow_style))

    # --- (b) Real-time Edge Computing ---
    ax = axes[1]
    ax.set_title("(b) Real-time Edge Computing", fontweight='bold', pad=15)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # AUV/Trawler body
    ax.add_patch(patches.Rectangle((0.1, 0.2), 0.8, 0.6, fc='#F0F0F0', ec='#333333', lw=2))
    ax.text(0.5, 0.85, "AUV / Smart Trawler Platform", ha='center', va='center', fontweight='bold')
    
    # On-board AI
    ax.text(0.5, 0.6, "On-Board AI\n(Edge CPU/GPU)", bbox=model_style, **text_props)
    
    # Input Data
    ax.text(0.15, 0.4, "Raw Sensor Data\n(Video, Sonar)", bbox=input_style, **text_props)
    ax.add_patch(patches.FancyArrowPatch((0.25, 0.4), (0.38, 0.55), connectionstyle="arc3,rad=0.2", **arrow_style))
    
    # Output Decision
    ax.text(0.82, 0.4, "Real-time Decision:\n'Target Biomass: X'", bbox=output_style, **text_props)
    ax.add_patch(patches.FancyArrowPatch((0.62, 0.55), (0.72, 0.4), connectionstyle="arc3,rad=0.2", **arrow_style))

    # --- Final Touches ---
    plt.tight_layout(rect=[0, 0, 1, 0.93])
    plt.savefig("figures/future_trends_figure.pdf", dpi=300, bbox_inches='tight')    
    # plt.show()

# Run the function
create_future_trends_figure()