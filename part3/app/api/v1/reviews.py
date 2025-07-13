#!/usr/bin/python3

"""Review API endpoints using Flask-RESTx."""
from flask import request
from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade
from flask_jwt_extended import jwt_required, get_jwt_identity


# Define the namespace for reviews
reviews_ns = Namespace('reviews', description='Operations related to reviews')

# Input model for creating or updating a review
review_input = reviews_ns.model('ReviewInput', {
    'text': fields.String(required=True, description='Review text'),
    'rating': fields.Integer(required=True, description='Rating between 1 and 5'),
    'place_id': fields.String(required=True, description='UUID of the place')
})

# Output model for returning a review
review_output = reviews_ns.model('ReviewOutput', {
    'id': fields.String(readonly=True),
    'text': fields.String,
    'rating': fields.Integer,
    'user_id': fields.String,
    'place_id': fields.String
})

facade = HBnBFacade()

@reviews_ns.route('/')
class ReviewList(Resource):
    @reviews_ns.marshal_list_with(review_output)
    def get(self):
        """Get all reviews"""
        return facade.get_all_reviews()

    @reviews_ns.expect(review_input)
    @reviews_ns.marshal_with(review_output, code=201)
    @jwt_required()
    def post(self):
        """Create a new review"""
        current_user = get_jwt_identity()
        data = request.get_json()
        data['user_id'] = current_user['id']

        # Step 1: Get the place
        place = facade.get_place(data['place_id'])
        if not place:
            return {"error": "Place not found"}, 404

        # Step 2: Check ownership
        if place["owner"]["id"] == current_user["id"]:
            return {"error": "You cannot review your own place."}, 400

        # Step 3: Check for existing review by this user for this place
        existing_review = facade.get_review_by_user_and_place(current_user["id"], data['place_id'])
        if existing_review:
            return {"error": "You have already reviewed this place."}, 400

        # Step 4: Create the review
        return facade.create_review(data), 201



@reviews_ns.route('/<string:review_id>')
@reviews_ns.param('review_id', 'The review identifier')
class ReviewResource(Resource):
    @reviews_ns.marshal_with(review_output)
    def get(self, review_id):
        """Get a single review"""
        review = facade.get_review(review_id)
        if not review:
            reviews_ns.abort(404, "Review not found")
        return review

    @reviews_ns.expect(review_input)
    @reviews_ns.marshal_with(review_output)
    @jwt_required()
    def put(self, review_id):
        """Update a review"""
        current_user = get_jwt_identity()
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404

        if review["user_id"] != current_user["id"]:
            return {"error": "Unauthorized action"}, 403
        
        data = request.get_json()
        updated = facade.update_review(review_id, data)
        if not updated:
            reviews_ns.abort(404, "Review not found")
        return updated

    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        current_user = get_jwt_identity()
        review = facade.get_review(review_id)

        if not review:
            return {"error": "Review not found"}, 404

        if review["user_id"] != current_user["id"]:
            return {"error": "Unauthorized action"}, 403

        facade.delete_review(review_id)
        return {"message": "Review deleted"}, 200



@reviews_ns.route('/place/<string:place_id>')
@reviews_ns.param('place_id', 'The place identifier')
class PlaceReviews(Resource):
    @reviews_ns.marshal_list_with(review_output)
    def get(self, place_id):
        """Get all reviews for a specific place"""
        reviews = facade.get_reviews_by_place(place_id)
        if reviews is None:
            reviews_ns.abort(404, "Place not found")
        return reviews

@reviews_ns.route('/place/<string:place_id>/new')
@reviews_ns.param('place_id', 'The place identifier')
class ReviewToPlace(Resource):
    @reviews_ns.expect(reviews_ns.model('ReviewToPlaceInput', {
        'text': fields.String(required=True),
        'rating': fields.Integer(required=True),
        'user_id': fields.String(required=True)
    }))
    
    @reviews_ns.marshal_with(review_output, code=201)
    @jwt_required()
    def post(self, place_id):
        """Create a review for a specific place"""
        current_user = get_jwt_identity()
        data = request.get_json()
        data['user_id'] = current_user["id"]
        
        #get place and check ownership
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        if place.owner_id == current_user["id"]:
            return {"error": "You cannot review your own place."}, 400

        #check for duplicates
        existing_review = facade.get_review_by_user_and_place(current_user["id"], data['place_id'])
        if existing_review:
            return {"error": "You have already reviewed this place."}, 400

        data = request.get_json()
        data['place_id'] = place_id
        return facade.create_review(data), 201
api = reviews_ns
