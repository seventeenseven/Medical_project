import random
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = random._urandom(56)

#Database Connection
db_info = {
    'host':'localhost',
    'database':'medical',
    'psw':'alex1997+',
    'user':'postgres'
    }

app.config['SQLALCHEMY_DATABASE_URI']= f"postgres://" \
                                       f"{db_info['user']}:{db_info['psw']}@{db_info['host']}/{db_info['database']}"  #instructions on the db connection
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False  #to not be bother by some warnings

#Databse Representation
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)

from app import models, routes