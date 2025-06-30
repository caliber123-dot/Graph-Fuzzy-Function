# import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Set the backend to Agg
import matplotlib.pyplot as plt
# apha value
def GetFuzzyFunction_aplha(a_val, b_val, c_val, d_val, a1, a2, a3, g_name, material, module):
    # Trapezoidal Membership Function Points (Young's Modulus for Aluminium)
    # a, b, c, d = 68947600000, 71402200000, 77402200000, 79966000000
    a = a_val
    b = b_val
    c = c_val
    d = d_val
    # User input
    # alpha_input = input("Enter α values (comma separated, like 0.3,0.3333,0.4567): ")
    # alpha_values = [float(x.strip()) for x in alpha_input.split(',')]
    # alpha_values = [0.35, 0.45, 0.56]
    alpha_values = [a1, a2, a3]
    # Precision for formatting labels
    precisions = [len(str(x).split('.')[-1]) if '.' in str(x) else 0 for x in alpha_values]
    # Calculate α-cut points
    x = []
    x_bar = []
    
    for alpha in alpha_values:
        if alpha == 1.0:
            # Flat top between b and c
            x.append(b)
            x_bar.append(c)
        else:
            # Sloped sides
            left = a + (b - a) * alpha
            right = d - (d - c) * alpha
            x.append(left)
            x_bar.append(right)

    # Plotting
    plt.figure(figsize=(10, 6))
    # Plot trapezoidal MF
    # plt.plot([a, b, c, d], [0, 1, 1, 0], label="Trapezoidal MF", color="blue", linewidth=2)
    plt.plot([a, b, c, d], [0, 1, 1, 0], label="Trapezoidal MF", color="blue", linewidth=2)
    colors = ['red', 'purple', 'orange', 'green', 'brown', 'cyan']

    for i in range(len(alpha_values)):
        color = colors[i % len(colors)]
        # Slightly extended α-cut lines
        extension = 0.05  # 5% extension
        x_len = x_bar[i] - x[i]
        x_start = x[i] - x_len * extension
        x_end = x_bar[i] + x_len * extension
        # Horizontal α-cut line
        plt.hlines(alpha_values[i], x_start, x_end, color=color, linestyles="dotted", linewidth=1.5)
        # Dots at α-cut ends
        plt.scatter([x[i], x_bar[i]], [alpha_values[i], alpha_values[i]], color="black")
        # Label formatting
        x_val_str = f"{x[i]:.{precisions[i]}f}"
        x_bar_val_str = f"{x_bar[i]:.{precisions[i]}f}"
        alpha_val_str = f"{alpha_values[i]:.{precisions[i]}f}"
        # Use smaller dynamic offset for this scale (±1 unit)
        plt.text(x[i] - 1, alpha_values[i] + 0.03, f"({x_val_str}, {alpha_val_str})", fontsize=8)
        plt.text(x_bar[i] + 1, alpha_values[i] + 0.03, f"({x_bar_val_str}, {alpha_val_str})", fontsize=8)
        # Vertical dashed lines
        plt.vlines(x[i], 0, alpha_values[i], color="green", linestyle="dashed")
        plt.vlines(x_bar[i], 0, alpha_values[i], color="green", linestyle="dashed")

    # Titles and Labels
    plt.title("Trapezoidal MF - α Cuts for " + module + " of " + material, fontsize=14)
    if(module == "Density"):
        plt.xlabel("Density (kg/m³)", fontsize=12)
    else:
        plt.xlabel("Young's Modulus (N/m²)", fontsize=12)
    plt.ylabel("Membership Degree (μ)", fontsize=12)

    # Y-axis setup
    plt.ylim(0, 1.1)
    plt.yticks([round(i * 0.2, 1) for i in range(6)] + [1.0])
    # X-axis baseline
    plt.axhline(0, color='black', linewidth=0.5, linestyle='--')
    plt.gca().spines['bottom'].set_position('zero')
    plt.gca().tick_params(axis='y', which='both', direction='out', pad=3)
    # Vertical markers at a, b, c, d
    plt.axvline(a, color='gray', linestyle="--", label="a (Min)")
    plt.axvline(b, color='gray', linestyle="--", label="b (Peak)")
    plt.axvline(c, color='gray', linestyle="--", label="c (Peak)")
    plt.axvline(d, color='gray', linestyle="--", label="d (Max)")
    plt.legend(loc='upper right')
    plt.grid(alpha=0.4)
    # plt.tight_layout()
    # plt.show()
    g = "static/img/" + g_name
    plt.savefig(g)
    plt.close() 

