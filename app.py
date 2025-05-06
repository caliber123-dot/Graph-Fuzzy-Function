from flask import Flask, render_template, request
from waitress import serve

app = Flask(__name__)

from app_fn import GetFuns
from barchat import GetBarChat
@app.route('/graph', methods=['GET', 'POST'])
# @app.route('/graph')
def graph():    
    g1 = g2 = g3 = g4 = 'basic.avif' # Default Graph Image
    alpha_cuts = ''
    alpha_dash_cuts= ''
    fn_dict_dash = fn_dict = ''
    if request.method=='POST':
        ddlfuntion = request.form.get('ddlfuntion')  
        ddlmaterials = request.form.get('ddlmaterials')        
        if(ddlfuntion == 'Trapezoidal'):    
            alpha_cuts = [0.3, 0.4, 0.5]        
            fn_dict = GetFuns(alpha_cuts)
            g2 = 'Bar_alpha' + 'MF' + '.png' 
            g1 = GetBarChat(alpha_cuts,fn_dict,g2,ddlmaterials, 1)
            # Alpha dash code
            alpha_dash_cuts = [0.35, 0.48, 0.54]        
            fn_dict_dash = GetFuns(alpha_dash_cuts)
            g4 = 'Bar_alpha_dash' + 'MF' + '.png' 
            g3 = GetBarChat(alpha_dash_cuts,fn_dict_dash,g4,ddlmaterials, 2)
        return render_template('graph.html',fn_dict= fn_dict,alpha_cuts=alpha_cuts,alpha_dash_cuts=alpha_dash_cuts,fn_dict_dash=fn_dict_dash,g1=g1,g2=g2,g3=g3,g4=g4,s1=ddlmaterials,s2=ddlfuntion)
    
    return render_template('graph.html',g1=g1,g2=g2,g3=g3,g4=g4)

from AlphaDensity import alphaDensityFun
from AlphaYoung import alphaYoungFun
from TriangularDensity import TriangularDensity
from TriangularYoung import TriangularYoungFun
@app.route('/', methods=['GET', 'POST'])
def index():
    # alpha = [0.313, 0.455, 0.585]
    g1 = g2 = g3 = g4 = 'basic.avif' # Default Graph Image
    if request.method=='POST':
        # Retrieve form data
        ddlmaterials = request.form.get('ddlmaterials')
        ddlfuntion = request.form.get('ddlfuntion')      
        print(ddlfuntion)
        # ddlgraph = None  
        a1 = request.form.get('alpha1')
        a2 = request.form.get('alpha2')
        a3 = request.form.get('alpha3')

        a4 = request.form.get('alpha_dash1')
        a5 = request.form.get('alpha_dash2')
        a6 = request.form.get('alpha_dash3')   
        if a1.strip() != '' and a2.strip() != '' and a3.strip() != '': 
            a1 = float(a1)
            a2 = float(a2)
            a3 = float(a3) 
            g1 = 'Alpha_' + 'Density' + '.png'   
            g3 = 'Alpha_' + 'Young' + '.png' 
            if(ddlfuntion == 'Trapezoidal'):
                alphaDensityFun(a1,a2,a3,g1)
                alphaYoungFun(a1,a2,a3,g3)
            else:
                TriangularDensity(a1,a2,a3,g1)
                TriangularYoungFun(a1,a2,a3,g3)
            
        if a4.strip() != '' and a5.strip() != '' and a6.strip() != '': 
            a4 = float(a4)
            a5 = float(a5)
            a6 = float(a6) 
            g2 = 'Alpha_dash_' + 'Density' + '.png'  
            g4 = 'Alpha_dash_' + 'Young' + '.png' 
            if(ddlfuntion == 'Trapezoidal'):
                alphaDensityFun(a4,a5,a6,g2)               
                alphaYoungFun(a4,a5,a6,g4)  
            else:
                TriangularDensity(a4,a5,a6,g2)
                TriangularYoungFun(a4,a5,a6,g4)
                
        return render_template('index.html', g1=g1,g2=g2,g3=g3,g4=g4,a1=a1,a2=a2,a3=a3,a4=a4,a5=a5,a6=a6,s1=ddlmaterials,s2=ddlfuntion )     
    return render_template('index.html',g1=g1,g2=g2,g3=g3,g4=g4)

if __name__ == '__main__':
    # app.run(host="0.0.0.0", port=8000, debug=True)
    serve(app, host="0.0.0.0", port=8000, threads=8)
