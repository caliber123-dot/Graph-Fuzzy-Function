# Define parameters for the trapezoidal function
import math

# For Trapezoidal fn
def GetFuns(alpha_cuts, a_y,b_y,c_y,d_y,a_d,b_d,c_d,d_d):
    # alpha_cuts = [0.3, 0.4, 0.5]
    # print('Young modulus:')
    a = a_y #Min
    b = b_y #peak
    c = c_y #upper peak
    d = d_y #Max   
    Y_min_list = []
    Y_max_list = []
    for alpha in alpha_cuts:
        Y_min = a + (b - a) * alpha
        Y_max = d - (d - c) * alpha 
        Y_min_list.append(Y_min)
        Y_max_list.append(Y_max)

    # print('Density:')
    a2 = a_d  # Minimum value (kg/m³)
    b2 = b_d  # Lower bound of plateau (kg/m³)
    c2 = c_d  # Upper bound of plateau (kg/m³)
    d2 = d_d  # Maximum value (kg/m³)
    d_min_list = []
    d_max_list = []
    for alpha in alpha_cuts:
        d_min = a2 + (b2 - a2) * alpha
        d_max = d2 - (d2 - c2) * alpha 
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
        
    fn_dict = {
        'α': alpha_cuts,
        "fn1": fn1_list,
        "fn2": fn2_list,
        "fn3": fn3_list,
        "fn4": fn4_list
    }
    return fn_dict
    
# fn_dict = GetFuns()
# print('function3:',fn_dict["fn3"])
# For Alpha dash >>> Change according to GetFunsTriangular2()
def GetFuns2(alpha_cuts, a_y,b_y,c_y,d_y,a_d,b_d,c_d,d_d,alpha1):
    # alpha_cuts = [0.3, 0.4, 0.5]
    # print('Young modulus:')
    a = a_y #Min
    b = b_y #peak
    c = c_y #upper peak
    d = d_y #Max   
    Y_min_list = []
    Y_max_list = []
    for alpha in alpha_cuts:
        Y_min = a + (b - a) * alpha
        Y_max = d - (d - c) * alpha 
        Y_min_list.append(Y_min)
        Y_max_list.append(Y_max)

    # print('Density:')
    a2 = a_d  # Minimum value (kg/m³)
    b2 = b_d  # Lower bound of plateau (kg/m³)
    c2 = c_d  # Upper bound of plateau (kg/m³)
    d2 = d_d  # Maximum value (kg/m³)
    d_min_list = []
    d_max_list = []
    for alpha in alpha_cuts:
        d_min = a2 + (b2 - a2) * alpha
        d_max = d2 - (d2 - c2) * alpha 
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
        # print("alpha:>>>>>", alpha1)
        alpha_dash_alpha = [f"{a}-{b}" for a, b in zip(alpha1,alpha_cuts)]
    fn_dict = {
        "α-α": alpha_dash_alpha,
        "fn1": fn1_list,
        "fn2": fn2_list,
        "fn3": fn3_list,
        "fn4": fn4_list
    }
    return fn_dict

# For Alpha >> Get Min amd Max Value for Trapezoidal Graph
def GetMinMax(alpha_cuts, a_y,b_y,c_y,d_y,a_d,b_d,c_d,d_d):
    a = a_y #Min
    b = b_y #peak
    c = c_y #upper peak
    d = d_y #Max   
    Y_min_list = []
    Y_max_list = []
    for alpha in alpha_cuts:
        Y_min = a + (b - a) * alpha
        Y_max = d - (d - c) * alpha 
        Y_min_list.append(Y_min)
        Y_max_list.append(Y_max)

    # print('Density:')
    a2 = a_d  # Minimum value (kg/m³)
    b2 = b_d  # Lower bound of plateau (kg/m³)
    c2 = c_d  # Upper bound of plateau (kg/m³)
    d2 = d_d  # Maximum value (kg/m³)
    d_min_list = []
    d_max_list = []
    for alpha in alpha_cuts:
        d_min = a2 + (b2 - a2) * alpha
        d_max = d2 - (d2 - c2) * alpha 
        d_min_list.append(d_min)
        d_max_list.append(d_max)
    
        
    fn_dict = {
        'α': alpha_cuts,
        "Ymin": Y_min_list,
        "Ymax": Y_max_list,
        "dmin": d_min_list,
        "dmax": d_max_list
    }
    return fn_dict

# For Alpha dash >> Get Min amd Max Value for Trapezoidal Graph
def GetMinMax2(alpha_cuts, a_y,b_y,c_y,d_y,a_d,b_d,c_d,d_d,alpha_dash):
    # alpha_cuts = [0.3, 0.4, 0.5]
    # print('Young modulus:')
    a = a_y #Min
    b = b_y #peak
    c = c_y #upper peak
    d = d_y #Max   
    Y_min_list = []
    Y_max_list = []
    # for alpha in alpha_cuts:
    #     Y_min = a + (b - a) * alpha
    #     Y_max = d - (d - c) * alpha 
    #     Y_min_list.append(Y_min)
    #     Y_max_list.append(Y_max)
    for alpha1, alpha2 in zip(alpha_cuts, alpha_dash):
        Y_min = a + (b - a) * alpha1
        Y_max = d - (d - c) * alpha2
        Y_min_list.append(Y_min)
        Y_max_list.append(Y_max)

    # print('Density:')
    a2 = a_d  # Minimum value (kg/m³)
    b2 = b_d  # Lower bound of plateau (kg/m³)
    c2 = c_d  # Upper bound of plateau (kg/m³)
    d2 = d_d  # Maximum value (kg/m³)
    d_min_list = []
    d_max_list = []
    # for alpha in alpha_cuts:
    for alpha1, alpha2 in zip(alpha_cuts, alpha_dash):
        d_min = a2 + (b2 - a2) * alpha1
        d_max = d2 - (d2 - c2) * alpha2 
        d_min_list.append(d_min)
        d_max_list.append(d_max)
           
        # print("alpha:>>>>>", alpha1)
        alpha_dash_alpha = [f"{a}-{b}" for a, b in zip(alpha_cuts,alpha_dash)]
    fn_dict = {
        "α-α": alpha_dash_alpha,
        "Ymin": Y_min_list,
        "Ymax": Y_max_list,
        "dmin": d_min_list,
        "dmax": d_max_list
    }
    return fn_dict
