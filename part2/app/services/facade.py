#!/usr/bin/python3
"""Facade: Manages logic between API and Models for all resources."""
from app.models.user import User
from app.persistence.repository import InMemoryRepository

class HBnBFacade: #new class for facade
    def __init__(self): #constructor
        self.user_repo = InMemoryRepository() #memory stores
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # Placeholder method for creating a user
    def create_user(self, user_data):
        """
        Creates a User instance from provided data.
        Validates using the User constructor.
        Stores in the in-memory repository.
        """
        user = User(**user_data) # take keys from the dictionary and maps them to parameters
        self.user_repo.add(user) #stores the object inside the fake database
        return user
    
    def get_user(self, user_id):
        """
        Looks up a user by UUID.
        Returns None if not found.
        """
        return self.user_repo.get(user_id) #Look up a user in the in-memory store by ID.

    def get_user_by_email(self, email): #prevent duplicate registration
        """
        Searches for a user by email address.
        Uses internal attribute indexing in repository.
        """
        #looks through all stored users and returns the one with user.email == value
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        """Return list of all users"""
        return self.user_repo.all() #all:method from InMemoryRepository that returns all stored objects
    
    # Placeholder method for fetching a place by ID
    def get_place(self, place_id):
        pass
