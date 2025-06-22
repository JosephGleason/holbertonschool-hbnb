#!/usr/bin/python3

from app.models.base_model import BaseModel #imports id, created,update, and update methods
import re #regular expression module. validate proper email format

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__() #constructor from BaseModel. Gives us id, created_at, and updated_at fields.
        
        #validate first name
        if not isinstance(first_name, str) or len(first_name) > 50:
            raise ValueError("First name must be up to 50 characters")
        self.first_name = first_name
        
        #validate second name
        if not isinstance(last_name, str) or len(last_name) > 50:
            raise ValueError("Last name must be up to 50 characters")
        self.last_name = last_name

        #validate email
        if not isinstance(email, str) or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Email must be a valid email address")
        self.email = email

        #validate if admin
        if not isinstance(is_admin, bool):
            raise ValueError("is_admin must be a boolean")
        self.is_admin = is_admin
