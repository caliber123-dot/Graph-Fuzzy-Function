import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from flask import send_file

# Material data: (Y_a, Y_b, Y_c, Y_d, ρ_a, ρ_b, ρ_c, ρ_d)
def Comparative_Alpha(alpha_str, graph, t1, materials):    
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

        # fn1 = natural_freq(Y_l, ρ_l)  # (Y̲,ρ̲)
        # fn2 = natural_freq(Y_u, ρ_l)  # (Y̅,ρ̲)
        # fn3 = natural_freq(Y_l, ρ_u)  # (Y̲,ρ̅)
        # fn4 = natural_freq(Y_u, ρ_u)  # (Y̅,ρ̅)
        # Calculate frequencies and format to 4 decimal places
        fn1 = float(f"{natural_freq(Y_l, ρ_l):.4f}")
        fn2 = float(f"{natural_freq(Y_u, ρ_l):.4f}")
        fn3 = float(f"{natural_freq(Y_l, ρ_u):.4f}")
        fn4 = float(f"{natural_freq(Y_u, ρ_u):.4f}")

        names.append(name)
        # fn1_list.append(round(fn1, 4)) # Ymin dmin 
        fn1_vals.append(fn1)
        fn2_vals.append(fn2)
        fn3_vals.append(fn3)
        fn4_vals.append(fn4)

    # Print results in table (rounded)
    df = pd.DataFrame({
        'Material': names,
        "α": str(α),
        'fn1 (Y̲,ρ̲)': [f"{x:.4f}" for x in fn1_vals],
        'fn2 (Y̅,ρ̲)': [f"{x:.4f}" for x in fn2_vals],
        'fn3 (Y̲,ρ̅)': [f"{x:.4f}" for x in fn3_vals],
        'fn4 (Y̅,ρ̅)': [f"{x:.4f}" for x in fn4_vals]
    })
    # t1 : α-Cut tbl 
    export_table_image(t1, df, 1)
    
    fn_dict = {
        'Material': names,
        "α": str(α),
        "fn1": [f"{x:.4f}" for x in fn1_vals],
        "fn2": [f"{x:.4f}" for x in fn2_vals],
        "fn3": [f"{x:.4f}" for x in fn3_vals],
        "fn4": [f"{x:.4f}" for x in fn4_vals]
    }

    # Plotting bar chart
    ind = np.arange(len(names))
    bar_w = 0.2
    fig, ax = plt.subplots(figsize=(11, 6))

    # ax.bar(ind - 1.5*bar_w, fn1_vals, width=bar_w, color='blue', label='fn1 (Y̲,ρ̲)')
    # ax.bar(ind - 0.5*bar_w, fn2_vals, width=bar_w, color='orange', label='fn2 (Y̅,ρ̲)')
    # ax.bar(ind + 0.5*bar_w, fn3_vals, width=bar_w, color='green', label='fn3 (Y̲,ρ̅)')
    # ax.bar(ind + 1.5*bar_w, fn4_vals, width=bar_w, color='red', label='fn4 (Y̅,ρ̅)')
    bars1 = ax.bar(ind - 1.5*bar_w, fn1_vals, width=bar_w, color='blue', label='fn1 (Y̲,ρ̲)')
    bars2 = ax.bar(ind - 0.5*bar_w, fn2_vals, width=bar_w, color='orange', label='fn2 (Y̅,ρ̲)')
    bars3 = ax.bar(ind + 0.5*bar_w, fn3_vals, width=bar_w, color='green', label='fn3 (Y̲,ρ̅)')
    bars4 = ax.bar(ind + 1.5*bar_w, fn4_vals, width=bar_w, color='red', label='fn4 (Y̅,ρ̅)')

    # Annotate bars
    
    def annotate_bars(bars, fontsize=7, rotation=90, y_offset=5):
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height + y_offset,
                f'{height:.4f}',
                ha='center', va='bottom',
                fontsize=fontsize,
                rotation=rotation
            )
    annotate_bars(bars1)
    annotate_bars(bars2)
    annotate_bars(bars3)
    annotate_bars(bars4)

    ax.set_xticks(ind)
    ax.set_xticklabels(names, rotation=0)
    # ax.set_xticklabels(names, rotation=15, ha='right')
    # ax.set_ylim(0, 900)
    ax.set_ylim(0, max(fn1_vals + fn2_vals + fn3_vals + fn4_vals) * 1.1)
    ax.set_ylabel("Natural Frequency (Hz)")
    ax.set_title(f"Comparative Natural Frequencies Using Trapezoidal Fuzzy Numbers α = {alpha_str}")
    ax.grid(axis='y', linestyle='--', alpha=0.6)
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1))

    plt.tight_layout()
    # plt.show()
    g = "static/img/" + graph
    plt.savefig(g)
    plt.close()  # Close the figure to free up memory
    return fn_dict

