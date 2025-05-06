# Define parameters for the trapezoidal function
import math

# print('Young modulus:')
def GetFuns(alpha_cuts):
    # alpha_cuts = [0.3, 0.4, 0.5]
    a = 68.95 #Min
    b = 72.46 #peak
    c = 76.46 #upper peak
    d =79.46 #Max   
    Y_min_list = []
    Y_max_list = []
    for alpha in alpha_cuts:
        Y_min = a + (b - a) * alpha
        Y_max = d - (d - c) * alpha 
        Y_min_list.append(Y_min)
        Y_max_list.append(Y_max)

    # print('Density:')
    a2 = 2.66  # Minimum value (kg/m³)
    b2 = 2.68  # Lower bound of plateau (kg/m³)
    c2 = 2.72  # Upper bound of plateau (kg/m³)
    d2 = 2.74  # Maximum value (kg/m³)
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
        "fn1": fn1_list,
        "fn2": fn2_list,
        "fn3": fn3_list,
        "fn4": fn4_list
    }
    return fn_dict
    
# fn_dict = GetFuns()
# print('function3:',fn_dict["fn3"])
