from flask import Flask, render_template, request
from waitress import serve
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

load_dotenv() # Load variables from .env file
# app.secret_key = os.getenv('SECRET_KEY')
# Configure the PostgreSQL connection
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class tbl_materials(db.Model):
    mat_id = db.Column(db.Integer, primary_key=True)
    mat_name = db.Column(db.String(100), nullable=False) # Cannot be NULL
    mat_a_val = db.Column(db.String(50), nullable=False)
    mat_b_val = db.Column(db.String(50), nullable=False)
    mat_c_val = db.Column(db.String(50), nullable=False)
    mat_d_val = db.Column(db.String(50), nullable=False)
    mat_status = db.Column(db.Integer, nullable=False)

class tbl_alpha(db.Model):
    alpha_id = db.Column(db.Integer, primary_key=True)
    alpha_fm_id = db.Column(db.Integer, nullable=False)
    alpha_mat_id = db.Column(db.Integer, nullable=False)
    alpha_alpha1 = db.Column(db.Float, nullable=False) # Cannot be NULL
    alpha_alpha2 = db.Column(db.Float, nullable=False)
    alpha_alpha3 = db.Column(db.Float, nullable=False)
    alpha_alphadash1 = db.Column(db.Float, nullable=True)
    alpha_alphadash2 = db.Column(db.Float, nullable=True)
    alpha_alphadash3 = db.Column(db.Float, nullable=True)
    alpha_status = db.Column(db.Integer, nullable=False)

# Initialize the database
@app.route('/init_db')
def init_db():
    try:
        with app.app_context():
            db.create_all()
            # List of material names to check and insert
            material_names = ["Aluminium", "Neoprene Rubber", "Teflon", "Nylon", "SS-304 Grade ABS Silicon"]
            # Check which materials already exist
            existing_materials = tbl_materials.query.filter(tbl_materials.mat_name.in_(material_names)).all()
            existing_names = [mat.mat_name for mat in existing_materials]
            # Only add materials that don't already exist
            materials_to_add = []
            if "Aluminium" not in existing_names:
                materials_to_add.append(tbl_materials(
                    mat_name="Aluminium", mat_a_val="0.2", mat_b_val="0.4",
                    mat_c_val="0.6", mat_d_val="0.8", mat_status=1
                ))
            if "Neoprene Rubber" not in existing_names:
                materials_to_add.append(tbl_materials(
                    mat_name="Neoprene Rubber", mat_a_val="0.1", mat_b_val="0.3",
                    mat_c_val="0.5", mat_d_val="0.7", mat_status=1
                ))

            if "Teflon" not in existing_names:
                materials_to_add.append(tbl_materials(
                    mat_name="Teflon", mat_a_val="0.15", mat_b_val="0.35",
                    mat_c_val="0.55", mat_d_val="0.75", mat_status=1
                ))

            if "Nylon" not in existing_names:
                materials_to_add.append(tbl_materials(
                    mat_name="Nylon", mat_a_val="0.25", mat_b_val="0.45",
                    mat_c_val="0.65", mat_d_val="0.85", mat_status=1
                ))
            if "SS-304 Grade ABS Silicon" not in existing_names:
                materials_to_add.append(tbl_materials(
                    mat_name="SS-304 Grade ABS Silicon", mat_a_val="0.25", mat_b_val="0.45",
                    mat_c_val="0.65", mat_d_val="0.85", mat_status=1
                ))
            # Add to session and commit to the database
            if materials_to_add:
                db.session.add_all(materials_to_add)
                db.session.commit()
                print("Material added successfully.")    
                return "<h1>Tables created and materials inserted successfully.</h1>", 200    
            else:
                 return "<h1>Tables already created. All materials already exist.</h1>", 200    
            # print("Tables created!")
            # return "<h1>Tables created successfully!</h1>", 200
    except Exception as e:
        return f"Error creating Tables: {str(e)}", 500

