# # import matplotlib.pyplotas plt
# import matplotlib.pyplot as plt
# # Define the triangular membership function parameters for Density of Aluminum
# a = 2.68  # Minimum value (kg/m³)
# b = 2.70  # Most likely value (kg/m³)
# c = 2.72  # Maximum value (kg/m³)

# # Define α levels
# alpha = [0.3, 0.4, 0.5]

# # Calculate x (lower bound) and x̄ (upper bound) for each α
# x = [a + (b - a) * alpha_val for alpha_val in alpha]
# x_bar = [c - (c - b) * alpha_val for alpha_val in alpha]


# # Plot the triangular membership function
# plt.figure(figsize=(10, 6))
# plt.plot([a, b, c], [0, 1, 0], label="Triangular Membership Function", color="blue", linewidth=2)

# # Plot α-cut points and annotate coordinates
# for i in range(len(alpha)):
#     plt.hlines(alpha[i], x[i], x_bar[i], color="red", linestyles="dotted", linewidth=1.5)
#     plt.scatter([x[i], x_bar[i]], [alpha[i], alpha[i]], color="black", label=f"α = {0.3,0.4,0.5}" if i == 0 else "")

#     # Annotate coordinates
#     plt.text(x[i], alpha[i] + 0.02, f"({x[i]:.2f}, {alpha[i]})", color="black", fontsize=9)
#     plt.text(x_bar[i], alpha[i] + 0.02, f"({x_bar[i]:.2f}, {alpha[i]})", color="black", fontsize=9)

# # Add labels and decorations
# plt.title("α-Cut Plane for Density (ρ) of Aluminum at 45° (Triangular MF)", fontsize=14)
# plt.xlabel("Density (kg/m³)", fontsize=12)
# plt.ylabel("Membership Degree (μ)", fontsize=12)
# plt.axhline(0, color='black', linewidth=0.5, linestyle='--')
# plt.axvline(a, color='gray', linestyle="--", label="a (Min)")
# plt.axvline(b, color='gray', linestyle="--", label="b (Peak)")
# plt.axvline(c, color='gray', linestyle="--", label="c (Max)")
# plt.legend()
# plt.grid(alpha=0.4)
# plt.show()



# import numpy as np
# import matplotlib.pyplot as plt

# # Define trapezoidal membership function parameters
# a, b, c, d = 2690, 2693, 2702, 2705  # Trapezoidal points

# # Generate x values and corresponding membership values
# x_density = np.linspace(2687, 2707, 500)
# mf_density = np.piecewise(
#     x_density,
#     [x_density <= a, (a < x_density) & (x_density < b), 
#      (b <= x_density) & (x_density <= c), (c < x_density) & (x_density < d), x_density >= d],
#     [0, lambda x: (x - a) / (b - a), 1, lambda x: (d - x) / (d - c), 0]
# )

# # Correct α-cut points calculated using membership function formulas
# alpha_cut_points = [
#     # (x_min, x_max, alpha, alpha_prime) with x_min and x_max computed for desired alphas
#     (a + 0.3*(b - a), d - 0.36*(d - c), 0.3, 0.36),  # First line
#     (a + 0.4*(b - a), d - 0.45*(d - c), 0.4, 0.45),  # Second line
#     (a + 0.5*(b - a), d - 0.58*(d - c), 0.5, 0.58)   # Third line
# ]

# # Plotting the trapezoidal membership function
# plt.figure(figsize=(10, 6))
# plt.plot(x_density, mf_density, label='Trapezoidal Membership Function', color='blue')

# # Plotting corrected α-cut lines
# for i, (x_min, x_max, alpha, alpha_prime) in enumerate(alpha_cut_points):
#     plt.scatter([x_min, x_max], [alpha, alpha_prime], color='black')  # Points on the MF
#     plt.plot([x_min, x_max], [alpha, alpha_prime], color='red', linestyle='dotted')  # Slanted line
#     plt.text(x_min, alpha, f'({x_min:.1f}, {alpha})', fontsize=10, ha='right')
#     plt.text(x_max, alpha_prime, f'({x_max:.1f}, {alpha_prime})', fontsize=10, ha='left')

# # Mark key points with dashed lines
# plt.axvline(x=a, color='gray', linestyle='dashed', label='a (2690)')
# plt.axvline(x=b, color='gray', linestyle='dashed', label='b (2693)')
# plt.axvline(x=c, color='gray', linestyle='dashed', label='c (2702)')
# plt.axvline(x=d, color='gray', linestyle='dashed', label='d (2705)')

# plt.xlabel("Density of Aluminum (kg/m³)")
# plt.ylabel("Membership Degree ($\\mu$)")
# plt.title("Corrected α - α' Cut Plane for Density (Trapezoidal MF)")
# plt.legend(loc='upper right')
# plt.grid(True)
# plt.savefig("corrected_alpha_cut_plot.png")
# plt.show()