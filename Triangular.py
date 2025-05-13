import matplotlib
matplotlib.use('Agg')  # Set the backend to Agg
import matplotlib.pyplot as plt

def GetFuzzyFunction_aplha2(a_val, b_val, c_val, a1, a2, a3, g_name, material, module):
    # Triangular Membership Function Points (Young's Modulus for Aluminium)
    a, b, c = a_val, b_val, c_val    
    # alpha_values = [0.35, 0.45, 0.56]
    alpha_values = [a1, a2, a3]
    # Precision for formatting labels
    precisions = [len(str(x).split('.')[-1]) if '.' in str(x) else 0 for x in alpha_values]
    # Calculate α-cut points
    x = [a + (b - a) * α for α in alpha_values]
    x_bar = [c - (c - b) * α for α in alpha_values]
    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot([a, b, c], [0, 1, 0], label="Triangular MF", color="blue", linewidth=2)
    colors = ['red', 'purple', 'orange', 'green', 'brown', 'cyan']
    for i in range(len(alpha_values)):
        color = colors[i % len(colors)]
        # Adjusted length of α-cut line
        extension = 0.05  # 5% of the line length for slight extension
        x_len = x_bar[i] - x[i]
        x_start = x[i] - x_len * extension
        x_end = x_bar[i] + x_len * extension
        # Draw α-cut line
        plt.hlines(alpha_values[i], x_start, x_end, color=color, linestyles="dotted", linewidth=1.5)
        # Black dots at actual α-cut points
        plt.scatter([x[i], x_bar[i]], [alpha_values[i], alpha_values[i]], color="black")
        # Label formatting
        x_val_str = f"{x[i]:.{precisions[i]}f}"
        x_bar_val_str = f"{x_bar[i]:.{precisions[i]}f}"
        alpha_val_str = f"{alpha_values[i]:.{precisions[i]}f}"
        # plt.text(x[i] - 1e8, alpha_values[i] + 0.03, f"({x_val_str}, {alpha_val_str})", fontsize=8)
        # plt.text(x_bar[i] + 1e8, alpha_values[i] + 0.03, f"({x_bar_val_str}, {alpha_val_str})", fontsize=8)
        # Vertical dashed lines from base to dot
        # Text near each black dot
        plt.text(x[i] - 1, alpha_values[i] + 0.03, f"({x_val_str}, {alpha_val_str})", fontsize=8)
        plt.text(x_bar[i] + 1, alpha_values[i] + 0.03, f"({x_bar_val_str}, {alpha_val_str})", fontsize=8)

        # Vertical lines from 0 to the black dots
        plt.vlines(x[i], 0, alpha_values[i], color="green", linestyle="dashed")
        plt.vlines(x_bar[i], 0, alpha_values[i], color="green", linestyle="dashed")

    # Title and labels
    # plt.title("Triangular MF - α Cuts for Young's Modulus of Aluminium", fontsize=14)
    plt.title("Triangular MF - α Cuts for " + module + " of " + material, fontsize=14)
    if(module == "Density"):
        plt.xlabel("Density (kg/m³)", fontsize=12)
    else:
        plt.xlabel("Young's Modulus (N/m²)", fontsize=12)
    plt.ylabel("Membership Degree (μ)", fontsize=12)
    
     # Y-axis setup: from 0 to 1 with ticks at 0.2 steps
    plt.ylim(0, 1)
    plt.yticks([round(i * 0.2, 1) for i in range(6)])  # [0.0, 0.2, ..., 1.0]

    # X-axis and base setup
    plt.axhline(0, color='black', linewidth=0.5, linestyle='--')
    plt.gca().spines['bottom'].set_position('zero')
    plt.gca().tick_params(axis='y', which='both', direction='out', pad=3)

    # Vertical markers at a, b, c
    plt.axvline(a, color='gray', linestyle="--", label="a (Min)")
    plt.axvline(b, color='gray', linestyle="--", label="b (Peak)")
    plt.axvline(c, color='gray', linestyle="--", label="c (Max)")

    plt.legend()
    plt.grid(alpha=0.4)
    # plt.tight_layout()
    # plt.show()
    g = "static/img/" + g_name
    plt.savefig(g)
    plt.close() 

