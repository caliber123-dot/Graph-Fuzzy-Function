import matplotlib.pyplot as plt
# Define the triangular membership function parameters for Density of Aluminum
a = 2.68  # Minimum value (kg/m³)
b = 2.70  # Most likely value (kg/m³)
c = 2.72  # Maximum value (kg/m³)

def TriangularDensity(a1,a2,a3,graph): 
    # Define α levels
    # alpha = [0.3, 0.4, 0.5]
    alpha = [a1, a2, a3]

    # Calculate x (lower bound) and x̄ (upper bound) for each α
    x = [a + (b - a) * alpha_val for alpha_val in alpha]
    x_bar = [c - (c - b) * alpha_val for alpha_val in alpha]

    # Plot the triangular membership function
    plt.figure(figsize=(10, 6))
    plt.plot([a, b, c], [0, 1, 0], label="Triangular Membership Function", color="blue", linewidth=2)

    # Plot α-cut points and annotate coordinates
    for i in range(len(alpha)):
        plt.hlines(alpha[i], x[i], x_bar[i], color="red", linestyles="dotted", linewidth=1.5)
        plt.scatter([x[i], x_bar[i]], [alpha[i], alpha[i]], color="black", label=f"α = {0.3,0.4,0.5}" if i == 0 else "")

        # Annotate coordinates
        plt.text(x[i], alpha[i] + 0.02, f"({x[i]:.2f}, {alpha[i]})", color="black", fontsize=9)
        plt.text(x_bar[i], alpha[i] + 0.02, f"({x_bar[i]:.2f}, {alpha[i]})", color="black", fontsize=9)

    # Add labels and decorations
    plt.title("α-Cut Plane for Density (ρ) of Aluminum at 45° (Triangular MF)", fontsize=14)
    plt.xlabel("Density (kg/m³)", fontsize=12)
    plt.ylabel("Membership Degree (μ)", fontsize=12)
    plt.axhline(0, color='black', linewidth=0.5, linestyle='--')
    plt.axvline(a, color='gray', linestyle="--", label="a (Min)")
    plt.axvline(b, color='gray', linestyle="--", label="b (Peak)")
    plt.axvline(c, color='gray', linestyle="--", label="c (Max)")
    plt.legend()
    plt.grid(alpha=0.4)
    # plt.show()
    g = "static/img/" + graph
    plt.savefig(g)
    plt.close()  # Close the figure to free up memory