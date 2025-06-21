#!/usr/bin/python3

from app.persistence.repository import InMemoryRepository

class HBnBFacade: #new class for facade
    def __init__(self): #constructor
        self.user_repo = InMemoryRepository() #memory stores
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # Placeholder method for creating a user
    def create_user(self, user_data):
        pass

    # Placeholder method for fetching a place by ID
    def get_place(self, place_id):
        pass
