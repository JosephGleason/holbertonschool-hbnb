#!/usr/bin/python3

"""App Factory for HBnB Flask REST API."""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config_class)

    # Initialize extensions with app
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Initialize API
    api = Api(
        app,
        version="1.0",
        title="HBnB API",
        description="HBnB Application API",
        doc="/api/v1/"
    )

    # Register namespaces here (AVOID importing from app.api directly)
    from app.api.v1.users import api as user_ns
    from app.api.v1.amenities import api as amenity_ns
    from app.api.v1.places import api as place_ns
    from app.api.v1.reviews import api as review_ns
    from app.api.v1.auth import api as auth_ns

    api.add_namespace(user_ns, path="/api/v1/users")
    api.add_namespace(amenity_ns, path="/api/v1/amenities")
    api.add_namespace(place_ns, path="/api/v1/places")
    api.add_namespace(review_ns, path="/api/v1/reviews")
    api.add_namespace(auth_ns, path="/api/v1/auth")

    # Auto-create tables + admin user
    with app.app_context():
        db.create_all()

        try:
            from app.services import facade

            admin = facade.get_user_by_email("admin@hbnb.com")
            if not admin:
                admin = facade.create_user({
                    "first_name": "Admin",
                    "last_name": "User",
                    "email": "admin@hbnb.com",
                    "password": "admin123"
                })
                admin.is_admin = True
                admin.save()
                print("✅ Admin created: admin@hbnb.com / admin123")
            else:
                if not admin.is_admin:
                    admin.is_admin = True
                    admin.save()
                print("✅ Admin ready: admin@hbnb.com / admin123")
        except Exception as e:
            print(f"⚠️  Admin user setup failed: {e}")

    return app
