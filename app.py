from flask import Flask, render_template, request , jsonify, send_file, redirect, url_for, flash, session
from waitress import serve
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
import os
from sqlalchemy import asc
import re
import bcrypt
from datetime import datetime
from sqlalchemy import text  # Import the text function

# app = Flask(__name__)
app = Flask(__name__, instance_relative_config=True)

# Path to database in instance folder
# db_path = os.path.join(app.instance_path, 'fuzzyfunction.db')
# print("Path :",db_path)
# Path : H:\BCA_Projects\GUI.Graph\instance\fuzzyfunction.db

load_dotenv() # Load variables from .env file
app.secret_key = os.getenv('SECRET_KEY')
# app.secret_key = secrets.token_hex(16)  # Generate a secure random SECRET_KEY
# os.chmod(app.instance_path, 0o755)  # Ensure proper permissions (Linux example)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fuzzyfunction.db'  # SQLite database file
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'fuzzyfunction.db')
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

class tbl_alpha_val(db.Model):
    av_id = db.Column(db.Integer, primary_key=True)
    av_alpha = db.Column(db.Float, nullable=False)
    av_status = db.Column(db.Integer, nullable=False) # 1: alpha & 2: alpha dash

# Define User model
class User(db.Model):
    __tablename__ = 'tbl_register'
    
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    username_email = db.Column(db.String(100), unique=True, nullable=False)
    is_email = db.Column(db.Boolean, nullable=False)
    password = db.Column(db.LargeBinary, nullable=False)
    user_phone = db.Column(db.LargeBinary, nullable=True)
    user_type = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# Initialize the database for Sqlite db
def init_db_1():
    """Initialize the database if it doesn't exist"""
    try:
        # Create instance folder if it doesn't exist
        os.makedirs(app.instance_path, exist_ok=True)
        
        db_file = os.path.join(app.instance_path, 'fuzzyfunction.db')
        
        # Check if database file exists and is accessible
        if not os.path.exists(db_file):
            print("Database not found. Creating new database...")
            # with app.app_context():
            #     db.create_all()
            init_db()
            print("Database created successfully.")
        else:
            print("Database exists and is ready.")
            
        # Verify database connection
        with app.app_context():
            # db.session.execute('SELECT 1').scalar()
            db.session.execute(text('SELECT 1')).scalar()  # Now using text()
            print("Database connection verified.")
            
    except Exception as e:
        print(f"Database initialization failed: {str(e)}")
        raise


@app.route('/init_db')
def init_db():
    try:
        with app.app_context():
             # Drop tbl_materials table if it exists
            tbl_materials.__table__.drop(db.engine, checkfirst=True)
            tbl_alpha_val.__table__.drop(db.engine, checkfirst=True)
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
            alpha_val_to_add = []
            alpha_val_to_add.append(tbl_alpha_val(av_alpha=0.1,av_status=1))
            alpha_val_to_add.append(tbl_alpha_val(av_alpha=0.2,av_status=1))
            alpha_val_to_add.append(tbl_alpha_val(av_alpha=0.3,av_status=1))
            alpha_val_to_add.append(tbl_alpha_val(av_alpha=0.4,av_status=1))
            alpha_val_to_add.append(tbl_alpha_val(av_alpha=0.5,av_status=1))
            alpha_val_to_add.append(tbl_alpha_val(av_alpha=0.6,av_status=1))
            alpha_val_to_add.append(tbl_alpha_val(av_alpha=0.7,av_status=1))
            alpha_val_to_add.append(tbl_alpha_val(av_alpha=0.8,av_status=1))
            alpha_val_to_add.append(tbl_alpha_val(av_alpha=0.9,av_status=1))

            alpha_val_to_add.append(tbl_alpha_val(av_alpha=0.11,av_status=2))
            alpha_val_to_add.append(tbl_alpha_val(av_alpha=0.22,av_status=2))
            alpha_val_to_add.append(tbl_alpha_val(av_alpha=0.33,av_status=2))
            alpha_val_to_add.append(tbl_alpha_val(av_alpha=0.44,av_status=2))
            alpha_val_to_add.append(tbl_alpha_val(av_alpha=0.55,av_status=2))
            alpha_val_to_add.append(tbl_alpha_val(av_alpha=0.66,av_status=2))
            alpha_val_to_add.append(tbl_alpha_val(av_alpha=0.77,av_status=2))
            alpha_val_to_add.append(tbl_alpha_val(av_alpha=0.88,av_status=2))
            alpha_val_to_add.append(tbl_alpha_val(av_alpha=0.99,av_status=2))
            # Add to session and commit to the database
            if materials_to_add or alpha_val_to_add:
                if materials_to_add:
                    db.session.add_all(materials_to_add)
                if alpha_val_to_add:
                    db.session.add_all(alpha_val_to_add)
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