def Comparative_Alpha_Triangular(alpha_str, graph, t1, materials):
    # Trapezoidal α-cut bounds
    # print(materials)
    def alpha_cut(a, b, c, d, α):
        lower = a + α * (b - a)
        upper = c - α * (c - b)
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

        # Calculate frequencies and format to 4 decimal places
        fn1 = float(f"{natural_freq(Y_l, ρ_l):.4f}")
        fn2 = float(f"{natural_freq(Y_u, ρ_l):.4f}")
        fn3 = float(f"{natural_freq(Y_l, ρ_u):.4f}")
        fn4 = float(f"{natural_freq(Y_u, ρ_u):.4f}")

        names.append(name)
        # fn1_list.append(round(fn1, 4)) # Ymin dmin 
        fn1_vals.append(fn1)
        fn2_vals.append(fn2)
        fn3_vals.append(fn3)
        fn4_vals.append(fn4)

    # Print results in table (rounded)
    df = pd.DataFrame({
        'Material': names,
        "α": str(α),
        'fn1 (Y̲,ρ̲)': [f"{x:.4f}" for x in fn1_vals],
        'fn2 (Y̅,ρ̲)': [f"{x:.4f}" for x in fn2_vals],
        'fn3 (Y̲,ρ̅)': [f"{x:.4f}" for x in fn3_vals],
        'fn4 (Y̅,ρ̅)': [f"{x:.4f}" for x in fn4_vals]
    })
    # t1 : α-Cut tbl 
    export_table_image(t1, df, 1)
    fn_dict = {
        'Material': names,
        "α": str(α),
        "fn1": [f"{x:.4f}" for x in fn1_vals],
        "fn2": [f"{x:.4f}" for x in fn2_vals],
        "fn3": [f"{x:.4f}" for x in fn3_vals],
        "fn4": [f"{x:.4f}" for x in fn4_vals]
    }
    # Plotting bar chart
    ind = np.arange(len(names))
    bar_w = 0.2
    fig, ax = plt.subplots(figsize=(11, 6))
    
    bars1 = ax.bar(ind - 1.5*bar_w, fn1_vals, width=bar_w, color='blue', label='fn1 (Y̲,ρ̲)')
    bars2 = ax.bar(ind - 0.5*bar_w, fn2_vals, width=bar_w, color='orange', label='fn2 (Y̅,ρ̲)')
    bars3 = ax.bar(ind + 0.5*bar_w, fn3_vals, width=bar_w, color='green', label='fn3 (Y̲,ρ̅)')
    bars4 = ax.bar(ind + 1.5*bar_w, fn4_vals, width=bar_w, color='red', label='fn4 (Y̅,ρ̅)')
    
    def annotate_bars(bars, fontsize=7, rotation=90, y_offset=5):
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height + y_offset,
                f'{height:.4f}',
                ha='center', va='bottom',
                fontsize=fontsize,
                rotation=rotation
            )
    annotate_bars(bars1)
    annotate_bars(bars2)
    annotate_bars(bars3)
    annotate_bars(bars4)

    ax.set_xticks(ind)
    ax.set_xticklabels(names, rotation=0)
    # ax.set_xticklabels(names, rotation=15, ha='right')
    # ax.set_ylim(0, 900)
    ax.set_ylim(0, max(fn1_vals + fn2_vals + fn3_vals + fn4_vals) * 1.1)
    ax.set_ylabel("Natural Frequency (Hz)")
    ax.set_title(f"Comparative Natural Frequencies Using Triangular Fuzzy Numbers α = {alpha_str}")
    ax.grid(axis='y', linestyle='--', alpha=0.6)
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1))

    plt.tight_layout()
    # plt.show()
    g = "static/img/" + graph
    plt.savefig(g)
    plt.close()  # Close the figure to free up memory
    return fn_dict


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
    # α and α′ input from user
    alpha_input = alpha
    alpha_prime_input = alpha_dash

    alpha = [float(x) for x in alpha_input.split(',')]
    alpha_prime = [float(x) for x in alpha_prime_input.split(',')]

    if len(alpha) != len(alpha_prime):
        raise ValueError("❌ α and α′ lists must have the same length.")

    names, fn1_vals, fn2_vals, fn3_vals, fn4_vals = [], [], [], [], []
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

            names.append(material)
            fn1_vals.append(fn1)
            fn2_vals.append(fn2)
            fn3_vals.append(fn3)
            fn4_vals.append(fn4)

            rows.append({
                "Material": material,
                "α": str(α),
                "α′": str(αp),
                # "α-α′": f"{float(α)}-{float(αp)}",
                "fn1 (Y̲,ρ̲)": f"{fn1:.4f}",
                "fn2 (Y̅,ρ̲)": f"{fn2:.4f}",
                "fn3 (Y̲,ρ̅)": f"{fn3:.4f}", 
                "fn4 (Y̅,ρ̅)": f"{fn4:.4f}"
            })

    # Display results with 4 decimal places
    df = pd.DataFrame(rows)
    export_table_image(t1, df, 2)
    # print("\nComparative Natural Frequency Table (in Hz):")
    # print(df.to_string(index=False))
    fn_dict = {
        'Material': names,
        "α": str(α),
        "α′": str(αp),
        "fn1": [f"{x:.4f}" for x in fn1_vals],
        "fn2": [f"{x:.4f}" for x in fn2_vals],
        "fn3": [f"{x:.4f}" for x in fn3_vals],
        "fn4": [f"{x:.4f}" for x in fn4_vals]
    }

    # Plotting
    fig, ax = plt.subplots(figsize=(11, 6))
    bar_width = 0.15
    index = np.arange(len(df))

    bars1 = ax.bar(index, df["fn1 (Y̲,ρ̲)"].astype(float), bar_width, label='fn1 (Y̲,ρ̲)')
    bars2 = ax.bar(index + bar_width, df["fn2 (Y̅,ρ̲)"].astype(float), bar_width, label='fn2 (Y̅,ρ̲)')
    bars3 = ax.bar(index + 2 * bar_width, df["fn3 (Y̲,ρ̅)"].astype(float), bar_width, label='fn3 (Y̲,ρ̅)')
    bars4 = ax.bar(index + 3 * bar_width, df["fn4 (Y̅,ρ̅)"].astype(float), bar_width, label='fn4 (Y̅,ρ̅)')

    # Annotate each bar
    def annotate_bars(bars, fontsize=7, rotation=90, y_offset=5):
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height + y_offset,
                f'{height:.4f}',
                ha='center', va='bottom',
                fontsize=fontsize,
                rotation=rotation
            )
    annotate_bars(bars1)
    annotate_bars(bars2)
    annotate_bars(bars3)
    annotate_bars(bars4)

    # X-axis labels
    ax.set_xticks(index + 1.5 * bar_width)
    # ax.set_xticklabels([f"{row['Material']} ({row['α']},{row['α′']})" for _, row in df.iterrows()],
    #                    rotation=45, ha='right')
    # ax.set_xticklabels([f"{row['Material']}" for _, row in df.iterrows()], rotation=0)
    ax.set_xticklabels([f"{row['Material']}\n({row['α']}, {row['α′']})" for _, row in df.iterrows()])
    # ax.set_ylim(0, max(fn1_vals + fn2_vals + fn3_vals + fn4_vals) * 1.1)
    all_vals = pd.concat([df["fn1 (Y̲,ρ̲)"], df["fn2 (Y̅,ρ̲)"], df["fn3 (Y̲,ρ̅)"], df["fn4 (Y̅,ρ̅)"]]).astype(float)
    ax.set_ylim(0, all_vals.max() * 1.1)
    ax.set_ylabel("Natural Frequency (Hz)")
    ax.set_title(f"Comparative Natural Frequencies Using Trapezoidal Fuzzy Numbers (α = {alpha_input} , α′ = {alpha_prime_input})")
    ax.grid(axis='y', linestyle='--', alpha=0.6)
    ax.legend()

    plt.tight_layout()
    # plt.show()
    g = "static/img/" + graph
    plt.savefig(g)
    plt.close()  # Close the figure to free up memory
    return fn_dict

