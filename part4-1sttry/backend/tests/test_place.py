#!/usr/bin/python3

from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

def test_place_with_review_and_amenity():
    user = User(first_name="Alice", last_name="Smith", email="alice@example.com")
    place = Place(title="Seaside Cabin", price=120, latitude=45.0, longitude=-122.0, owner=user)
    
    review = Review(text="Great spot!", rating=4, place=place, user=user)
    place.add_review(review)

    amenity = Amenity(name="Wi-Fi")
    place.add_amenity(amenity)

    assert place.reviews[0].text == "Great spot!"
    assert place.amenities[0].name == "Wi-Fi"
    print("test_place_with_review_and_amenity passed!")

test_place_with_review_and_amenity()