from app_fn import GetFuns, GetFuns2, GetMinMax, GetMinMax2
from barchat import GetBarChat, GetBarChat2
from app_fn_triangular import GetFunsTriangular,GetFunsTriangular2, export_table_image,GetMinMax_Tri,GetMinMax_Tri2
@app.route('/graph', methods=['GET', 'POST'])
# @app.route('/graph')
def graph():    
    if 'user_id' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('login'))
    g1 = g2 = g3 = g4 = 'basic.avif' # Default Graph Image
    alpha = ''
    alpha_cuts = ''
    alpha_dash_cuts= ''
    fn_dict_dash = fn_dict = ''
    filename=''
    # materials = tbl_materials.query.filter_by(mat_status=1).all()  # Only active materials
    alpha_val1 = tbl_alpha_val.query.filter_by(av_status=1).order_by(asc(tbl_alpha_val.av_alpha)).all()
    alpha_val2 = tbl_alpha_val.query.filter_by(av_status=2).order_by(asc(tbl_alpha_val.av_alpha)).all()
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

            if(ddlfuntion == '1'): #Trapezoidal
                if mat_name == 'Aluminium':
                    filename = "TRAP_" + "AL"
                elif mat_name == 'Neoprene Rubber':
                    filename = "TRAP_" + "NR"
                elif mat_name == 'Teflon':
                    filename = "TRAP_" + "TF"
                elif mat_name == 'Nylon':
                    filename = "TRAP_" + "NL"
                elif mat_name == 'SS-304 Grade ABS Silicon':
                    filename = "TRAP_" + "SS304"
            if(ddlfuntion == '2'): #Triangular
                if mat_name == 'Aluminium':
                    filename = "TRIA_" + "AL"
                elif mat_name == 'Neoprene Rubber':
                    filename = "TRIA_" + "NR"
                elif mat_name == 'Teflon':
                    filename = "TRIA_" + "TF"
                elif mat_name == 'Nylon':
                    filename = "TRIA_" + "NL"
                elif mat_name == 'SS-304 Grade ABS Silicon':
                    filename = "TRIA_" + "SS304"
        # print("Material Name =====>>>>", mat_name)
        fun_type = ''
        if(ddlfuntion == '1'):   
            fun_type = "Trapezoidal" 
        else:
            fun_type = "Triangular"
        show_alpha="d-hide"
        show_alpha_dash="d-hide"
        t1 = filename + "_Alpha_Table.png"
        t2 = filename + "_Alpha_Table_Dash.png"
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
            g2 = filename + '_Bar_alpha' + '.png' 
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
            g4 = filename + '_Bar_alpha_dash' + '.png' 
            g3 = GetBarChat2(alpha,alpha_dash_cuts, fn_dict_dash, g4, mat_name, 2, fun_type)
            show_alpha_dash = "d-show"
        add_Alpha_val(a1, alpha_val1)
        add_Alpha_val(a2, alpha_val1)
        add_Alpha_val(a3, alpha_val1)
        alpha_val_to_add = []            
        for new_val in arr1:
            print(new_val)
            alpha_val_to_add.append(tbl_alpha_val(av_alpha=new_val,av_status=1))            
        add_Alpha_val2(a4, alpha_val2)
        add_Alpha_val2(a5, alpha_val2)
        add_Alpha_val2(a6, alpha_val2)
        for new_val2 in arr2:
            print(new_val2)
            alpha_val_to_add.append(tbl_alpha_val(av_alpha=new_val2,av_status=2))            
            # if alpha_val_to_add:
        if alpha_val_to_add:
            db.session.add_all(alpha_val_to_add)
            db.session.commit()
            print("Alpha added successfully.") 
            if len(arr1) > 0 :
                alpha_val1 = tbl_alpha_val.query.filter_by(av_status=1).order_by(asc(tbl_alpha_val.av_alpha)).all()
            if len(arr2) > 0 :
                alpha_val2 = tbl_alpha_val.query.filter_by(av_status=2).order_by(asc(tbl_alpha_val.av_alpha)).all()
        arr1.clear()
        arr2.clear()
        return render_template('graph.html',fn_dict= fn_dict,alpha_cuts=alpha_cuts,alpha=alpha,alpha_dash_cuts=alpha_dash_cuts,fn_dict_dash=fn_dict_dash,g1=g1,g2=g2,g3=g3,g4=g4,a1=a1,a2=a2,a3=a3,a4=a4,a5=a5,a6=a6,s1=ddlmat_ID,s2=ddlfuntion,s3=ddlalphacut,materials=materials,show_alpha=show_alpha,show_alpha_dash=show_alpha_dash,t1=t1,t2=t2,alpha_val1=alpha_val1,alpha_val2=alpha_val2)
    
    return render_template('graph.html',g1=g1,g2=g2,g3=g3,g4=g4,s1=None, alpha_val1=alpha_val1,alpha_val2=alpha_val2)

