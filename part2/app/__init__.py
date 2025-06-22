#!/usr/bin/python3

"""App Factory for HBnB Flask REST API."""

from flask import Flask
from app.api import api_bp  # import the modular blueprint from app/api/__init__.py

def create_app():
    """Creates and configures the Flask application."""
    app = Flask(__name__)
    app.register_blueprint(api_bp)  # register all namespaces through the blueprint
    return app