from app_fn import GetFuns
from barchat import GetBarChat
@app.route('/graph', methods=['GET', 'POST'])
# @app.route('/graph')
def graph():    
    g1 = g2 = g3 = g4 = 'basic.avif' # Default Graph Image
    alpha_cuts = ''
    alpha_dash_cuts= ''
    fn_dict_dash = fn_dict = ''
    materials = tbl_materials.query.filter_by(mat_status=1).all()  # Only active materials
    if request.method=='POST':
        ddlfuntion = request.form.get('ddlfuntion')  # ID
        ddlmat_ID = request.form.get('ddlmaterials') # ID 
        a1 = safe_float(request.form.get('alpha1'))
        a2 = safe_float(request.form.get('alpha2'))
        a3 = safe_float(request.form.get('alpha3'))

        a4 = safe_float(request.form.get('alpha_dash1'))
        a5 = safe_float(request.form.get('alpha_dash2'))
        a6 = safe_float(request.form.get('alpha_dash3'))     
        material = tbl_materials.query.filter_by(mat_id=ddlmat_ID).first()
        mat_name = material.mat_name if material else None
        # print("Material Name =====>>>>", mat_name)
        fun_type = ''
        if(ddlfuntion == '1'):   
            fun_type = "Trapezoidal" 
        else:
            fun_type = "Triangular"
        alpha_cuts = [a1, a2, a3]        
        fn_dict = GetFuns(alpha_cuts)
        g2 = 'Bar_alpha' + 'MF' + '.png' 
        g1 = GetBarChat(alpha_cuts, fn_dict, g2, mat_name, 1, fun_type)
        # Alpha dash code
        alpha_dash_cuts = [a4, a5, a6]        
        fn_dict_dash = GetFuns(alpha_dash_cuts)
        g4 = 'Bar_alpha_dash' + 'MF' + '.png' 
        g3 = GetBarChat(alpha_dash_cuts, fn_dict_dash, g4, mat_name, 2, fun_type)
        return render_template('graph.html',fn_dict= fn_dict,alpha_cuts=alpha_cuts,alpha_dash_cuts=alpha_dash_cuts,fn_dict_dash=fn_dict_dash,g1=g1,g2=g2,g3=g3,g4=g4,a1=a1,a2=a2,a3=a3,a4=a4,a5=a5,a6=a6,s1=ddlmat_ID,s2=ddlfuntion,materials=materials)
    
    return render_template('graph.html',g1=g1,g2=g2,g3=g3,g4=g4,materials=materials,s1=None)

from AlphaDensity import alphaDensityFun
from AlphaYoung import alphaYoungFun
from TriangularDensity import TriangularDensity
from TriangularYoung import TriangularYoungFun
@app.route('/', methods=['GET', 'POST'])
def index():
    # alpha = [0.313, 0.455, 0.585]
    materials = tbl_materials.query.filter_by(mat_status=1).all()  # Only active materials
    g1 = g2 = g3 = g4 = 'basic.avif' # Default Graph Image
    if request.method=='POST':
        # Retrieve form data
        ddlmaterials = request.form.get('ddlmaterials')
        # print(ddlmaterials)
        ddlfuntion = request.form.get('ddlfuntion')      

        material = request.form.get('material') 
        if material.strip() != '':
            msg = add_Materials(ddlmaterials,material)
            materials = tbl_materials.query.filter_by(mat_status=1).all()  # Only active materials
            return render_template('index.html', g1=g1,g2=g2,g3=g3,g4=g4,materials=materials,s1=ddlmaterials,s2=ddlfuntion,msg=msg)     
        else:
        # print(ddlfuntion)
        # ddlgraph = None  
            a1 = safe_float(request.form.get('alpha1'))
            a2 = safe_float(request.form.get('alpha2'))
            a3 = safe_float(request.form.get('alpha3'))

            a4 = safe_float(request.form.get('alpha_dash1'))
            a5 = safe_float(request.form.get('alpha_dash2'))
            a6 = safe_float(request.form.get('alpha_dash3'))   
            alpha_id = request.form.get('alpha_id')
            if alpha_id.strip() != '':
                print("Record Found")
            else:
                print("No Record")
            msg = add_Alpha(a1,a2,a3,a4,a5,a6,ddlfuntion,ddlmaterials)
            if(msg == "Record updated successfully!"):
                is_update = True
            else:
                is_update = False
            print(msg)        

            if a1 != '' and a2 != '' and a3 != '': 
                
                g1 = 'Alpha_' + 'Density' + '.png'   
                g3 = 'Alpha_' + 'Young' + '.png' 
                if(ddlfuntion == 'Trapezoidal'):
                    alphaDensityFun(a1,a2,a3,g1)
                    alphaYoungFun(a1,a2,a3,g3)
                else:
                    TriangularDensity(a1,a2,a3,g1)
                    TriangularYoungFun(a1,a2,a3,g3)
                
            if a4 != '' and a5 != '' and a6 != '': 
                
                g2 = 'Alpha_dash_' + 'Density' + '.png'  
                g4 = 'Alpha_dash_' + 'Young' + '.png' 
                if(ddlfuntion == 'Trapezoidal'):
                    alphaDensityFun(a4,a5,a6,g2)               
                    alphaYoungFun(a4,a5,a6,g4)  
                else:
                    TriangularDensity(a4,a5,a6,g2)
                    TriangularYoungFun(a4,a5,a6,g4)
                    
            return render_template('index.html', g1=g1,g2=g2,g3=g3,g4=g4,a1=a1,a2=a2,a3=a3,a4=a4,a5=a5,a6=a6,materials=materials,s1=ddlmaterials,s2=ddlfuntion,alpha_id=alpha_id,is_update=is_update)     
    return render_template('index.html',g1=g1,g2=g2,g3=g3,g4=g4,materials=materials, s1=None)
