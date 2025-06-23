#!/usr/bin/python3

from flask import Blueprint
from flask_restx import Api

from app.api.v1.users import api as user_ns
from app.api.v1.amenities import api as amenity_ns #import the new namespace
from app.api.v1.places import api as place_ns
from app.api.v1.reviews import reviews_ns

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(api_bp, title='HBnB API', version='1.0', description='HBnB API documentation')

# Register namespaces
api.add_namespace(user_ns, path='/users')
api.add_namespace(amenity_ns, path='/amenities')  # register amenities namespace
api.add_namespace(place_ns, path='/places')
api.add_namespace(reviews_ns, path='/reviews')
