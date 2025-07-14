import matplotlib.pyplot as plt

# Define the triangular membership function parameters for Neoprene Rubber young modulus
a = 100000  # Minimum value (N/m²)
b = 300000  # Peak value (N/m²)
c = 500000  # Maximum value (N/m²)

def TriangularYoungFun(a1,a2,a3,graph): 
    # Define α levels
    # alpha = [0.3, 0.4, 0.5]
    alpha = [a1, a2, a3]
    colors = ["red", "purple", "orange"]  # Different colors for α-cuts

    # Calculate x (lower bound) and x̄ (upper bound) for each α
    x = [a + (b - a) * alpha_val for alpha_val in alpha]
    x_bar = [c - (c - b) * alpha_val for alpha_val in alpha]

    # Plot the triangular membership function
    plt.figure(figsize=(10, 6))
    plt.plot([a, b, c], [0, 1, 0], label="Triangular Membership Function", color="blue", linewidth=2)
    # Plot α-cut points and annotate coordinates
    for i in range(len(alpha)):
        # Plot the α-cut line
        plt.hlines(alpha[i], x[i], x_bar[i], color=colors[i], linestyles="dotted", linewidth=1.5)

        # Mark the points on the α-cut
        plt.scatter([x[i], x_bar[i]], [alpha[i], alpha[i]], color="black")

        # Annotate the coordinates with only α value (not α1, α2, α3)
        plt.text(x[i], alpha[i] + 0.02, f"({x[i]:.2f}, {alpha[i]:.1f})", color="black", fontsize=9)
        plt.text(x_bar[i], alpha[i] + 0.02, f"({x_bar[i]:.2f}, {alpha[i]:.1f})", color="black", fontsize=9)

        # Draw vertical dashed lines from α-cut points down to x-axis (Intersection Lines)
        plt.vlines(x[i], 0, alpha[i], color="green", linestyles="dashed", linewidth=1)
        plt.vlines(x_bar[i], 0, alpha[i], color="green", linestyles="dashed", linewidth=1)
    # Add labels and decorations
    plt.title("α-Cut Plane for Young's Modulus of Neoprene Rubber (Triangular MF)", fontsize=14)
    plt.xlabel("Young's Modulus (N/m²)", fontsize=12)
    plt.ylabel("Membership Degree (μ)", fontsize=12)
    plt.axhline(0, color='black', linewidth=0.5, linestyle='--')
    plt.axvline(a, color='gray', linestyle="--", label="a (Min)")
    plt.axvline(b, color='gray', linestyle="--", label="b (Peak)")
    plt.axvline(c, color='gray', linestyle="--", label="c (Max)")
    plt.grid(alpha=0.4)

    # Custom legend for α-cuts with smaller size
    plt.scatter([], [], color="red", label=r"$\alpha_1 = 0.3$")
    plt.scatter([], [], color="purple", label=r"$\alpha_2 = 0.4$")
    plt.scatter([], [], color="orange", label=r"$\alpha_3 = 0.5$")

    # Make legend smaller
    plt.legend(fontsize=9, frameon=True, loc="upper right", borderpad=0.3, handletextpad=0.3)

    # plt.show()
    g = "static/img/" + graph
    plt.savefig(g)
    plt.close()  # Close the figure to free up memory