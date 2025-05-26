import matplotlib.pyplot as plt
import numpy as np

# For Alpha Cuts
def GetBarChat(alpha_cuts,fn_dict, graph, material, aval, fun_type):
    # alphas = [0.3, 0.4, 0.5]
    alphas = alpha_cuts
    # bar_width = 0.15
    bar_width = 0.2
    x = np.arange(len(alphas))

    fn1 =  fn_dict["fn1"]
    fn2 =  fn_dict["fn2"]
    fn3 =  fn_dict["fn3"]
    fn4 =  fn_dict["fn4"]

    plt.figure(figsize=(10, 5))
    bars1 = plt.bar(x,               fn1, width=bar_width, label='fn1 (Y̲,ρ̲)')
    bars2 = plt.bar(x+bar_width,     fn2, width=bar_width, label='fn2 (Y̅,ρ̲)')
    bars3 = plt.bar(x+2*bar_width,   fn3, width=bar_width, label='fn3 (Y̲,ρ̅)')
    bars4 = plt.bar(x+3*bar_width,   fn4, width=bar_width, label='fn4 (Y̅,ρ̅)')

    # Annotate each bar
    def annotate(bars, vals):
        for bar, val in zip(bars, vals):
            plt.text(bar.get_x()+bar.get_width()/2,
                 bar.get_height()+0.01,
                 f"{val:.4f}", ha='center', va='bottom', fontsize=8)

    annotate(bars1, fn1)
    annotate(bars2, fn2)
    annotate(bars3, fn3)
    annotate(bars4, fn4)

    # X ticks centered
    centers = x + 1.5*bar_width
    plt.xticks(centers, alphas)
    
    # Y limits and grid
    all_vals = fn1 + fn2 + fn3 + fn4
    plt.ylim(min(all_vals)*0.95, max(all_vals)*1.05)
    plt.grid(axis='y', linestyle='--', alpha=0.6)

    # plt.xlabel("α - Level")
    if aval == 1:
        plt.xlabel('α-level')
    else:
        plt.xlabel('α dash-level')
    plt.ylabel("Natural Frequency (Hz)")
    # plt.title("Natural Frequencies of Aluminium for Different α-Cuts")
    if aval == 1:
        plt.title("Natural Frequency vs α-level for "+ fun_type + " MF (" + material + ")")
    else:
        plt.title("Natural Frequency vs α-dash level for "+ fun_type + " MF (" + material + ")")

    # ——— Move legend outside ———
    plt.subplots_adjust(right=0.75)
    plt.legend(loc='upper left', bbox_to_anchor=(1.02, 1), borderaxespad=0)
    plt.tight_layout()
    # plt.show()
    g = "static/img/" + graph
    plt.savefig(g)
    plt.close()  # Close the figure to free up memory
   # ================== End GetBarChat()========================
    
# For Alpha dash Cuts
def GetBarChat2(alpha_cuts, alpha_dash_cuts,fn_dict, graph, material, aval, fun_type):
    print('Alpha - alpha dash Cuts')
    bar_width = 0.2
    x = np.arange(len(alpha_cuts))

    fn1 =  fn_dict["fn1"]
    fn2 =  fn_dict["fn2"]
    fn3 =  fn_dict["fn3"]
    fn4 =  fn_dict["fn4"]

    plt.figure(figsize=(12, 6))
    plt.bar(x,                fn1, width=bar_width, label='fn1 (Y̲,ρ̲)')
    plt.bar(x + bar_width,    fn2, width=bar_width, label='fn2 (Y̅,ρ̲)')
    plt.bar(x + 2*bar_width,  fn3, width=bar_width, label='fn3 (Y̲,ρ̅)')
    plt.bar(x + 3*bar_width,  fn4, width=bar_width, label='fn4 (Y̅,ρ̅)')

    # Annotate each bar with its value
    for i in range(len(x)):
        plt.text(x[i],                fn1[i], f"{fn1[i]:.4f}", ha='center', va='bottom', fontsize=8)
        plt.text(x[i] + bar_width,    fn2[i], f"{fn2[i]:.4f}", ha='center', va='bottom', fontsize=8)
        plt.text(x[i] + 2*bar_width,  fn3[i], f"{fn3[i]:.4f}", ha='center', va='bottom', fontsize=8)
        plt.text(x[i] + 3*bar_width,  fn4[i], f"{fn4[i]:.4f}", ha='center', va='bottom', fontsize=8)

    # Center the x-axis labels between the groups
    centers = x + 1.5 * bar_width
    xtick_labels = [f"({a:.2f}–{b:.2f})" for a, b in zip(alpha_cuts, alpha_dash_cuts)]
    plt.xticks(centers, xtick_labels, fontsize=11)
    plt.xlim(centers[0] - bar_width * 2, centers[-1] + bar_width * 2.5)

    # Set y-axis limits with a small margin
    all_frequencies = fn1 + fn2 + fn3 + fn4
    plt.ylim(min(all_frequencies) * 0.95, max(all_frequencies) * 1.05)

    plt.xlabel("(α–α′) Cuts", fontsize=12)
    plt.ylabel("Natural Frequency (Hz)", fontsize=12)
    # plt.title("Natural Frequencies for (α–α′) Cuts", fontsize=14)
    plt.title("Natural Frequency vs (α–α′) Cuts for "+ fun_type + " MF (" + material + ")", fontsize=14)
    plt.grid(axis='y', linestyle='--', alpha=0.6)

    # Move legend outside the plot
    plt.subplots_adjust(right=0.75)
    plt.legend(loc='upper left', bbox_to_anchor=(1.02, 1), borderaxespad=0)

    plt.tight_layout()
    # plt.show()
    g = "static/img/" + graph
    plt.savefig(g)
    plt.close()

