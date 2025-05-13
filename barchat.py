import matplotlib.pyplot as plt
import numpy as np

# Alpha levels
def GetBarChat(alpha_cuts,fn_dict, graph, material, aval, fun_type):
    # alphas = [0.3, 0.4, 0.5]
    alphas = alpha_cuts
    # print(alphas)
    # Natural frequencies for each alpha level
    # fn1 = [0.816, 0.819, 0.822]
    # fn2 = [0.857, 0.854, 0.851]
    # fn3 = [0.812, 0.815, 0.819]
    # fn4 = [0.853, 0.851, 0.848]
    fn1 =  fn_dict["fn1"]
    fn2 =  fn_dict["fn2"]
    fn3 =  fn_dict["fn3"]
    fn4 =  fn_dict["fn4"]
    # print(fn1)
    # Bar width and positions
    bar_width = 0.2
    r1 = np.arange(len(alphas))
    r2 = [x + bar_width for x in r1]
    r3 = [x + bar_width for x in r2]
    r4 = [x + bar_width for x in r3]

    # Plotting the bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(r1, fn1, width=bar_width, label='fn₁ (Y, ρ)')
    plt.bar(r2, fn2, width=bar_width, label='fn₂ (Y̅, ρ)')
    plt.bar(r3, fn3, width=bar_width, label='fn₃ (Y, ρ̅)')
    plt.bar(r4, fn4, width=bar_width, label='fn₄ (Y̅, ρ̅)')

    
    # for i in range(len(alphas)):
    #     plt.text(r1[i], fn1[i]/2, f'{fn1[i]:.3f}', ha='center', va='top', rotation=90, color='white', fontsize=9)
    #     plt.text(r2[i], fn2[i]/2, f'{fn2[i]:.3f}', ha='center', va='center', rotation=90, color='white', fontsize=9)
    #     plt.text(r3[i], fn3[i]/2, f'{fn3[i]:.3f}', ha='center', va='center', rotation=90, color='white', fontsize=9)
    #     plt.text(r4[i], fn4[i]/2, f'{fn4[i]:.3f}', ha='center', va='center', rotation=90, color='white', fontsize=9)
    for i in range(len(alphas)):
        plt.text(r1[i], fn1[i] - 0.01, f'{fn1[i]:.3f}', ha='center', va='top', rotation=90, color='white', fontsize=10)
        plt.text(r2[i], fn2[i] - 0.01, f'{fn2[i]:.3f}', ha='center', va='top', rotation=90, color='white', fontsize=10)
        plt.text(r3[i], fn3[i] - 0.01, f'{fn3[i]:.3f}', ha='center', va='top', rotation=90, color='white', fontsize=10)
        plt.text(r4[i], fn4[i] - 0.01, f'{fn4[i]:.3f}', ha='center', va='top', rotation=90, color='white', fontsize=10)
    # Labels and ticks
    if aval == 1:
        plt.xlabel('α-level')
    else:
        plt.xlabel('α dash-level')
    plt.ylabel('Natural Frequency (fn)')
    if aval == 1:
        plt.title("Natural Frequency vs α-level for "+ fun_type + " MF (" + material + ")")
    else:
        plt.title("Natural Frequency vs α-dash level for "+ fun_type + " MF (" + material + ")")
    plt.xticks([r + 1.5 * bar_width for r in range(len(alphas))], alphas)
    plt.legend()
    plt.grid(True, axis='y', linestyle='--', alpha=0.6)
    plt.ylim(0.0, 1.0)  # Set y-axis from 0.0 to 1.0
    plt.xlim(-0.1, r4[-1] + bar_width + 0.1)
    plt.tight_layout()
    # plt.show()
    g = "static/img/" + graph
    plt.savefig(g)
    plt.close()  # Close the figure to free up memory