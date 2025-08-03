#!/usr/bin/python3
"""Facade: Manages logic between API and Models for all resources."""
from app.models.review import Review
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.user import User
from app import bcrypt
from app.persistence.repository import SQLAlchemyRepository

class HBnBFacade: #new class for facade
    def __init__(self): #constructor
        self.user_repo = SQLAlchemyRepository(User)
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review)
        self.amenity_repo = SQLAlchemyRepository(Amenity)


    # Placeholder method for creating a user
    def create_user(self, data):
        # Extract the plaintext password
        plaintext = data.pop('password', None)
        if not plaintext or not isinstance(plaintext, str):
            raise ValueError("Password must be a non-empty string")

        # Instantiate your User with all other fields
        user = User(**data)

        # Hash the password and assign
        user.password = bcrypt.generate_password_hash(plaintext).decode('utf-8')

        # Check for duplicate email
        if self.get_user_by_email(user.email):
            raise ValueError("Email already registered")

        # Persist
        self.user_repo.add(user)
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
        return User.query.filter_by(email=email).first()

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
                "description": place.description,
                "price": place.price,
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

    def create_review(self, review_data):
        """
        Creates a Review object after validating user, place, and rating.
        """
        # Check required fields
        text = review_data.get("text")
        rating = review_data.get("rating")
        user_id = review_data.get("user_id")
        place_id = review_data.get("place_id")

        if not text or not isinstance(text, str):
            raise ValueError("Review text must be a non-empty string")

        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")

        user = self.user_repo.get(user_id)
        if not user:
            raise ValueError("User not found")

        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")

        # Create review
        review = Review(
            text=text,
            rating=rating,
            user_id=user.id,
            place_id=place.id
        )
        self.review_repo.add(review)
        return {
            "id":       review.id,
            "text":     review.text,
            "rating":   review.rating,
            "user_id":  review.user_id,
            "place_id": review.place_id
        }


    def get_review(self, review_id):
        """
        Retrieves a single review by its ID.
        Returns None if not found.
        """
        review = self.review_repo.get(review_id)
        if not review:
            return None

        return {
            "id": review.id,
            "text": review.text,
            "rating": review.rating,
            "user_id": review.user.id,
            "place_id": review.place.id
        }

    def get_all_reviews(self):
        """
        Returns a list of all reviews with basic information.
        """
        reviews = self.review_repo.get_all()
        return [
            {
                "id": review.id,
                "text": review.text,
                "rating": review.rating,
                "user_id": review.user.id,
                "place_id": review.place.id
            }
            for review in reviews
        ]

    def get_review_by_user_and_place(self, user_id, place_id):
        """
        Returns a review if the user has already reviewed the given place.
        Otherwise returns None
        """
        reviews = self.review_repo.get_all()
        for review in reviews:
            if review.user.id == user_id and review.place.id == place_id:
                return review
        return None

    def update_review(self, review_id, review_data):
        """
        Updates an existing review's text and rating after validation.
        """
        review = self.review_repo.get(review_id)
        if not review:
            return None  # Not found

        # Optional: update text
        if "text" in review_data:
            text = review_data["text"]
            if not isinstance(text, str) or not text.strip():
                raise ValueError("Review text must be a non-empty string")
            review.text = text.strip()

        # Optional: update rating
        if "rating" in review_data:
            rating = review_data["rating"]
            if not isinstance(rating, int) or not (1 <= rating <= 5):
                raise ValueError("Rating must be an integer between 1 and 5")
            review.rating = rating

        # Update storage (optional if object is mutable)
        self.review_repo.update(review_id, {
            "text": review.text,
            "rating": review.rating
        })

        return review

    def delete_review(self, review_id):
        """
        Deletes a review by ID.
        Returns True if successful, False if not found.
        """
        review = self.review_repo.get(review_id)
        if not review:
            return False

        self.review_repo.delete(review_id)
        return True

    def get_reviews_by_place(self, place_id):
        """
        Returns a list of all reviews for a specific place.
        """
        place = self.place_repo.get(place_id)
        if not place:
            return None  # Place not found

        reviews = self.review_repo.get_all()
        return [
            {
                "id": review.id,
                "text": review.text,
                "rating": review.rating,
                "user_id": review.user.id
            }
            for review in reviews if review.place.id == place_id
        ]
