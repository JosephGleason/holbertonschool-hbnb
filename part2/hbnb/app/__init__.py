#!/usr/bin/python3

#import flask class to make flask web app
from flask import Flask
#import api class from restx to org and doc rest api
from flask_restx import Api

#func app factory builds app
def create_app():
    app = Flask(__name__) #Flask class from flask framework
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/')
    
    return app
