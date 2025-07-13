#!/usr/bin/python3

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('auth', description='Authentication operations')

# Input model for login credentials
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        """Authenticate user and return a JWT token"""
        credentials = api.payload

        #retrieves the user by email
        user = facade.get_user_by_email(credentials['email'])

        #verify user exists and password match
        if not user or not user.verify_password(credentials['password']):
            return {'error': 'Invalid credentials'}, 401

        #create JWT token with userid and is admin
        access_token = create_access_token(identity={
            'id': str(user.id),
            'is_admin': user.is_admin
        })

        return {'access_token': access_token}, 200

@api.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        """A protected endpoint that requires a valid JWT token"""
        current_user = get_jwt_identity()
        return {'message': f'Hello, user {current_user["id"]}'}, 200
