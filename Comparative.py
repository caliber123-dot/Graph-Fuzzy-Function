import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from flask import send_file

# Material data: (Y_a, Y_b, Y_c, Y_d, ρ_a, ρ_b, ρ_c, ρ_d)
def Comparative_Alpha(alpha_str, graph, t1, materials):
    # materials = {
    #     'Aluminum': (6.8E10, 6.9E10, 7.1E10, 7.2E10, 2680, 2690, 2710, 2720),
    #     'Neoprene Rubber': (100000, 200000, 400000, 500000, 1250, 1260, 1290, 1300),
    #     'Teflon': (4.00e+08, 4.50e+08, 5.50e+08, 6.00e+08, 2180, 2188, 2212, 2220),
    #     'Nylon': (2.00E+09, 2.50E+09, 3.50E+09, 4.00E+09, 1050, 1075, 1125, 1150),
    #     'SS-304 Grade ABS silicon': (1.93e11, 1.95e11, 1.98e11, 2.00e11, 7900, 7915, 7945, 7960)
    # }
    # Trapezoidal α-cut bounds
    def alpha_cut(a, b, c, d, α):
        lower = a + α * (b - a)
        upper = d - α * (d - c)
        return lower, upper

    # Get α value (keep original string for display, convert to float for math)
    try:
        # alpha_str = input("Enter α between 0 and 1: ").strip()
        α = float(alpha_str)
        assert 0 <= α <= 1
    except:
        print("❌ Please enter a valid number in [0,1].")
        exit()

    # Lists to store results
    names, fn1_vals, fn2_vals, fn3_vals, fn4_vals = [], [], [], [], []

    # Frequency calculation
    def natural_freq(Y, ρ):
        return (1 / (2 * np.pi)) * np.sqrt(Y / ρ)

    # Loop over materials
    for name, (Ya, Yb, Yc, Yd, ρa, ρb, ρc, ρd) in materials.items():
        Y_l, Y_u = alpha_cut(Ya, Yb, Yc, Yd, α)
        ρ_l, ρ_u = alpha_cut(ρa, ρb, ρc, ρd, α)

        fn1 = natural_freq(Y_l, ρ_l)  # (Y̲,ρ̲)
        fn2 = natural_freq(Y_u, ρ_l)  # (Y̅,ρ̲)
        fn3 = natural_freq(Y_l, ρ_u)  # (Y̲,ρ̅)
        fn4 = natural_freq(Y_u, ρ_u)  # (Y̅,ρ̅)

        names.append(name)
        # fn1_list.append(round(fn1, 4)) # Ymin dmin 
        fn1_vals.append(round(fn1, 4))
        fn2_vals.append(round(fn2, 4))
        fn3_vals.append(round(fn3, 4))
        fn4_vals.append(round(fn4, 4))

    # Print results in table (rounded)
    df = pd.DataFrame({
        'Material': names,
        "α": str(α),
        'fn1 (Y̲,ρ̲)': fn1_vals,
        'fn2 (Y̅,ρ̲)': fn2_vals,
        'fn3 (Y̲,ρ̅)': fn3_vals,
        'fn4 (Y̅,ρ̅)': fn4_vals
    })
    # t1 : α-Cut tbl 
    export_table_image(t1, df, 1)
    # print(f"\nNatural Frequencies at α = {alpha_str} (in Hz):\n")
    # print(df.to_string(index=False, formatters={
    #     'fn1 (Y̲,ρ̲)': '{:.4f}'.format,
    #     'fn2 (Y̅,ρ̲)': '{:.4f}'.format,
    #     'fn3 (Y̲,ρ̅)': '{:.4f}'.format,
    #     'fn4 (Y̅,ρ̅)': '{:.4f}'.format
    # }))

    # Plotting bar chart
    ind = np.arange(len(names))
    bar_w = 0.2
    fig, ax = plt.subplots(figsize=(10, 5))

    ax.bar(ind - 1.5*bar_w, fn1_vals, width=bar_w, color='blue', label='fn1 (Y̲,ρ̲)')
    ax.bar(ind - 0.5*bar_w, fn2_vals, width=bar_w, color='orange', label='fn2 (Y̅,ρ̲)')
    ax.bar(ind + 0.5*bar_w, fn3_vals, width=bar_w, color='green', label='fn3 (Y̲,ρ̅)')
    ax.bar(ind + 1.5*bar_w, fn4_vals, width=bar_w, color='red', label='fn4 (Y̅,ρ̅)')

    ax.set_xticks(ind)
    ax.set_xticklabels(names, rotation=0)
    ax.set_ylabel("Natural Frequency (Hz)")
    ax.set_title(f"Comparative Natural Frequencies Using Trapezoidal Fuzzy Numbers α = {alpha_str}")
    ax.grid(axis='y', linestyle='--', alpha=0.6)
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1))

    plt.tight_layout()
    # plt.show()
    g = "static/img/" + graph
    plt.savefig(g)
    plt.close()  # Close the figure to free up memory

