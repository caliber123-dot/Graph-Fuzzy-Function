import numpy as np
import matplotlib.pyplot as plt

# Define trapezoidal membership function parameters
a, b, c, d = 2690, 2693, 2702, 2705  # Trapezoidal points

# Generate x values and corresponding membership values
x_density = np.linspace(2687, 2707, 500)
mf_density = np.piecewise(
    x_density,
    [x_density <= a, (a < x_density) & (x_density < b), 
     (b <= x_density) & (x_density <= c), (c < x_density) & (x_density < d), x_density >= d],
    [0, lambda x: (x - a) / (b - a), 1, lambda x: (d - x) / (d - c), 0]
)

# Correct α-cut points calculated using membership function formulas
alpha_cut_points = [
    # (x_min, x_max, alpha, alpha_prime) with x_min and x_max computed for desired alphas
    (a + 0.3*(b - a), d - 0.36*(d - c), 0.3, 0.36),  # First line
    (a + 0.4*(b - a), d - 0.45*(d - c), 0.4, 0.45),  # Second line
    (a + 0.5*(b - a), d - 0.58*(d - c), 0.5, 0.58)   # Third line
]

# Plotting the trapezoidal membership function
plt.figure(figsize=(10, 6))
plt.plot(x_density, mf_density, label='Trapezoidal Membership Function', color='blue')

# Plotting corrected α-cut lines
for i, (x_min, x_max, alpha, alpha_prime) in enumerate(alpha_cut_points):
    plt.scatter([x_min, x_max], [alpha, alpha_prime], color='black')  # Points on the MF
    plt.plot([x_min, x_max], [alpha, alpha_prime], color='red', linestyle='dotted')  # Slanted line
    plt.text(x_min, alpha, f'({x_min:.1f}, {alpha})', fontsize=10, ha='right')
    plt.text(x_max, alpha_prime, f'({x_max:.1f}, {alpha_prime})', fontsize=10, ha='left')

# Mark key points with dashed lines
plt.axvline(x=a, color='gray', linestyle='dashed', label='a (2690)')
plt.axvline(x=b, color='gray', linestyle='dashed', label='b (2693)')
plt.axvline(x=c, color='gray', linestyle='dashed', label='c (2702)')
plt.axvline(x=d, color='gray', linestyle='dashed', label='d (2705)')

plt.xlabel("Density of Aluminum (kg/m³)")
plt.ylabel("Membership Degree ($\\mu$)")
plt.title("Corrected α - α' Cut Plane for Density (Trapezoidal MF)")
plt.legend(loc='upper right')
plt.grid(True)
plt.savefig("corrected_alpha_cut_plot.png")
plt.show()