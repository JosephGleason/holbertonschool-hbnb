#!/usr/bin/python3

"""App Factory for HBnB Flask REST API."""

from flask import Flask
from app.api import api_bp  # import the modular blueprint from app/api/__init__.py
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

jwt = JWTManager()
db = SQLAlchemy()

def create_app(config_class="config.DevelopmentConfig"):
    """Creates and configures the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config_class)  # register all namespaces through the blueprint
    
    jwt.init_app(app) #initialize JWT with config
    
    app.register_blueprint(api_bp)
    return app
