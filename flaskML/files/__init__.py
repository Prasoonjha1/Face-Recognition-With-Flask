from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import numpy as np
import config

config.nameList = np.load('data2.npy')
config.encodeListForKnown = np.load('data.npy')
config.classNames = np.load('data1.npy')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///service.db'
app.config['SECRET_KEY'] = '351047ae3ff7b8e1eace8197'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
from files import routes