# from AlphaDensity import alphaDensityFun
# from AlphaYoung import alphaYoungFun
from Trapezoidal import GetFuzzyFunction_aplha, GetFuzzyFunction_aplha_alpha_dash
from Triangular import GetFuzzyFunction_aplha2, GetFuzzyFunction_aplha_alpha_dash2
# from TriangularDensity import TriangularDensity
# from TriangularYoung import TriangularYoungFun
@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'user_id' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('login'))
    fn_dict_dash = fn_dict = ''
    # materials = tbl_materials.query.filter_by(mat_status=1).all()  # Only active materials    
    g1 = g2 = g3 = g4 = 'basic.avif' # Default Graph Image
    alpha_val1 = tbl_alpha_val.query.filter_by(av_status=1).order_by(asc(tbl_alpha_val.av_alpha)).all()
    alpha_val2 = tbl_alpha_val.query.filter_by(av_status=2).order_by(asc(tbl_alpha_val.av_alpha)).all()
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
        # fn_dict = ''
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
            filename=''
            material = tbl_materials.query.filter_by(mat_id=ddlmaterials).first()
            if material:
                mat_name = material.mat_name if material else None            
                if(ddlfuntion == '1'): #Trapezoidal
                    if mat_name == 'Aluminium':
                        filename = "TRAP_" + "AL"
                    elif mat_name == 'Neoprene Rubber':
                        filename = "TRAP_" + "NR"
                    elif mat_name == 'Teflon':
                        filename = "TRAP_" + "TF"
                    elif mat_name == 'Nylon':
                        filename = "TRAP_" + "NL"
                    elif mat_name == 'SS-304 Grade ABS Silicon':
                        filename = "TRAP_" + "SS304"
                if(ddlfuntion == '2'): #Triangular
                    if mat_name == 'Aluminium':
                        filename = "TRIA_" + "AL"
                    elif mat_name == 'Neoprene Rubber':
                        filename = "TRIA_" + "NR"
                    elif mat_name == 'Teflon':
                        filename = "TRIA_" + "TF"
                    elif mat_name == 'Nylon':
                        filename = "TRIA_" + "NL"
                    elif mat_name == 'SS-304 Grade ABS Silicon':
                        filename = "TRIA_" + "SS304"
            # Create Alpha Graph
            g1 = filename + '_Alpha_' + 'Density' + '.png'   
            g3 = filename + '_Alpha_' + 'Young' + '.png' 
            g2 = filename + '_Alpha_dash_' + 'Density' + '.png'  
            g4 = filename + '_Alpha_dash_' + 'Young' + '.png' 
            
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
                # alpha_cuts = [0.3, 0.4, 0.5]
                # alpha cut
                alpha_cuts=[]
                if a1 != '' and a2 != '' and a3 != '':
                    alpha_cuts = [a1,a2,a3]
                    GetFuzzyFunction_aplha(a_d,b_d,c_d,d_d,a1,a2,a3,g1,mat_name,"Density")
                    GetFuzzyFunction_aplha(a_y,b_y,c_y,d_y,a1,a2,a3,g3,mat_name,"Young's Modulus")
                    fn_dict = GetMinMax(alpha_cuts,a_y,b_y,c_y,d_y,a_d,b_d,c_d,d_d)
                    print(fn_dict)
                if a4 != '' and a5 != '' and a6 != '':                    
                    # alpha - alpha dash cut
                    alpha_dash = [a4,a5,a6]
                    GetFuzzyFunction_aplha_alpha_dash(a_d,b_d,c_d,d_d,a1,a2,a3,a4,a5,a6,g2,mat_name,"Density")
                    GetFuzzyFunction_aplha_alpha_dash(a_y,b_y,c_y,d_y,a1,a2,a3,a4,a5,a6,g4,mat_name,"Young's Modulus")    
                    fn_dict_dash = GetMinMax2(alpha_cuts, a_y,b_y,c_y,d_y,a_d,b_d,c_d,d_d,alpha_dash)            
            elif(ddlfuntion == '2'): #Triangular
                # a, b, c = 68947600000, 74456800000, 79966000000
                # a, b, c = 100000, 300000, 500000
                if a1 != '' and a2 != '' and a3 != '':
                    alpha_cuts = [a1,a2,a3]
                    GetFuzzyFunction_aplha2(a_d,b_d,c_d,a1,a2,a3,g1,mat_name,"Density")
                    GetFuzzyFunction_aplha2(a_y,b_y,c_y,a1,a2,a3,g3,mat_name,"Young's Modulus")
                    fn_dict = GetMinMax_Tri(alpha_cuts,a_y,b_y,c_y,a_d,b_d,c_d)
                if a4 != '' and a5 != '' and a6 != '':                    
                    # alpha - alpha dash cut
                    alpha_dash = [a4,a5,a6]
                    GetFuzzyFunction_aplha_alpha_dash2(a_d,b_d,c_d,a1,a2,a3,a4,a5,a6,g2,mat_name,"Density")
                    GetFuzzyFunction_aplha_alpha_dash2(a_y,b_y,c_y,a1,a2,a3,a4,a5,a6,g4,mat_name,"Young's Modulus") 
                    fn_dict_dash = GetMinMax_Tri2(alpha_cuts, a_y,b_y,c_y,a_d,b_d,c_d,alpha_dash)                           
            # search_value = 0.51
            add_Alpha_val(a1, alpha_val1)
            add_Alpha_val(a2, alpha_val1)
            add_Alpha_val(a3, alpha_val1)
            alpha_val_to_add = []            
            for new_val in arr1:
                print(new_val)
                alpha_val_to_add.append(tbl_alpha_val(av_alpha=new_val,av_status=1))            
            add_Alpha_val2(a4, alpha_val2)
            add_Alpha_val2(a5, alpha_val2)
            add_Alpha_val2(a6, alpha_val2)
            for new_val2 in arr2:
                print(new_val2)
                alpha_val_to_add.append(tbl_alpha_val(av_alpha=new_val2,av_status=2))            
            # if alpha_val_to_add:
            if alpha_val_to_add:
                db.session.add_all(alpha_val_to_add)
                db.session.commit()
                print("Alpha added successfully.") 
                if len(arr1) > 0 :
                    alpha_val1 = tbl_alpha_val.query.filter_by(av_status=1).order_by(asc(tbl_alpha_val.av_alpha)).all()
                if len(arr2) > 0 :
                    alpha_val2 = tbl_alpha_val.query.filter_by(av_status=2).order_by(asc(tbl_alpha_val.av_alpha)).all()
            arr1.clear()
            arr2.clear()
            # exists = any(item.av_alpha == search_value for item in alpha_val1)
            # print(f"Does {search_value} exist? {exists}")
            return render_template('index.html', g1=g1,g2=g2,g3=g3,g4=g4,a1=a1,a2=a2,a3=a3,a4=a4,a5=a5,a6=a6,materials=materials,s1=ddlmaterials,s2=ddlfuntion,alpha_id=alpha_id,is_update=is_update,alpha_val1=alpha_val1,alpha_val2=alpha_val2, fn_dict=fn_dict,fn_dict_dash=fn_dict_dash)     
    return render_template('index.html',g1=g1,g2=g2,g3=g3,g4=g4, s1=None, alpha_val1=alpha_val1,alpha_val2=alpha_val2)
