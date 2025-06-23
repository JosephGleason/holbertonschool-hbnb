#!/usr/bin/python3

"""Review API endpoints using Flask-RESTx."""
from flask import request
from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

# Define the namespace for reviews
reviews_ns = Namespace('reviews', description='Operations related to reviews')

# Input model for creating or updating a review
review_input = reviews_ns.model('ReviewInput', {
    'text': fields.String(required=True, description='Review text'),
    'rating': fields.Integer(required=True, description='Rating between 1 and 5'),
    'user_id': fields.String(required=True, description='UUID of the user'),
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
    def post(self):
        """Create a new review"""
        data = request.get_json()
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
    def put(self, review_id):
        """Update a review"""
        data = request.get_json()
        updated = facade.update_review(review_id, data)
        if not updated:
            reviews_ns.abort(404, "Review not found")
        return updated

    def delete(self, review_id):
        """Delete a review"""
        deleted = facade.delete_review(review_id)
        if not deleted:
            reviews_ns.abort(404, "Review not found")
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
    def post(self, place_id):
        """Create a review for a specific place"""
        data = request.get_json()
        data['place_id'] = place_id
        return facade.create_review(data), 201
