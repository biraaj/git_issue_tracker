from flask import Flask

#Intializing application
app = Flask(__name__)

#importing views
from app import views
