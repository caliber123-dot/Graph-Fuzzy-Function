import numpy as np
import matplotlib.pyplot as plt

# Define the Trapezoidal Membership Function
def trapezoidal_mf(x, a, b, c, d):
    return np.piecewise(
        x,
        [x < a, (a <= x) & (x < b), (b <= x) & (x <= c), (c < x) & (x <= d), x > d],
        [0, lambda x: (x - a) / (b - a), 1, lambda x: (d - x) / (d - c), 0],
    )

# Define parameters for the trapezoidal function
a, b, c, d = 0.5, 0.6, 0.8, 0.9  # Min, peak, upper peak, Max
# Generate x values
x = np.linspace(0.5, 0.9, 1000)
y = trapezoidal_mf(x, a, b, c, d)

def alphaYoungFun(a1,a2,a3,graph):    
    # Define α-cut levels
    # alpha_cuts = [0.35, 0.45, 0.56]
    alpha_cuts = [a1, a2, a3]

    # Plot the membership function
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, label="Trapezoidal Membership Function", color="blue")

    # Mark α-cut levels
    for alpha in alpha_cuts:
        # Compute α-cut intersection points
        if alpha < 1:
            x_alpha_left = a + alpha * (b - a)
            x_alpha_right = d - alpha * (d - c)
        else:
            x_alpha_left, x_alpha_right = b, c  # At peak (μ = 1), the α-cut is (b, c)

        # Plot α-cut points and lines
        plt.scatter([x_alpha_left, x_alpha_right], [alpha, alpha], color="black")
        plt.hlines(alpha, x_alpha_left, x_alpha_right, colors="red", linewidth=2)
        plt.vlines([x_alpha_left, x_alpha_right], ymin=0, ymax=alpha, colors="green", linestyle="dotted")
        plt.text(x_alpha_left, alpha, f"({x_alpha_left:.3f}, {alpha})", verticalalignment="bottom")
        plt.text(x_alpha_right, alpha, f"({x_alpha_right:.3f}, {alpha})", verticalalignment="bottom")

    # Labels and legend
    plt.axvline(a, color="gray", linestyle="--", label="a (Min)")
    plt.axvline(b, color="gray", linestyle="--", label="b (peak)")
    plt.axvline(c, color="gray", linestyle="--", label="c (peak)")
    plt.axvline(d, color="gray", linestyle="--", label="d (Max)")
    plt.xlabel("Young's modulus (N/m³)")
    plt.ylabel("Membership Degree (μ)")
    plt.title("α-Cut for Young's modulus  of Aluminum (Trapezoidal MF)")
    plt.legend()
    plt.grid()
    # plt.savefig("g2.png")
    # plt.show()
    g = "static/img/" + graph
    plt.savefig(g)
    plt.close()  # Close the figure to free up memory
