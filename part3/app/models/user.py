#!/usr/bin/python3

from app import db
from app import bcrypt
from app.models.base_model import BaseModel
from sqlalchemy.orm import validates
import re

class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    @validates('email')
    def validate_email(self, key, email):
        if not isinstance(email, str) or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Email must be a valid email address")
        return email

    @validates('first_name', 'last_name')
    def validate_name(self, key, value):
        if not isinstance(value, str) or len(value) > 50:
            raise ValueError(f"{key} must be a string up to 50 characters")
        return value

    @validates('is_admin')
    def validate_is_admin(self, key, value):
        if not isinstance(value, bool):
            raise ValueError("is_admin must be a boolean")
        return value

    def hash_password(self, password):
        """Hashes the password before saving."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Checks the password against the stored hash."""
        return bcrypt.check_password_hash(self.password, password)

    places = db.relationship('Place', backref='owner', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)
