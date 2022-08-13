from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    load_dotenv()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:sql@localhost:5432/TransFEPostgre'
    db.init_app(app)
    return app

db = SQLAlchemy(create_app())