def GetFuzzyFunction_aplha_alpha_dash(a_val, b_val, c_val, d_val, a1, a2, a3, a4, a5, a6, g_name, material, module):
# Trapezoidal MF Parameters for Density of Aluminium (in kg/m³)
    # a, b, c, d = 2680, 2690, 2710, 2720  
    a = a_val
    b = b_val
    c = c_val
    d = d_val
    # print(a,b,c,d)
    # User Inputs
    # alpha_input = input("Enter α values (comma separated, like 0.3,0.3333,0.4567): ")
    # alpha_dash_input = input("Enter α' values (comma separated, like 0.3,0.3333,0.4567): ")
    alpha = [a1, a2, a3]
    alpha_dash = [a4, a5, a6]
    # print(alpha)
    # print(alpha_dash)
    # Convert to float
    # alpha = [float(val.strip()) for val in alpha_input.split(',')]
    # alpha_dash = [float(val.strip()) for val in alpha_dash_input.split(',')]

    # Decimal precision for labeling
    prec_alpha = [len(str(val).split('.')[-1]) if '.' in str(val) else 0 for val in alpha]
    prec_alpha_dash = [len(str(val).split('.')[-1]) if '.' in str(val) else 0 for val in alpha_dash]

    # Compute α-cut and α′-cut points
    x = [a + (b - a) * alpha[i] for i in range(len(alpha))]  # Left slope
    x_bar = [d - (d - c) * alpha_dash[i] for i in range(len(alpha_dash))]  # Right slope

    # Plot initialization
    plt.figure(figsize=(10, 6))
    plt.plot([a, b, c, d], [0, 1, 1, 0], label= "Trapezoidal MF", color="blue", linewidth=2)

    colors = ['red', 'purple', 'orange', 'green', 'brown', 'cyan']
    if material == "Aluminium":
        if(module == "Density"):
            x_extend = 3  # Horizontal extension for α–α′ lines
        else:
            x_extend = 1e9  # Large enough for visible extension
    if material == "Neoprene Rubber":
        if(module == "Density"):
            x_extend = 3  
        else:
            x_extend = 1e5  
    if material == "Teflon":
        if(module == "Density"):
            x_extend = 3  
        else:
            x_extend = 1e7  
    if material == "Nylon":
        if(module == "Density"):
            x_extend = 3  
        else:
            x_extend = 1e8
    if material == "SS-304 Grade ABS Silicon":
        if(module == "Density"):
            x_extend = 3  
        else:
            x_extend = 3e8
    else:
        if(module == "Density"):
            x_extend = 3
        else:
            # x_extend = 1e9
            x_extend = 3

    for i in range(len(alpha)):
        color = colors[i % len(colors)]
        # Draw extended slanted α–α′ line
        x_start = x[i] - x_extend
        x_end = x_bar[i] + x_extend
        plt.plot([x_start, x_end], [alpha[i], alpha_dash[i]], color=color, linestyle="--", linewidth=1.5)
        # Dots at α and α′
        plt.scatter([x[i], x_bar[i]], [alpha[i], alpha_dash[i]], color="black", zorder=5)
        # Labels at α and α′ points
        plt.text(x[i] - 1.2, alpha[i] + 0.02,
                f"({x[i]:.{prec_alpha[i]}f}, {alpha[i]:.{prec_alpha[i]}f})", fontsize=8)
        plt.text(x_bar[i] + 0.5, alpha_dash[i] + 0.02,
                f"({x_bar[i]:.{prec_alpha_dash[i]}f}, {alpha_dash[i]:.{prec_alpha_dash[i]}f})", fontsize=8)
        # Fixed vertical dashed lines from y=0 to point exactly at alpha[i] and alpha_dash[i]
        plt.vlines(x[i], 0, alpha[i], color="green", linestyle="dashed", linewidth=1)
        plt.vlines(x_bar[i], 0, alpha_dash[i], color="green", linestyle="dashed", linewidth=1)

        # Trapezoid parameter guides
    plt.axvline(a, color='gray', linestyle="--", label="a (Min)")
    plt.axvline(b, color='gray', linestyle="--", label="b (Peak)")
    plt.axvline(c, color='gray', linestyle="--", label="c (Peak)")
    plt.axvline(d, color='gray', linestyle="--", label="d (Max)")
    plt.axhline(0, color='black', linestyle='--', linewidth=0.5)

    # Axes labels and title
    # plt.title("Trapezoidal MF α–α′ Cut Plane for Density of Aluminium", fontsize=14)
    plt.title("Trapezoidal MF - α–α′ Cut for " + module + " of " + material, fontsize=14)    
    if(module == "Density"):
        plt.xlabel("Density (kg/m³)", fontsize=12)
    else:
        plt.xlabel("Young's Modulus (N/m²)", fontsize=12)
    plt.ylabel("Membership Degree (μ)", fontsize=12)
    plt.legend()
    plt.grid(alpha=0.4)
    plt.ylim(-0.05, 1.1)  # Set y-limit to just below x-axis
    plt.gca().spines['bottom'].set_position('zero')
    # plt.tight_layout()
    # plt.show()
    g = "static/img/" + g_name
    plt.savefig(g)
    plt.close() 
