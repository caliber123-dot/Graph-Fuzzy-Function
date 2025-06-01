# Define parameters for the triangular function
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from flask import send_file
# For Alpha Cuts
def GetFunsTriangular(alpha_cuts,a_y,b_y,c_y,a_d,b_d,c_d):
    # print('Young modulus:')
    # a, b, c = 68947600000, 74456800000, 79966000000  # Young's modulus 
    a, b, c = a_y, b_y, c_y  # Young's modulus 
     
    Y_min_list = []
    Y_max_list = []
    for alpha in alpha_cuts:
        Y_min = a + (b - a) * alpha
        Y_max = c - (c - b) * alpha 
        Y_min_list.append(Y_min)
        Y_max_list.append(Y_max)

    # a2, b2, c2 = 2680, 2700, 2720      # Density (kg/m³)
    a2, b2, c2 = a_d, b_d, c_d      # Density (kg/m³)
    
    d_min_list = []
    d_max_list = []
    for alpha in alpha_cuts:
        d_min = a2 + (b2 - a2) * alpha
        d_max = c2 - (c2 - b2) * alpha 
        d_min_list.append(d_min)
        d_max_list.append(d_max)
    fn1_list = [] 
    fn2_list = [] 
    fn3_list = [] 
    fn4_list = []  
    for i in range(3):    
        fn1 = (1/(2*3.14)) * math.sqrt(Y_min_list[i]/d_min_list[i])         
        fn2 = (1/(2*3.14)) * math.sqrt(Y_max_list[i]/d_min_list[i])
        fn3 = (1/(2*3.14)) * math.sqrt(Y_min_list[i]/d_max_list[i])
        fn4 = (1/(2*3.14)) * math.sqrt(Y_max_list[i]/d_max_list[i])
    
        fn1_list.append(round(fn1, 4)) # Ymin dmin 
        fn2_list.append(round(fn2, 4)) # Ymax dmin
        fn3_list.append(round(fn3, 4)) # Ymin dmax
        fn4_list.append(round(fn4, 4)) # Ymax dmax

    print("Function 1 :",fn1_list)
    print("Function 2 :",fn2_list)
    print("Function 3 :",fn3_list)
    print("Function 4 :",fn4_list)    
    fn_dict = {
        'α': alpha_cuts,
        "fn1": fn1_list,
        "fn2": fn2_list,
        "fn3": fn3_list,
        "fn4": fn4_list
    }
    return fn_dict
# For Alpha dash
def GetFunsTriangular2(alpha_cuts,alpha_dash_cuts,a_y,b_y,c_y,a_d,b_d,c_d):
    # --- Fixed triangular‑MF parameters ---
    # Young's modulus bounds (Pa)
    a, b, c = a_y, b_y, c_y  
    # Density bounds (kg/m³)
    d_min, d_peak, d_max = a_d, b_d, c_d  

    # 1) Read in α and α′ series from the user
    # alpha_cuts = [0.3, 0.4, 0.5]  
    alpha = alpha_cuts
    alpha_prime = alpha_dash_cuts
    # Check that both lists have the same length
    if len(alpha) != len(alpha_prime):
        raise ValueError("α and α′ lists must have the same length!")

    # 2) Compute the lower and upper bounds for Y and ρ
    Y_low    = [a + (b - a) * ai for ai in alpha]
    Y_high   = [c - (c - b) * ap for ap in alpha_prime]
    rho_low  = [d_min + (d_peak - d_min) * ai for ai in alpha]
    rho_high = [d_max - (d_max - d_peak) * ap for ap in alpha_prime]
    
    # 3) Calculate natural frequencies for all four combinations
    fn1 = [(1/(2 * np.pi)) * np.sqrt(Y / ro) for Y, ro in zip(Y_low,  rho_low)]
    fn2 = [(1/(2 * np.pi)) * np.sqrt(Y / ro) for Y, ro in zip(Y_high, rho_low)]
    fn3 = [(1/(2 * np.pi)) * np.sqrt(Y / ro) for Y, ro in zip(Y_low,  rho_high)]
    fn4 = [(1/(2 * np.pi)) * np.sqrt(Y / ro) for Y, ro in zip(Y_high, rho_high)]
    
    # Function to format list
    def format_list(values):
        formatted = [round(float(v), 4) for v in values]
        # print(f"{name} : {formatted}")
        return formatted
    # Print formatted outputs
    fn1 = format_list(fn1)
    fn2 = format_list(fn2)
    fn3 = format_list(fn3)
    fn4 = format_list(fn4)

    alpha_dash_alpha = [f"{a}-{b}" for a, b in zip(alpha_cuts, alpha_dash_cuts)]

    fn_dict = {
    'α-α': alpha_dash_alpha,
    'fn1': [round(float(v), 4) for v in fn1],
    'fn2': [round(float(v), 4) for v in fn2],
    'fn3': [round(float(v), 4) for v in fn3],
    'fn4': [round(float(v), 4) for v in fn4],
    }
    return fn_dict

    # df = pd.DataFrame(data)
    # print("\nNatural Frequency Table (in Hz):")
    # print(df.to_string(index=False))

def export_table_image(g_name, alpha , fn_dict, alpha_cuts, alpha_dash_cuts):
    if alpha_dash_cuts is not None:
        alpha_dash_alpha = [f"{a}-{b}" for a, b in zip(alpha_cuts, alpha_dash_cuts)]
    alpha_cuts = alpha_cuts    
    df = pd.DataFrame({
        # 'α': alpha_cuts,
        **({'α': alpha_cuts} if alpha_dash_cuts is None else {"α-α'": alpha_dash_alpha}),
        'fn₁ (Y̲,ρ̲)': fn_dict['fn1'],
        'fn₂ (Y̅,ρ̲)': fn_dict['fn2'],
        'fn₃ (Y̲,ρ̅ )': fn_dict['fn3'],
        'fn₄ (Y̅,ρ̅ )': fn_dict['fn4']
    })
    
    # Reset index and pass only values without index
    fig, ax = plt.subplots(figsize=(6, 2.8))
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
    for (row, col), cell in tbl.get_celld().items():
        cell.set_height(0.22)
        cell.set_width(0.18)
    
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