def add_Materials(ddlmaterials,material):
    myMsg = ''  
    a_value = safe_float(request.form.get('a_value'))
    b_value = safe_float(request.form.get('b_value'))
    c_value = safe_float(request.form.get('c_value'))
    d_value = safe_float(request.form.get('d_value'))
    # Check if the material already exists (by name)
    existing_material = tbl_materials.query.filter_by(mat_name=material).first()
    if existing_material:
        myMsg = f"Material '{material}' already exists!"
    else:
        # Create new record
        new_material = tbl_materials(
            mat_name=material,
            mat_a_val=str(a_value),
            mat_b_val=str(b_value),
            mat_c_val=str(c_value),
            mat_d_val=str(d_value),
            mat_status=1
        )
        db.session.add(new_material)
        db.session.commit()
        myMsg = "Material added successfully!"
    return myMsg
def add_Alpha(a1,a2,a3,a4,a5,a6,ddlfuntion,ddlmaterials):
    myMsg = ''   
    # Check if email or phone number already exists
    existing_record = tbl_alpha.query.filter((tbl_alpha.alpha_fm_id == ddlfuntion) & (tbl_alpha.alpha_mat_id == ddlmaterials)).first()
    if existing_record:
        # Update the existing record
        existing_record.alpha_alpha1 = a1
        existing_record.alpha_alpha2 = a2
        existing_record.alpha_alpha3 = a3
        existing_record.alpha_alphadash1 = a4
        existing_record.alpha_alphadash2 = a5
        existing_record.alpha_alphadash3 = a6
        existing_record.alpha_status = 1
        db.session.commit()
        myMsg = "Record updated successfully!"
        # myMsg = "Record already exists with this function or materials."
    else:
        # Add new record        
        tosave = tbl_alpha(
            alpha_fm_id=ddlfuntion,
            alpha_mat_id=ddlmaterials,
            alpha_alpha1=a1,
            alpha_alpha2=a2,
            alpha_alpha3=a3,
            alpha_alphadash1=a4,
            alpha_alphadash2=a5,
            alpha_alphadash3=a6,
            alpha_status=1
        )
        db.session.add(tosave)
        db.session.commit()
        myMsg = "Record saved successful!"
    return myMsg
def safe_float(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default

@app.route('/get_alpha_data/<int:mat_id>/<int:fm_id>')
def get_alpha_data(mat_id,fm_id):
    # Fetch the first matching record for that material
    # alpha_record = tbl_alpha.query.filter_by(alpha_mat_id=mat_id).first()
    alpha_record = tbl_alpha.query.filter((tbl_alpha.alpha_fm_id == fm_id) & (tbl_alpha.alpha_mat_id == mat_id)).first()
    if alpha_record:
        return {
            "alpha1": alpha_record.alpha_alpha1,
            "alpha2": alpha_record.alpha_alpha2,
            "alpha3": alpha_record.alpha_alpha3,
            "alphadash1": alpha_record.alpha_alphadash1,
            "alphadash2": alpha_record.alpha_alphadash2,
            "alphadash3": alpha_record.alpha_alphadash3,
            "alpha_id": alpha_record.alpha_id,
        }
    else:
        return {}, 204  # No content found

if __name__ == '__main__':
    # app.run(host="0.0.0.0", port=8000, debug=True)
    serve(app, host="0.0.0.0", port=8000, threads=8)
