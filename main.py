from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

# Init database
class Base(DeclarativeBase):
    pass

# Assumes POSTGRES_URL string from .env in vercel
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('POSTGRES_WORKING')
app.config['SECRET_KEY'] = os.getenv('FLASK_KEY')
db = SQLAlchemy(model_class = Base)
db.init_app(app)

# MODEL TABLES
class Tune(db.Model):
    tune_id = db.Column(db.Integer, primary_key = True)
    tune_name = db.Column(db.String)
    tune_key = db.Column(db.String)
    tune_mode = db.Column(db.String)
    tune_type = db.Column(db.String)

# Create database tables
with app.app_context():
    db.create_all()

### ENDPOINTS

@app.route('/')
def default_route():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug = False)
