#!/usr/bin/python3
"""Facade: Manages logic between API and Models for all resources."""
from app.models.place import Place
from app.models.amenity import Amenity
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
        return self.user_repo.get_all() #all:method from InMemoryRepository that returns all stored objects
    
    def update_user(self, user_id, user_data):
        """
        Updates an existing user by ID with the given new data.
        """
        user = self.user_repo.get(user_id)
        if not user:
            return None  # user not found

        # Check if new email is already used
        if user.email != user_data['email']:
            existing = self.get_user_by_email(user_data['email'])
            if existing and existing.id != user.id:
                raise ValueError("Email already registered")

        # Update user fields
        user.first_name = user_data['first_name']
        user.last_name = user_data['last_name']
        user.email = user_data['email']
        self.user_repo.update(user_id, user_data)
        return user

    def create_amenity(self, amenity_data):
        """
        Creates an Amenity instance from the input dictionary
        """
        amenity = Amenity(**amenity_data) # take keys from the dictionary and maps them to parameters
        self.amenity_repo.add(amenity) #stores the object inside the fake database
        return amenity

    def get_amenity(self, amenity_id):
        """
        Retrieves a single amenity by its unique ID.
        Returns the Amenity object or None if not found.
        """
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """
        Returns a list of all Amenity objects currently stored.
        """
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """
        Updates an existing Amenity by ID with the given new data.
        """
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None  # Amenity not found

        new_name = amenity_data.get('name')
        if not isinstance(new_name, str) or not new_name.strip():
            raise ValueError("Amenity name must be a non-empty string")
        if len(new_name) > 50:
            raise ValueError("Amenity name must be at most 50 characters")

        amenity.name = new_name.strip()
        self.amenity_repo.update(amenity_id, {"name": amenity.name})
        return amenity
    
    def create_place(self, place_data):
        """
        Creates a Place object with validated owner and amenities.
        """

        # Validate owner
        owner = self.user_repo.get(place_data.get("owner_id"))
        if not owner:
            raise ValueError("Owner not found")

        # Validate amenities
        amenities = []
        for amenity_id in place_data.get("amenities", []):
            amenity = self.amenity_repo.get(amenity_id)
            if not amenity:
                raise ValueError(f"Amenity ID {amenity_id} not found")
            amenities.append(amenity)

        # Build Place (this will auto-validate title, price, lat/lng)
        place = Place(
            title=place_data["title"],
            description=place_data.get("description", ""),
            price=place_data["price"],
            latitude=place_data["latitude"],
            longitude=place_data["longitude"],
            owner=owner
        )

        # Add amenities to place
        for amenity in amenities:
            place.add_amenity(amenity)

        # Save to memory
        self.place_repo.add(place)
        return place


    def get_place(self, place_id):
        """
        Retrieves a place by ID, including owner and amenities.
        Returns None if not found.
        """
        place = self.place_repo.get(place_id)
        if not place:
            return None
        
        owner = place.owner
        owner_data = {
            "id": owner.id,
            "first_name": owner.first_name,
            "last_name": owner.last_name,
            "email": owner.email
        }
        
        amenities_data = []
        for amenity in place.amenities:
            amenities_data.append({
                "id": amenity.id,
                "name": amenity.name
            })

        return {
            "id": place.id,
            "title": place.title,
            "description": place.description,
            "price": place.price,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "owner": owner_data,
            "amenities": amenities_data
        }

    def get_all_places(self):
        """
        Retrieves a list of all places with basic location info.
        """
        places = self.place_repo.get_all()
        return [
            {
                "id": place.id,
                "title": place.title,
                "latitude": place.latitude,
                "longitude": place.longitude
            }
            for place in places
        ]

    def update_place(self, place_id, place_data):
        """
        Updates a place by ID with minimal required validation.
        """
        place = self.place_repo.get(place_id)
        if not place:
            return None

        # Validate and update price
        if "price" in place_data:
            price = place_data["price"]
            if not isinstance(price, (int, float)) or price < 0:
                raise ValueError("Price must be a non-negative number")
            place.price = float(price)

        # Validate and update latitude
        if "latitude" in place_data:
            lat = place_data["latitude"]
            if not isinstance(lat, (int, float)) or not -90 <= lat <= 90:
                raise ValueError("Latitude must be between -90 and 90")
            place.latitude = float(lat)

        # Validate and update longitude
        if "longitude" in place_data:
            lon = place_data["longitude"]
            if not isinstance(lon, (int, float)) or not -180 <= lon <= 180:
                raise ValueError("Longitude must be between -180 and 180")
            place.longitude = float(lon)

        # Validate and update amenities
        if "amenities" in place_data:
            new_amenities = []
            for amenity_id in place_data["amenities"]:
                amenity = self.amenity_repo.get(amenity_id)
                if not amenity:
                    raise ValueError(f"Amenity ID {amenity_id} not found")
                new_amenities.append(amenity)
            place.amenities = new_amenities

        return place