global arr1, arr2
# r1 = 0
arr1 = []
arr2 = []
def add_Alpha_val(search_val, alpha_val1):
    global arr1  # Declare globals inside the function to modify them
    exists = any(item.av_alpha == search_val for item in alpha_val1)
    if exists:
        print(f"Does {search_val} exist? {exists}")
    else:
        # print("Add new record.")
        arr1.append(search_val)
        
def add_Alpha_val2(search_val, alpha_val2):
    global arr2  # Declare globals inside the function to modify them
    exists = any(item.av_alpha == search_val for item in alpha_val2)
    if exists:
        print(f"Does {search_val} exist? {exists}")
    else:
        arr2.append(search_val)
        

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
from export import export_images_to_excel, export_images_to_excel2
from werkzeug.utils import secure_filename


@app.route('/export_excel', methods=['POST'])
def export_excel():
    try:
        fn_dict = request.form.get('fn_dict')
        file1 = request.form.get('file1')
        filetitle = request.form.get('filetitle')
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
            fn_dict=fn_dict,
            filetitle=filetitle
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

# From Index
@app.route('/export_excel2', methods=['POST'])
def export_excel2():
    try:
        fn_dict = request.form.get('fn_dict')
        fn_dict_dash = request.form.get('fn_dict_dash')
        file1 = request.form.get('file1')
        file2 = request.form.get('file2')
        file3 = request.form.get('file3')
        file4 = request.form.get('file4')
        filetitle = request.form.get('filetitle')
        # print("file1>>",file1)
        # print("fn_dict_dash>>",fn_dict_dash)
                    
        # Secure the filenames and create full paths
        img1_path = os.path.join('static', 'img', secure_filename(file1))
        img2_path = os.path.join('static', 'img', secure_filename(file2))
        img3_path = os.path.join('static', 'img', secure_filename(file3))
        img4_path = os.path.join('static', 'img', secure_filename(file4))
        
        # Verify images exist
        if not all([os.path.exists(img1_path), os.path.exists(img2_path)]):
            return {"error": "One or both images not found"}, 404

        # Create absolute path for temp Excel
        output_path = os.path.abspath('temp_export.xlsx')
        
        # Generate Excel
        export_images_to_excel2(
            img1=img1_path,
            img2=img2_path, img3=img3_path, img4=img4_path,
            output_excel=output_path,
            max_width=600,
            max_height=400,
            fn_dict=fn_dict,
            fn_dict_dash=fn_dict_dash,
            filetitle=filetitle
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

@app.route('/')
def index():
    return render_template('home.html', current_user=None)

@app.route('/', endpoint='contact')
def hello_world():
    return render_template('index.html', current_user=None)

@app.route('/profile', endpoint='profile')
def hello_world():
    return render_template('profile.html', current_user=None)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        full_name = request.form.get('full_name')
        username_email = request.form.get('username_email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        # master_password = request.form.get('master_password')
        
        # Validate form data
        if not all([full_name, username_email, password, confirm_password]):
            flash('All fields are required', 'error')
            return render_template('register.html')
        
        # Validate username/email format
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        is_email = bool(email_pattern.match(username_email))
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('register.html')
            
        # Check if user already exists
        existing_user = User.query.filter_by(username_email=username_email).first()
        
        if existing_user:
            flash('Username/Email already registered', 'error')
            return render_template('register.html')
            
        # Hash passwords
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        # hashed_master_password = bcrypt.hashpw(master_password.encode('utf-8'), bcrypt.gensalt()) if master_password else None
        
        # Create new user
        new_user = User(
            full_name=full_name,
            username_email=username_email,
            is_email=is_email,
            password=hashed_password,
            # master_password=hashed_master_password,
            user_type='user'
        )        
        # Insert user into database
        db.session.add(new_user)
        db.session.commit()        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))    
    return render_template('register.html', current_user=None)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_email = request.form.get('username_email')
        password = request.form.get('password')
        # master_password = request.form.get('master_password')
        
        if not all([username_email, password]):
            flash('All fields are required', 'error')
            return render_template('login.html')
        
        # Find user by username_email
        user = User.query.filter_by(username_email=username_email).first()
        
        # Check if user exists and passwords match
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password):
            # Create session for user
            session['user_id'] = user.id
            session['username_email'] = user.username_email
            session['name'] = user.full_name
            session['user_type'] = user.user_type
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials', 'error')
            return render_template('login.html')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    # init_db_1()
    # app.run(host="0.0.0.0", port=8000, debug=True)    
    serve(app, host="0.0.0.0", port=8000, threads=8)
