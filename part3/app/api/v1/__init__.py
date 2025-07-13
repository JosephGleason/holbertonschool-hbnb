#!/usr/bin/python3
"""Initializes API v1 namespaces and documentation."""
from flask import Blueprint
from flask_restx import Api

from .users import api as user_ns
from .amenities import api as amenity_ns

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(api_bp, title='HBnB API', version='1.0', description='HBnB API documentation')

# Register namespaces
api.add_namespace(user_ns, path='/users')
api.add_namespace(amenity_ns, path='/amenities')
