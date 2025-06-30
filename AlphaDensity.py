# import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Set the backend to 'Agg'
import matplotlib.pyplot as plt

# Define the trapezoidal membership function parameters for Density of Aluminum
a = 2.66  # Minimum value (kg/m³)
b = 2.68  # Lower bound of plateau (kg/m³)
c = 2.72  # Upper bound of plateau (kg/m³)
d = 2.74  # Maximum value (kg/m³)

# Define α levels with a wider range
# alpha = []
def alphaDensityFun(a1,a2,a3,graph):
    # alpha = [0.313, 0.455, 0.585]  # Adjusted alpha values for better visualization
    alpha = [a1, a2, a3]

    # Calculate x (lower bound) and x̄ (upper bound) for each α
    x = [a + (b - a) * alpha_val for alpha_val in alpha]  # Left slope
    x_bar = [d - (d - c) * alpha_val for alpha_val in alpha]  # Right slope

    # Debugging prints
    # print(f"Updated alpha values: {alpha}")
    # print(f"Lower bounds (x): {x}")
    # print(f"Upper bounds (x̄): {x_bar}")

    # Clear previous plots
    plt.clf()
    plt.figure(figsize=(10, 6))
    plt.plot([a, b, c, d], [0, 1, 1, 0], label="Trapezoidal Membership Function", color="blue", linewidth=2)

    # Plot α-cut points and annotate coordinates
    for i in range(len(alpha)):
        plt.hlines(alpha[i], x[i], x_bar[i], color="red", linestyle="solid", linewidth=2)
        plt.scatter([x[i], x_bar[i]], [alpha[i], alpha[i]], color="black", label=f"α = {alpha[i]:.3f}" if i == 0 else "")

        # Annotate coordinates
        plt.text(x[i], alpha[i] + 0.02, f"({x[i]:.2f}, {alpha[i]:.3f})", color="black", fontsize=9)
        plt.text(x_bar[i], alpha[i] + 0.02, f"({x_bar[i]:.2f}, {alpha[i]:.3f})", color="black", fontsize=9)

        # Draw vertical dashed lines from α-cut points down to x-axis
        plt.vlines(x[i], 0, alpha[i], color="green", linestyles="dashed", linewidth=1)
        plt.vlines(x_bar[i], 0, alpha[i], color="green", linestyles="dashed", linewidth=1)

    # Add labels and decorations
    plt.title("α-Cut Plane for Density (ρ) of Aluminum (Trapezoidal MF)", fontsize=14)
    plt.xlabel("Density (kg/m³)", fontsize=12)
    plt.ylabel("Membership Degree (μ)", fontsize=12)
    plt.axhline(0, color='black', linewidth=0.5, linestyle='--')
    plt.axvline(a, color='gray', linestyle="--", label="a (Min)")
    plt.axvline(b, color='gray', linestyle="--", label="b (Start Plateau)")
    plt.axvline(c, color='gray', linestyle="--", label="c (End Plateau)")
    plt.axvline(d, color='gray', linestyle="--", label="d (Max)")
    plt.legend()
    plt.grid(alpha=0.4)
    # plt.savefig("g1.png")
    # plt.show()
    g = "static/img/" + graph
    plt.savefig(g)
    plt.close()  # Close the figure to free up memory