def Comparative_Alpha_Dash_Triangular(alpha, alpha_dash, graph, t1, materials):
    # α and α′ input from user
    alpha_input = alpha
    alpha_prime_input = alpha_dash

    alpha = [float(x) for x in alpha_input.split(',')]
    alpha_prime = [float(x) for x in alpha_prime_input.split(',')]

    if len(alpha) != len(alpha_prime):
        raise ValueError("❌ α and α′ lists must have the same length.")
    
    names, fn1_vals, fn2_vals, fn3_vals, fn4_vals = [], [], [], [], []
    rows = []
    for material, (Ya, Yb, Yc, Yd, ρa, ρb, ρc, ρd) in materials.items():
        for α, αp in zip(alpha, alpha_prime):
            # α-cut bounds
            Y_lower = Ya + α * (Yb - Ya)
            Y_upper = Yc - αp * (Yc - Yb)
            rho_lower = ρa + α * (ρb - ρa)
            rho_upper = ρc - αp * (ρc - ρb)

            # Frequencies
            fn1 = (1 / (2 * np.pi)) * np.sqrt(Y_lower / rho_lower)
            fn2 = (1 / (2 * np.pi)) * np.sqrt(Y_upper / rho_lower)
            fn3 = (1 / (2 * np.pi)) * np.sqrt(Y_lower / rho_upper)
            fn4 = (1 / (2 * np.pi)) * np.sqrt(Y_upper / rho_upper)

            names.append(material)
            fn1_vals.append(fn1)
            fn2_vals.append(fn2)
            fn3_vals.append(fn3)
            fn4_vals.append(fn4)

            rows.append({
                "Material": material,
                "α": str(α),
                "α′": str(αp),
                # "α-α′": f"{float(α)}-{float(αp)}",
                "fn1 (Y̲,ρ̲)": f"{fn1:.4f}",
                "fn2 (Y̅,ρ̲)": f"{fn2:.4f}",
                "fn3 (Y̲,ρ̅)": f"{fn3:.4f}", 
                "fn4 (Y̅,ρ̅)": f"{fn4:.4f}"
            })

    # Display results with 4 decimal places
    df = pd.DataFrame(rows)

    export_table_image(t1, df, 2)
    # print("\nComparative Natural Frequency Table (in Hz):")
    # print(df.to_string(index=False))
    fn_dict = {
        'Material': names,
        "α": str(α),
        "α′": str(αp),
        "fn1": [f"{x:.4f}" for x in fn1_vals],
        "fn2": [f"{x:.4f}" for x in fn2_vals],
        "fn3": [f"{x:.4f}" for x in fn3_vals],
        "fn4": [f"{x:.4f}" for x in fn4_vals]
    }

    # Plotting
    fig, ax = plt.subplots(figsize=(11, 6))
    bar_width = 0.15
    index = np.arange(len(df))

    bars1 = ax.bar(index, df["fn1 (Y̲,ρ̲)"].astype(float), bar_width, label='fn1 (Y̲,ρ̲)')
    bars2 = ax.bar(index + bar_width, df["fn2 (Y̅,ρ̲)"].astype(float), bar_width, label='fn2 (Y̅,ρ̲)')
    bars3 = ax.bar(index + 2 * bar_width, df["fn3 (Y̲,ρ̅)"].astype(float), bar_width, label='fn3 (Y̲,ρ̅)')
    bars4 = ax.bar(index + 3 * bar_width, df["fn4 (Y̅,ρ̅)"].astype(float), bar_width, label='fn4 (Y̅,ρ̅)')

    # Annotate each bar
    def annotate_bars(bars, fontsize=7, rotation=90, y_offset=5):
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height + y_offset,
                f'{height:.4f}',
                ha='center', va='bottom',
                fontsize=fontsize,
                rotation=rotation
            )
    annotate_bars(bars1)
    annotate_bars(bars2)
    annotate_bars(bars3)
    annotate_bars(bars4)

    # X-axis labels
    ax.set_xticks(index + 1.5 * bar_width)
    # ax.set_xticklabels([f"{row['Material']} ({row['α']},{row['α′']})" for _, row in df.iterrows()],
    #                    rotation=45, ha='right')
    # ax.set_xticklabels([f"{row['Material']}" for _, row in df.iterrows()], rotation=0)
    ax.set_xticklabels([f"{row['Material']}\n({row['α']}, {row['α′']})" for _, row in df.iterrows()])
    # ax.set_ylim(0, max(fn1_vals + fn2_vals + fn3_vals + fn4_vals) * 1.1)
    all_vals = pd.concat([df["fn1 (Y̲,ρ̲)"], df["fn2 (Y̅,ρ̲)"], df["fn3 (Y̲,ρ̅)"], df["fn4 (Y̅,ρ̅)"]]).astype(float)
    ax.set_ylim(0, all_vals.max() * 1.1)
    ax.set_ylabel("Natural Frequency (Hz)")
    ax.set_title(f"Comparative Natural Frequencies Using Triangular Fuzzy Numbers (α = {alpha_input} , α′ = {alpha_prime_input})")
    ax.grid(axis='y', linestyle='--', alpha=0.6)
    ax.legend()

    plt.tight_layout()
    # plt.show()
    g = "static/img/" + graph
    plt.savefig(g)
    plt.close()  # Close the figure to free up memory
    return fn_dict
