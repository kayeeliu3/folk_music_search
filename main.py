from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Text, inspect
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv
import os
import json

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
class tunes(db.Model):
    tune_id = db.Column(db.Integer, primary_key = True)
    tune_name = db.Column(db.String)
    tune_key = db.Column(db.String)
    tune_type = db.Column(db.String)

    def __repr__(self):
        return f'<Tune {self.tune_name}>'
    
    # To help create JSON format
    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }

# Create database tables
# with app.app_context():
    # db.create_all()

### ENDPOINTS

@app.route('/')
def default_route():
    return render_template("index.html")

@app.route('/search', methods=['GET'])
def search_route():
    if request.method == 'GET': 
        all_tunes = tunes.query.all()
        print(all_tunes)
        return render_template("search.html", tunes = all_tunes)

@app.route('/favourites')
def favourites_route():
    return render_template("favourites.html")

### FUNCTIONS

def list_all_tunes():
    all_tunes = tunes.query.all()
    response = []
    for tune in all_tunes: 
        response = tune._mapping
    
    return response

if __name__ == "__main__":
    app.run(debug = False)