# Alpha levels Old Code
# def GetBarChat(alpha_cuts,fn_dict, graph, material, aval, fun_type):
#     # alphas = [0.3, 0.4, 0.5]
#     alphas = alpha_cuts
#     # print(alphas)
#     # Natural frequencies for each alpha level
#     # fn1 = [0.816, 0.819, 0.822]
#     # fn2 = [0.857, 0.854, 0.851]
#     # fn3 = [0.812, 0.815, 0.819]
#     # fn4 = [0.853, 0.851, 0.848]
#     fn1 =  fn_dict["fn1"]
#     fn2 =  fn_dict["fn2"]
#     fn3 =  fn_dict["fn3"]
#     fn4 =  fn_dict["fn4"]
#     # print(fn1)
#     # Bar width and positions
#     bar_width = 0.2
#     r1 = np.arange(len(alphas))
#     r2 = [x + bar_width for x in r1]
#     r3 = [x + bar_width for x in r2]
#     r4 = [x + bar_width for x in r3]

#     # Plotting the bar chart
#     plt.figure(figsize=(10, 6))
#     plt.bar(r1, fn1, width=bar_width, label='fn₁ (Y, ρ)')
#     plt.bar(r2, fn2, width=bar_width, label='fn₂ (Y̅, ρ)')
#     plt.bar(r3, fn3, width=bar_width, label='fn₃ (Y, ρ̅)')
#     plt.bar(r4, fn4, width=bar_width, label='fn₄ (Y̅, ρ̅)')

    
#     # for i in range(len(alphas)):
#     #     plt.text(r1[i], fn1[i]/2, f'{fn1[i]:.3f}', ha='center', va='top', rotation=90, color='white', fontsize=9)
#     #     plt.text(r2[i], fn2[i]/2, f'{fn2[i]:.3f}', ha='center', va='center', rotation=90, color='white', fontsize=9)
#     #     plt.text(r3[i], fn3[i]/2, f'{fn3[i]:.3f}', ha='center', va='center', rotation=90, color='white', fontsize=9)
#     #     plt.text(r4[i], fn4[i]/2, f'{fn4[i]:.3f}', ha='center', va='center', rotation=90, color='white', fontsize=9)
#     for i in range(len(alphas)):
#         plt.text(r1[i], fn1[i] - 0.01, f'{fn1[i]:.3f}', ha='center', va='top', rotation=90, color='white', fontsize=10)
#         plt.text(r2[i], fn2[i] - 0.01, f'{fn2[i]:.3f}', ha='center', va='top', rotation=90, color='white', fontsize=10)
#         plt.text(r3[i], fn3[i] - 0.01, f'{fn3[i]:.3f}', ha='center', va='top', rotation=90, color='white', fontsize=10)
#         plt.text(r4[i], fn4[i] - 0.01, f'{fn4[i]:.3f}', ha='center', va='top', rotation=90, color='white', fontsize=10)
#     # Labels and ticks
#     if aval == 1:
#         plt.xlabel('α-level')
#     else:
#         plt.xlabel('α dash-level')
#     plt.ylabel('Natural Frequency (fn)')
#     if aval == 1:
#         plt.title("Natural Frequency vs α-level for "+ fun_type + " MF (" + material + ")")
#     else:
#         plt.title("Natural Frequency vs α-dash level for "+ fun_type + " MF (" + material + ")")
#     plt.xticks([r + 1.5 * bar_width for r in range(len(alphas))], alphas)
#     plt.legend()
#     plt.grid(True, axis='y', linestyle='--', alpha=0.6)
#     plt.ylim(0.0, 1.0)  # Set y-axis from 0.0 to 1.0
#     plt.xlim(-0.1, r4[-1] + bar_width + 0.1)
#     plt.tight_layout()
#     # plt.show()
#     g = "static/img/" + graph
#     plt.savefig(g)
#     plt.close()  # Close the figure to free up memory