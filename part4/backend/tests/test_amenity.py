from app.models.amenity import Amenity

def test_amenity_creation():
    amenity = Amenity(name="Wi-Fi")
    assert amenity.name == "Wi-Fi"
    assert hasattr(amenity, 'id')
    assert hasattr(amenity, 'created_at')
    assert hasattr(amenity, 'updated_at')
    print("Valid amenity creation passed.")

    try:
        Amenity(name="")  # invalid
    except ValueError:
        print("Empty name rejected as expected.")

    try:
        Amenity(name="x" * 51)  # invalid
    except ValueError:
        print("Long name rejected as expected.")

test_amenity_creation()