def GetFuzzyFunction_aplha_alpha_dash2(a_val, b_val, c_val, a1, a2, a3, a4, a5, a6, g_name, material, module):
    # Triangular Membership Function Points (Young's Modulus for Aluminium)
    # a, b, c = 68947600000, 74456800000, 79966000000
    a, b, c = a_val, b_val, c_val    
    # User input
    # alpha_input = input("Enter α values (comma separated, e.g. 0.3001, 0.4002, 0.5003): ")
    # alpha_dash_input = input("Enter α' values (comma separated, e.g. 0.3501, 0.4802, 0.5403): ")
    # alpha = [float(x.strip()) for x in alpha_input.split(',')]
    # alpha_dash = [float(x.strip()) for x in alpha_dash_input.split(',')]
    alpha = [a1, a2, a3]
    alpha_dash = [a4, a5, a6]
    # Precision handling for formatted label display
    prec_alpha = [len(str(x).split('.')[-1]) if'.' in str(x) else 0 for x in alpha]
    prec_alpha_dash = [len(str(x).split('.')[-1]) if '.' in str(x) else 0 for x in alpha_dash]

    # Calculate α cut lower bounds and α′ cut upper bounds
    x = [a + (b - a) * alpha[i] for i in range(len(alpha))]
    x_bar = [c - (c - b) * alpha_dash[i] for i in range(len(alpha_dash))]

    # Margin to extend lines left and right
    # x_extend = 1e9  # Large enough for visible extension
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

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot([a, b, c], [0, 1, 0], label="Triangular MF", color="blue", linewidth=2)
    colors = ['red', 'purple', 'orange', 'green', 'brown', 'cyan']

    for i in range(len(alpha)):
        color = colors[i % len(colors)]
        # Extended line beyond actual cut points
        x_start = x[i] - x_extend
        x_end = x_bar[i] + x_extend
        # Draw extended slanted α–α′ cut line
        plt.plot([x_start, x_end], [alpha[i], alpha_dash[i]],
        color=color, linestyle="--", linewidth=1.5)
        # Draw dots at actual cut positions
        plt.scatter([x[i], x_bar[i]], [alpha[i], alpha_dash[i]], color="black")
        # Labels at actual cut points
        plt.text(x[i] - 1.2, alpha[i] + 0.02,
        f"({x[i]:.{prec_alpha[i]}f}, {alpha[i]:.{prec_alpha[i]}f})", fontsize=8)
        plt.text(x_bar[i] + 0.5, alpha_dash[i] + 0.02,
        f"({x_bar[i]:.{prec_alpha_dash[i]}f}, {alpha_dash[i]:.{prec_alpha_dash[i]}f})", fontsize=8)
        # Vertical dashed lines at actual points
        plt.vlines(x[i], 0, alpha[i], color="green", linestyle="dashed", linewidth=1)
        plt.vlines(x_bar[i], 0, alpha_dash[i], color="green", linestyle="dashed", linewidth=1)

    # Labels and formatting
    # plt.title("Triangular MF α – α′ Cut Plane for Young's Modulus of Aluminium", fontsize=14)
    plt.title("Triangular MF - α–α′ Cut for " + module + " of " + material, fontsize=14)    
    if(module == "Density"):
        plt.xlabel("Density (kg/m³)", fontsize=12)
    else:
        plt.xlabel("Young's Modulus (N/m²)", fontsize=12)
    plt.ylabel("Membership Degree (μ)", fontsize=12)

    plt.axhline(0, color='black', linewidth=0.5, linestyle='--')
    plt.axvline(a, color='gray', linestyle="--", label="a (Min)")
    plt.axvline(b, color='gray', linestyle="--", label="b (Peak)")
    plt.axvline(c, color='gray', linestyle="--", label="c (Max)")

    plt.legend()
    plt.grid(alpha=0.4)
    plt.gca().spines['bottom'].set_position('zero')
    plt.gca().tick_params(axis='y', which='both', direction='out', pad=3)
    # plt.tight_layout()
    # plt.show()
    g = "static/img/" + g_name
    plt.savefig(g)
    plt.close() 