def export_table_image(g_name, df, status):
    # if alpha_dash_cuts is not None:
    #     alpha_dash_alpha = [f"{a}-{b}" for a, b in zip(alpha_cuts, alpha_dash_cuts)]
    # alpha_cuts = alpha_cut    
    df = df
    
    # Reset index and pass only values without index
    if status == 1 :
        fig, ax = plt.subplots(figsize=(9, 2.8))
    else:
        fig, ax = plt.subplots(figsize=(10, 2.8))
    ax.axis('off')

    # Add centered title
    # plt.title(alpha, fontsize=10, weight='bold', pad=4)

    # Create table without index column
    tbl = ax.table(
        cellText=df.values,
        colLabels=df.columns,
        cellLoc='center',
        loc='center'
    )
    # Format table
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(12)
    tbl.scale(1.2, 1.5)  # Makes cells larger for padding effect

    # Eliminate extra space
    # plt.subplots_adjust(left=0.01, right=0.99, top=0.75, bottom=0.05)

    # Optional: adjust cell size manually (finer control)
    # for (row, col), cell in tbl.get_celld().items():
    #     cell.set_height(0.22)
    #     cell.set_width(0.18)
    # Adjust cell size: first column is double width
    for (row, col), cell in tbl.get_celld().items():
        cell.set_height(0.22)
        if col == 0:
            cell.set_width(0.36)  # Double width
        else:
            cell.set_width(0.18)  # Regular width
    
    plt.tight_layout()        
    # g_path = os.path.join("static", "img", g_name)
    g_path =  "static/img/" + g_name
    plt.savefig(g_path, bbox_inches='tight', dpi=200)
    # plt.savefig(g_path, bbox_inches='tight', pad_inches=0.02, dpi=200)
    plt.close(fig)
    # Return the file for download
    return send_file(
        g_path,
        download_name=g_name,
        as_attachment=True,
        mimetype='image/png'
    )

# alpha dash α-α'
def Comparative_Alpha_Dash(alpha, alpha_dash, graph, t1, materials):
# Trapezoidal (a, b, c, d) values for Young's Modulus and Density
    # materials = {
    #     'Aluminum': (6.8E10, 6.9E10, 7.1E10, 7.2E10, 2680, 2690, 2710, 2720),
    #     'Neoprene Rubber': (100000, 200000, 400000, 500000, 1250, 1260, 1290, 1300),
    #     'Teflon': (4.00e+08, 4.50e+08, 5.50e+08, 6.00e+08, 2180, 2188, 2212, 2220),
    #     'Nylon': (2.00E+09, 2.50E+09, 3.50E+09, 4.00E+09, 1050, 1075, 1125, 1150),
    #     'SS-304 Grade ABS silicon': (1.93e11, 1.95e11, 1.98e11, 2.00e11, 7900, 7915, 7945, 7960)
    # }

    # α and α′ input from user
    alpha_input = alpha
    alpha_prime_input = alpha_dash

    alpha = [float(x) for x in alpha_input.split(',')]
    alpha_prime = [float(x) for x in alpha_prime_input.split(',')]

    if len(alpha) != len(alpha_prime):
        raise ValueError("❌ α and α′ lists must have the same length.")

    rows = []
    for material, (Ya, Yb, Yc, Yd, ρa, ρb, ρc, ρd) in materials.items():
        for α, αp in zip(alpha, alpha_prime):
            # α-cut bounds
            Y_lower = Ya + α * (Yb - Ya)
            Y_upper = Yd - αp * (Yd - Yc)
            rho_lower = ρa + α * (ρb - ρa)
            rho_upper = ρd - αp * (ρd - ρc)

            # Frequencies
            fn1 = (1 / (2 * np.pi)) * np.sqrt(Y_lower / rho_lower)
            fn2 = (1 / (2 * np.pi)) * np.sqrt(Y_upper / rho_lower)
            fn3 = (1 / (2 * np.pi)) * np.sqrt(Y_lower / rho_upper)
            fn4 = (1 / (2 * np.pi)) * np.sqrt(Y_upper / rho_upper)

            rows.append({
                "Material": material,
                "α": str(α),
                "α′": str(αp),
                # "α-α′": f"{float(α)}-{float(αp)}",
                "fn1 (Y̲,ρ̲)": round(fn1, 4),
                "fn2 (Y̅,ρ̲)": round(fn2, 4),
                "fn3 (Y̲,ρ̅)": round(fn3, 4),
                "fn4 (Y̅,ρ̅)": round(fn4, 4)
            })

    # Display results with 4 decimal places
    df = pd.DataFrame(rows)

    export_table_image(t1, df, 2)
    # print("\nComparative Natural Frequency Table (in Hz):")
    # print(df.to_string(index=False))

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 5))
    bar_width = 0.15
    index = np.arange(len(df))

    ax.bar(index, df["fn1 (Y̲,ρ̲)"], bar_width, label='fn1 (Y̲,ρ̲)')
    ax.bar(index + bar_width, df["fn2 (Y̅,ρ̲)"], bar_width, label='fn2 (Y̅,ρ̲)')
    ax.bar(index + 2 * bar_width, df["fn3 (Y̲,ρ̅)"], bar_width, label='fn3 (Y̲,ρ̅)')
    ax.bar(index + 3 * bar_width, df["fn4 (Y̅,ρ̅)"], bar_width, label='fn4 (Y̅,ρ̅)')

    # X-axis labels
    ax.set_xticks(index + 1.5 * bar_width)
    # ax.set_xticklabels([f"{row['Material']} ({row['α']},{row['α′']})" for _, row in df.iterrows()],
    #                    rotation=45, ha='right')
    # ax.set_xticklabels([f"{row['Material']}" for _, row in df.iterrows()], rotation=0)
    ax.set_xticklabels([f"{row['Material']}\n({row['α']}, {row['α′']})" for _, row in df.iterrows()])

    ax.set_ylabel("Natural Frequency (Hz)")
    ax.set_title(f"Comparative Natural Frequencies Using Trapezoidal Fuzzy Numbers (α = {alpha_input} , α′ = {alpha_prime_input})")
    ax.grid(axis='y', linestyle='--', alpha=0.6)
    ax.legend()

    plt.tight_layout()
    # plt.show()
    g = "static/img/" + graph
    plt.savefig(g)
    plt.close()  # Close the figure to free up memory
