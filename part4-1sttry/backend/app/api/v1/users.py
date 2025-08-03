#!/usr/bin/python3

from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new user"""
        user_data = api.payload
        current_user = get_jwt_identity()
        if not current_user.get("is_admin", False):
            return {"error": "Admin privileges required"}, 403

        if facade.get_user_by_email(user_data['email']):
            return {'error': 'Email already registered'}, 400

        try:
            new_user = facade.create_user(user_data)
        except ValueError as e:
            return {'error': str(e)}, 400

        return {
            'id': new_user.id,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'email': new_user.email
        }, 201

    def get(self):
        """Get list of all users"""
        users = facade.get_all_users()
        result = []
        for user in users:
            result.append({
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            })
        return result, 200
    
@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}, 200

    @api.expect(user_model, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input or email already registered')
    @jwt_required()
    def put(self, user_id):
        """Update a user by ID"""
        current_user = get_jwt_identity()
        
        user_data = api.payload
        is_admin = current_user.get("is_admin", False)

        # If not admin, enforce self-only access and no email/password update
        if not is_admin:
            if current_user["id"] != user_id:
                return {"error": "Unauthorized action"}, 403
            if 'email' in user_data or 'password' in user_data:
                return {"error": "You cannot modify email or password."}, 400
        else:
            # If admin is updating email, ensure uniqueness
            new_email = user_data.get("email")
            if new_email:
                existing_user = facade.get_user_by_email(new_email)
                if existing_user and existing_user.id != user_id:
                    return {"error": "Email already in use"}, 400

        try:
            updated_user = facade.update_user(user_id, user_data)
        except ValueError as e:
            return {'error': str(e)}, 400

        if not updated_user:
            return {'error': 'User not found'}, 404


        return {
            'id': updated_user.id,
            'first_name': updated_user.first_name,
            'last_name': updated_user.last_name,
            'email': updated_user.email
        }, 200