def Getapha_dash2Test():
    a, b, c = 68947600000, 74456800000, 79966000000
    # User input
    # alpha_input = input("Enter α values (comma separated, e.g. 0.3001, 0.4002, 0.5003): ")
    # alpha_dash_input = input("Enter α' values (comma separated, e.g. 0.3501, 0.4802, 0.5403): ")

    # alpha = [float(x.strip()) for x in alpha_input.split(',')]
    # alpha_dash = [float(x.strip()) for x in alpha_dash_input.split(',')]

    # Precision handling for formatted label display
    prec_alpha = [len(str(x).split('.')[-1]) if'.' in str(x) else 0 for x in alpha]
    prec_alpha_dash = [len(str(x).split('.')[-1]) if '.' in str(x) else 0 for x in alpha_dash]

    # Calculate α cut lower bounds and α′ cut upper bounds
    x = [a + (b - a) * alpha[i] for i in range(len(alpha))]
    x_bar = [c - (c - b) * alpha_dash[i] for i in range(len(alpha_dash))]

    # Margin to extend lines left and right
    x_extend = 1e9  # Large enough for visible extension

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot([a, b, c], [0, 1, 0], label="Triangular MF", color="blue", linewidth=2)

    colors = ['red', 'purple', 'orange', 'green', 'brown', 'cyan']

    for i in range(len(alpha)):
        color = colors[i % len(colors)]

    # Extended line beyond actual cut points
        x_start = x[i] - x_extend
        x_end = x_bar[i] + x_extend

    # Draw extended slanted α–α′ cut line
        plt.plot([x_start, x_end], [alpha[i], alpha_dash[i]],
        color=color, linestyle="--", linewidth=1.5)

        # Draw dots at actual cut positions
        plt.scatter([x[i], x_bar[i]], [alpha[i], alpha_dash[i]], color="black")

        # Labels at actual cut points
        plt.text(x[i] - 0.3e9, alpha[i] + 0.02,
        f"({x[i]:.{prec_alpha[i]}f}, {alpha[i]:.{prec_alpha[i]}f})", fontsize=8)
        plt.text(x_bar[i] + 0.3e9, alpha_dash[i] + 0.02,
        f"({x_bar[i]:.{prec_alpha_dash[i]}f}, {alpha_dash[i]:.{prec_alpha_dash[i]}f})", fontsize=8)

        # Vertical dashed lines at actual points
        plt.vlines(x[i], 0, alpha[i], color="green", linestyle="dashed", linewidth=1)
        plt.vlines(x_bar[i], 0, alpha_dash[i], color="green", linestyle="dashed", linewidth=1)

    # Labels and formatting
    plt.title("Triangular MF α – α′ Cut Plane for Young's Modulus of Aluminium", fontsize=14)
    plt.xlabel("Young's Modulus (N/m²)", fontsize=12)
    plt.ylabel("Membership Degree (μ)", fontsize=12)

    plt.axhline(0, color='black', linewidth=0.5, linestyle='--')
    plt.axvline(a, color='gray', linestyle="--", label="a (Min)")
    plt.axvline(b, color='gray', linestyle="--", label="b (Peak)")
    plt.axvline(c, color='gray', linestyle="--", label="c (Max)")

    plt.legend()
    plt.grid(alpha=0.4)
    plt.gca().spines['bottom'].set_position('zero')
    plt.gca().tick_params(axis='y', which='both', direction='out', pad=3)
    plt.tight_layout()
    plt.show()
