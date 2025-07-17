from flask import Flask
from waitress import serve
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import and_
import os
# from sqlalchemy import asc
# import re
# import bcrypt
from datetime import datetime
from sqlalchemy import text  # Import the text function
# import time

# app = Flask(__name__)
app = Flask(__name__, instance_relative_config=True)

load_dotenv() # Load variables from .env file
app.secret_key = os.getenv('SECRET_KEY')
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
    mat_user_id = db.Column(db.Integer, nullable=False)

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
    alpha_user_id = db.Column(db.Integer, nullable=False)

class tbl_alpha_val(db.Model):
    av_id = db.Column(db.Integer, primary_key=True)
    av_alpha = db.Column(db.Float, nullable=False)
    av_status = db.Column(db.Integer, nullable=False) # 1: alpha & 2: alpha dash
    av_user_id = db.Column(db.Integer, nullable=False)

class tbl_member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    status = db.Column(db.Integer, nullable=False) # 1: alpha & 2: alpha dash
    user_id = db.Column(db.Integer, nullable=False)

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

class PasswordReset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('tbl_register.id'), nullable=False)
    token = db.Column(db.String(100), unique=True, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    used = db.Column(db.Boolean, default=False)
    user = db.relationship('User', backref=db.backref('reset_tokens', lazy=True))

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

# Import all routes
from routes import *

# @app.route('/abcd')
if __name__ == '__main__':
    # Online Site On Render.com
    # app.run(host="0.0.0.0", port=8000, debug=True)    
    serve(app, host="0.0.0.0", port=8000, threads=8)
