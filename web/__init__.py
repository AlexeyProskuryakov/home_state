# coding:utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

__author__ = '4ikist'

app = Flask('home_state')
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'super-secret'
app.config['CSRF_ENABLED'] = True

db = SQLAlchemy(app)
