from flask import Flask, render_template, request , jsonify, send_file
from waitress import serve
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
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
    mat_fm_id = db.Column(db.Integer, nullable=False)
    mat_name = db.Column(db.String(100), nullable=False) # Cannot be NULL
    mat_a_val_d = db.Column(db.String(50), nullable=False)
    mat_b_val_d = db.Column(db.String(50), nullable=False)
    mat_c_val_d = db.Column(db.String(50), nullable=False)
    mat_d_val_d = db.Column(db.String(50), nullable=False)
    mat_a_val_y = db.Column(db.String(50), nullable=False)
    mat_b_val_y = db.Column(db.String(50), nullable=False)
    mat_c_val_y = db.Column(db.String(50), nullable=False)
    mat_d_val_y = db.Column(db.String(50), nullable=False)
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
             # Drop tbl_materials table if it exists
            tbl_materials.__table__.drop(db.engine, checkfirst=True)
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
                   mat_fm_id=1, mat_name="Aluminium", mat_a_val_d="2680", mat_b_val_d="2690",
                    mat_c_val_d="2710", mat_d_val_d="2720", mat_a_val_y="68947600000", mat_b_val_y="71402200000",
                    mat_c_val_y="77402200000", mat_d_val_y="79966000000", mat_status=1
                ))
                materials_to_add.append(tbl_materials(
                   mat_fm_id=2, mat_name="Aluminium", mat_a_val_d="2680", mat_b_val_d="2700",
                    mat_c_val_d="2720", mat_d_val_d="0", mat_a_val_y="68947600000", mat_b_val_y="74456800000",
                    mat_c_val_y="79966000000", mat_d_val_y="0", mat_status=1                   
                ))
            if "Neoprene Rubber" not in existing_names:
                materials_to_add.append(tbl_materials(
                   mat_fm_id=1, mat_name="Neoprene Rubber", mat_a_val_d="1250", mat_b_val_d="1260",
                    mat_c_val_d="1290", mat_d_val_d="1300", mat_a_val_y="100000", mat_b_val_y="200000",
                    mat_c_val_y="400000", mat_d_val_y="500000", mat_status=1
                ))
                materials_to_add.append(tbl_materials(
                   mat_fm_id=2, mat_name="Neoprene Rubber", mat_a_val_d="1250", mat_b_val_d="1275",
                    mat_c_val_d="1300", mat_d_val_d="0", mat_a_val_y="100000", mat_b_val_y="300000",
                    mat_c_val_y="500000", mat_d_val_y="0", mat_status=1                   
                ))
                
            if "Teflon" not in existing_names:
                materials_to_add.append(tbl_materials(
                   mat_fm_id=1, mat_name="Teflon", mat_a_val_d="2180", mat_b_val_d="2188",
                    mat_c_val_d="2212", mat_d_val_d="2220", mat_a_val_y="4.00e+08", mat_b_val_y="4.50e+08",
                    mat_c_val_y="5.50e+08", mat_d_val_y="6.00e+08", mat_status=1
                ))
                materials_to_add.append(tbl_materials(
                   mat_fm_id=2, mat_name="Teflon", mat_a_val_d="2180", mat_b_val_d="2200",
                    mat_c_val_d="2220", mat_d_val_d="0", mat_a_val_y="4.00e+08", mat_b_val_y="5.00e+08",
                    mat_c_val_y="6.00e+08", mat_d_val_y="0", mat_status=1                   
                ))

            if "Nylon" not in existing_names:
                materials_to_add.append(tbl_materials(
                   mat_fm_id=1, mat_name="Nylon", mat_a_val_d="1050", mat_b_val_d="1075",
                    mat_c_val_d="1125", mat_d_val_d="1150", mat_a_val_y="2.00e+09", mat_b_val_y="2.50e+09",
                    mat_c_val_y="3.50e+09", mat_d_val_y="4.00e+09", mat_status=1
                ))
                materials_to_add.append(tbl_materials(
                   mat_fm_id=2, mat_name="Nylon", mat_a_val_d="1050", mat_b_val_d="1100",
                    mat_c_val_d="1150", mat_d_val_d="0", mat_a_val_y="2.00E+09", mat_b_val_y="3.00E+09",
                    mat_c_val_y="4.00E+09", mat_d_val_y="0", mat_status=1                   
                ))
                
            if "SS-304 Grade ABS Silicon" not in existing_names:
                materials_to_add.append(tbl_materials(
                   mat_fm_id=1, mat_name="SS-304 Grade ABS Silicon", mat_a_val_d="7900", mat_b_val_d="7915",
                    mat_c_val_d="7945", mat_d_val_d="7960", mat_a_val_y="1.93e+11", mat_b_val_y="1.95e+11",
                    mat_c_val_y="1.98e+11", mat_d_val_y="2.00e+11", mat_status=1
                ))
                materials_to_add.append(tbl_materials(
                   mat_fm_id=2, mat_name="SS-304 Grade ABS Silicon", mat_a_val_d="7900", mat_b_val_d="7930",
                    mat_c_val_d="7960", mat_d_val_d="0", mat_a_val_y="1.93E+11", mat_b_val_y="1.96E+11",
                    mat_c_val_y="2.00E+11", mat_d_val_y="0", mat_status=1                   
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

@app.route('/newmat')
def newmat():
    # return render_template('index.html',g1=g1,g2=g2,g3=g3,g4=g4,materials=materials, s1=None)
    return render_template('newmat.html')

# @app.route('/abcd')
@app.route('/abcd', methods=['GET', 'POST'])
def abcd():
    if request.method=='POST':
        # print("========================")
        ddlfuntion = request.form.get('ddlfuntion') # id 
        materials = tbl_materials.query.filter(
        and_(
            tbl_materials.mat_status == 1,
            tbl_materials.mat_fm_id == ddlfuntion
        )).order_by(tbl_materials.mat_id).all()
        # Retrieve form data
        matid = request.form.get('ddlmaterials') # id
        # print(ddlmaterials)
        a_value_d = request.form.get('a_value_d')
        b_value_d = request.form.get('b_value_d')
        c_value_d = request.form.get('c_value_d')
        d_value_d = request.form.get('d_value_d')

        a_value_y = request.form.get('a_value_y')
        b_value_y = request.form.get('b_value_y')
        c_value_y = request.form.get('c_value_y')
        d_value_y = request.form.get('d_value_y')
        # Find the material with mat_id=1
        material_to_update = tbl_materials.query.get(matid)

        if material_to_update:
            # Update the existing material
            # material_to_update.mat_name = material
            material_to_update.mat_a_val_d = a_value_d.strip()
            material_to_update.mat_b_val_d = b_value_d.strip()
            material_to_update.mat_c_val_d = c_value_d.strip()
            material_to_update.mat_d_val_d = d_value_d.strip()

            material_to_update.mat_a_val_y = a_value_y.strip()
            material_to_update.mat_b_val_y = b_value_y.strip()
            material_to_update.mat_c_val_y = c_value_y.strip()
            material_to_update.mat_d_val_y = d_value_y.strip()
            # material_to_update.mat_status = 1            
            db.session.commit()
            myMsg = "Material updated successfully!"
        else:
            myMsg = "Material with ID=1 not found!"
        return render_template('abcd.html',materials=materials, s1=matid,s2=ddlfuntion,a=a_value_d,b=b_value_d,c=c_value_d,d=d_value_d,myMsg=myMsg,a1=a_value_y,b1=b_value_y,c1=c_value_y,d1=d_value_y)
    return render_template('abcd.html')

from app_fn import GetFuns, GetFuns2
from barchat import GetBarChat, GetBarChat2
from app_fn_triangular import GetFunsTriangular,GetFunsTriangular2, export_table_image
@app.route('/graph', methods=['GET', 'POST'])
# @app.route('/graph')
def graph():    
    g1 = g2 = g3 = g4 = 'basic.avif' # Default Graph Image
    alpha = ''
    alpha_cuts = ''
    alpha_dash_cuts= ''
    fn_dict_dash = fn_dict = ''
    # materials = tbl_materials.query.filter_by(mat_status=1).all()  # Only active materials
    if request.method=='POST':
        ddlfuntion = request.form.get('ddlfuntion')  # ID
        ddlmat_ID = request.form.get('ddlmaterials') # ID 
        ddlalphacut = request.form.get('ddlalphacut') # ID 

        materials = tbl_materials.query.filter(
        and_(
            tbl_materials.mat_status == 1,
            tbl_materials.mat_fm_id == ddlfuntion
        )).order_by(tbl_materials.mat_id).all()

        a1 = safe_float(request.form.get('alpha1'))
        a2 = safe_float(request.form.get('alpha2'))
        a3 = safe_float(request.form.get('alpha3'))

        a4 = safe_float(request.form.get('alpha_dash1'))
        a5 = safe_float(request.form.get('alpha_dash2'))
        a6 = safe_float(request.form.get('alpha_dash3'))     
        # material = tbl_materials.query.filter_by(mat_id=ddlmat_ID).first()
        # mat_name = material.mat_name if material else None
        material = tbl_materials.query.filter_by(mat_id=ddlmat_ID).first()
        if material:
            mat_name = material.mat_name if material else None
            a_d = safe_float(material.mat_a_val_d)
            b_d = safe_float(material.mat_b_val_d)
            c_d = safe_float(material.mat_c_val_d)
            d_d = safe_float(material.mat_d_val_d)
            a_y = safe_float(material.mat_a_val_y)
            b_y = safe_float(material.mat_b_val_y)
            c_y = safe_float(material.mat_c_val_y)
            d_y = safe_float(material.mat_d_val_y)
        # print("Material Name =====>>>>", mat_name)
        fun_type = ''
        if(ddlfuntion == '1'):   
            fun_type = "Trapezoidal" 
        else:
            fun_type = "Triangular"
        show_alpha="d-hide"
        show_alpha_dash="d-hide"
        t1 = "Alpha_Table.png"
        t2 = "Alpha_Table_Dash.png"
        # Select Alpha Cut: ddlalphacut
        if(ddlalphacut == "1"): #Alpha Cut
            t2 = "basic.avif"
            alpha_cuts = [a1, a2, a3]        
            if(ddlfuntion == '1'): # Trapezoidal
                fn_dict = GetFuns(alpha_cuts,a_y,b_y,c_y,d_y,a_d,b_d,c_d,d_d)
                # print(fn_dict)
                export_table_image(t1, "Table : α-Cut",fn_dict, alpha_cuts, None)
            else: # Triangular
                fn_dict = GetFunsTriangular(alpha_cuts,a_y,b_y,c_y,a_d,b_d,c_d)
                # print(fn_dict)
                export_table_image(t1, "Table : α-Cut",fn_dict, alpha_cuts, None)
            g2 = 'Bar_alpha' + 'MF' + '.png' 
            g1 = GetBarChat(alpha_cuts, fn_dict, g2, mat_name, 1, fun_type)
            show_alpha = "d-show"
        elif(ddlalphacut == "2"): #Alpha dash Cuts 
            t1 = "basic.avif"
            # alpha_cuts = [a1, a2, a3]   
            # alpha_cuts = ''
            alpha = [a1, a2, a3] #alpha_cuts
            # print(alpha_cuts)   
            alpha_dash_cuts = [a4, a5, a6]        
            # fn_dict_dash = GetFuns(alpha_dash_cuts)            
            if(ddlfuntion == '1'): # Trapezoidal
                fn_dict_dash = GetFuns2(alpha_dash_cuts,a_y,b_y,c_y,d_y,a_d,b_d,c_d,d_d,alpha)       
                # print("fn_dict_dash >>>: ",fn_dict_dash)         
                export_table_image(t2, "Table : α-α'-Cut",fn_dict_dash, alpha, alpha_dash_cuts)
            else: # Triangular
                fn_dict_dash = GetFunsTriangular2(alpha,alpha_dash_cuts,a_y,b_y,c_y,a_d,b_d,c_d)
                # print(fn_dict_dash)
                export_table_image(t2, "Table : α-α'-Cut",fn_dict_dash, alpha, alpha_dash_cuts)
                # print(fn_dict_dash)
            g4 = 'Bar_alpha_dash' + 'MF' + '.png' 
            g3 = GetBarChat2(alpha,alpha_dash_cuts, fn_dict_dash, g4, mat_name, 2, fun_type)
            show_alpha_dash = "d-show"
        return render_template('graph.html',fn_dict= fn_dict,alpha_cuts=alpha_cuts,alpha=alpha,alpha_dash_cuts=alpha_dash_cuts,fn_dict_dash=fn_dict_dash,g1=g1,g2=g2,g3=g3,g4=g4,a1=a1,a2=a2,a3=a3,a4=a4,a5=a5,a6=a6,s1=ddlmat_ID,s2=ddlfuntion,s3=ddlalphacut,materials=materials,show_alpha=show_alpha,show_alpha_dash=show_alpha_dash,t1=t1,t2=t2)
    
    return render_template('graph.html',g1=g1,g2=g2,g3=g3,g4=g4,s1=None)

# from AlphaDensity import alphaDensityFun
# from AlphaYoung import alphaYoungFun
from Trapezoidal import GetFuzzyFunction_aplha, GetFuzzyFunction_aplha_alpha_dash
from Triangular import GetFuzzyFunction_aplha2, GetFuzzyFunction_aplha_alpha_dash2
# from TriangularDensity import TriangularDensity
# from TriangularYoung import TriangularYoungFun
@app.route('/', methods=['GET', 'POST'])
def index():
    # alpha = [0.313, 0.455, 0.585]
    # materials = tbl_materials.query.filter_by(mat_status=1).all()  # Only active materials    
    g1 = g2 = g3 = g4 = 'basic.avif' # Default Graph Image
    if request.method=='POST':
        ddlfuntion = request.form.get('ddlfuntion') # id 
        materials = tbl_materials.query.filter(
        and_(
            tbl_materials.mat_status == 1,
            tbl_materials.mat_fm_id == ddlfuntion
        )).order_by(tbl_materials.mat_id).all()
        # Retrieve form data
        ddlmaterials = request.form.get('ddlmaterials') # id
        # print(ddlmaterials)        
        # material = request.form.get('material') # textbox
        material = '' # Not use
        if material.strip() != '':
            # Add Materials:
            msg = add_Materials(ddlmaterials,material)
            materials = tbl_materials.query.filter_by(mat_status=1).all()  # Only active materials
            return render_template('index.html', g1=g1,g2=g2,g3=g3,g4=g4,materials=materials,s1=ddlmaterials,s2=ddlfuntion,msg=msg)     
        else:            
            a1 = safe_float(request.form.get('alpha1'))
            a2 = safe_float(request.form.get('alpha2'))
            a3 = safe_float(request.form.get('alpha3'))
            a4 = safe_float(request.form.get('alpha_dash1'))
            a5 = safe_float(request.form.get('alpha_dash2'))
            a6 = safe_float(request.form.get('alpha_dash3'))   
            alpha_id = request.form.get('alpha_id') # its Disabled in html use for update id
            
            msg = add_Alpha(a1,a2,a3,a4,a5,a6,ddlfuntion,ddlmaterials)
            if(msg == "Record updated successfully!"):
                is_update = True
            else:
                is_update = False    
            # Create Alpha Graph
            g1 = 'Alpha_' + 'Density' + '.png'   
            g3 = 'Alpha_' + 'Young' + '.png' 
            g2 = 'Alpha_dash_' + 'Density' + '.png'  
            g4 = 'Alpha_dash_' + 'Young' + '.png' 
            material = tbl_materials.query.filter_by(mat_id=ddlmaterials).first()
            if material:
                mat_name = material.mat_name if material else None
                a_d = safe_float(material.mat_a_val_d)
                b_d = safe_float(material.mat_b_val_d)
                c_d = safe_float(material.mat_c_val_d)
                d_d = safe_float(material.mat_d_val_d)
                a_y = safe_float(material.mat_a_val_y)
                b_y = safe_float(material.mat_b_val_y)
                c_y = safe_float(material.mat_c_val_y)
                d_y = safe_float(material.mat_d_val_y)
                
            # material = tbl_materials.query.filter_by(mat_id=ddlmaterials).first()
            if(ddlfuntion == '1'): #Trapezoidal 
                # a, b, c, d = 2680, 2690, 2710, 2720  
                # alpha cut
                if a1 != '' and a2 != '' and a3 != '':
                    GetFuzzyFunction_aplha(a_d,b_d,c_d,d_d,a1,a2,a3,g1,mat_name,"Density")
                    GetFuzzyFunction_aplha(a_y,b_y,c_y,d_y,a1,a2,a3,g3,mat_name,"Young's Modulus")
                if a4 != '' and a5 != '' and a6 != '':                    
                    # alpha - alpha dash cut
                    GetFuzzyFunction_aplha_alpha_dash(a_d,b_d,c_d,d_d,a1,a2,a3,a4,a5,a6,g2,mat_name,"Density")
                    GetFuzzyFunction_aplha_alpha_dash(a_y,b_y,c_y,d_y,a1,a2,a3,a4,a5,a6,g4,mat_name,"Young's Modulus")                
            elif(ddlfuntion == '2'): #Triangular
                # a, b, c = 68947600000, 74456800000, 79966000000
                # a, b, c = 100000, 300000, 500000
                if a1 != '' and a2 != '' and a3 != '':
                    GetFuzzyFunction_aplha2(a_d,b_d,c_d,a1,a2,a3,g1,mat_name,"Density")
                    GetFuzzyFunction_aplha2(a_y,b_y,c_y,a1,a2,a3,g3,mat_name,"Young's Modulus")
                if a4 != '' and a5 != '' and a6 != '':                    
                    # alpha - alpha dash cut
                    GetFuzzyFunction_aplha_alpha_dash2(a_d,b_d,c_d,a1,a2,a3,a4,a5,a6,g2,mat_name,"Density")
                    GetFuzzyFunction_aplha_alpha_dash2(a_y,b_y,c_y,a1,a2,a3,a4,a5,a6,g4,mat_name,"Young's Modulus")                
                
            return render_template('index.html', g1=g1,g2=g2,g3=g3,g4=g4,a1=a1,a2=a2,a3=a3,a4=a4,a5=a5,a6=a6,materials=materials,s1=ddlmaterials,s2=ddlfuntion,alpha_id=alpha_id,is_update=is_update)     
    return render_template('index.html',g1=g1,g2=g2,g3=g3,g4=g4, s1=None)
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

@app.route('/get_material_data/<int:mat_id>/<int:fm_id>')
def get_material_data(mat_id,fm_id):
    # Fetch the first matching record for that material   
    alpha_record = tbl_materials.query.filter((tbl_materials.mat_fm_id == fm_id) & (tbl_materials.mat_id == mat_id)).first()
    if alpha_record:
        return {
            "a_val_d": alpha_record.mat_a_val_d,
            "b_val_d": alpha_record.mat_b_val_d,
            "c_val_d": alpha_record.mat_c_val_d,
            "d_val_d": alpha_record.mat_d_val_d,     
            "a_val_y": alpha_record.mat_a_val_y,
            "b_val_y": alpha_record.mat_b_val_y,
            "c_val_y": alpha_record.mat_c_val_y,
            "d_val_y": alpha_record.mat_d_val_y,       
        }
    else:
        return {}, 204  # No content found

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

@app.route('/get_alpha_data_cut/<int:mat_id>/<int:fm_id>/<int:cut_id>')
def get_alpha_data_cut(mat_id,fm_id,cut_id):
    # print("cut_id ========>>> ", cut_id)
    # Fetch the first matching record for that material
    alpha_record = tbl_alpha.query.filter((tbl_alpha.alpha_fm_id == fm_id) & (tbl_alpha.alpha_mat_id == mat_id)).first()
    if alpha_record:
        if cut_id == 1:
            return jsonify({
                "alpha1": alpha_record.alpha_alpha1,
                "alpha2": alpha_record.alpha_alpha2,
                "alpha3": alpha_record.alpha_alpha3,
                "cut_id": cut_id
            })
        elif cut_id == 2:
            return jsonify({
                "alpha1": alpha_record.alpha_alpha1,
                "alpha2": alpha_record.alpha_alpha2,
                "alpha3": alpha_record.alpha_alpha3,
                "alphadash1": alpha_record.alpha_alphadash1,
                "alphadash2": alpha_record.alpha_alphadash2,
                "alphadash3": alpha_record.alpha_alphadash3,
                # "alphadash11": f"{ alpha_record.alpha_alpha1}-{ alpha_record.alpha_alphadash1}",
                # "alphadash22": f"{alpha_record.alpha_alpha2 }-{ alpha_record.alpha_alphadash2}",
                # "alphadash33": f"{alpha_record.alpha_alpha3 }-{ alpha_record.alpha_alphadash3}",
                "cut_id": cut_id
            })
        else:
            return jsonify({"error": "Invalid cut_id"}), 400
    else:
        return {}, 204  # No content found

@app.route('/get_materials/<int:function_id>', methods=['GET'])
def get_materials(function_id):
    materials = tbl_materials.query.filter(
        and_(
            tbl_materials.mat_status == 1,
            tbl_materials.mat_fm_id == function_id
        )
    ).order_by(tbl_materials.mat_id).all()

    material_list = [
        {'mat_id': mat.mat_id, 'mat_name': mat.mat_name}
        for mat in materials
    ]

    return jsonify(material_list)
from export import export_images_to_excel
from werkzeug.utils import secure_filename
# @app.route('/export_excel/<string:file1>/<string:file2>')
# def export_excel(file1, file2):
#     try:
#         print(file1)
#         # Secure the filenames and create full paths
#         img1_path = os.path.join('static', 'img', secure_filename(file1))
#         img2_path = os.path.join('static', 'img', secure_filename(file2))
        
#         # Verify images exist
#         if not all([os.path.exists(img1_path), os.path.exists(img2_path)]):
#             return {"error": "One or both images not found"}, 404

#         # Create absolute path for temp Excel
#         output_path = os.path.abspath('temp_export.xlsx')
        
#         # Generate Excel
#         export_images_to_excel(
#             img1=img1_path,
#             img2=img2_path,
#             output_excel=output_path,
#             max_width=600,
#             max_height=400
#         )

#         # Verify Excel was created
#         if not os.path.exists(output_path):
#             return {"error": "Failed to create Excel file"}, 500

#         # Send file with proper headers
#         return send_file(
#             output_path,
#             as_attachment=True,
#             download_name='exported_data.xlsx',
#             mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
#             conditional=True
#         )

#     except Exception as e:
#         return {"error": f"Server error: {str(e)}"}, 500
        
#     finally:
#         # Clean up temp file
#         if os.path.exists(output_path):
#             try:
#                 os.remove(output_path)
#             except:
#                 pass

@app.route('/export_excel', methods=['POST'])
def export_excel():
    try:
        fn_dict = request.form.get('fn_dict')
        file1 = request.form.get('file1')
        # print("file1>>",file1)
        # print("fn_dict>>",fn_dict)
                    
        # Secure the filenames and create full paths
        img1_path = os.path.join('static', 'img', secure_filename(file1))
        img2_path = os.path.join('static', 'img', secure_filename(file1))
        
        # Verify images exist
        if not all([os.path.exists(img1_path), os.path.exists(img2_path)]):
            return {"error": "One or both images not found"}, 404

        # Create absolute path for temp Excel
        output_path = os.path.abspath('temp_export.xlsx')
        
        # Generate Excel
        export_images_to_excel(
            img1=img1_path,
            img2=img2_path,
            output_excel=output_path,
            max_width=600,
            max_height=400,
            fn_dict=fn_dict
        )

        # Verify Excel was created
        if not os.path.exists(output_path):
            return {"error": "Failed to create Excel file"}, 500

        # Send file with proper headers
        return send_file(
            output_path,
            as_attachment=True,
            download_name='exported_data.xlsx',
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            conditional=True
        )

    except Exception as e:
        return {"error": f"Server error: {str(e)}"}, 500
        
    finally:
        # Clean up temp file
        if os.path.exists(output_path):
            try:
                os.remove(output_path)
            except:
                pass


@app.route('/exportimage')
def exportimage():
    export_table_image("Alpha_Table.png",None,None)
    return "<h1>Tables image success.</h1>"

if __name__ == '__main__':
    # app.run(host="0.0.0.0", port=8000, debug=True)
    serve(app, host="0.0.0.0", port=8000, threads=8)
