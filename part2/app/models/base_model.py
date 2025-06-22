#!/usr/bin/python3

import uuid #generates universally unique ID
from datetime import datetime #gives access to current time for created or update

class BaseModel: #defined all other models will inherit from
    def __init__(self):
        self.id = str(uuid.uuid4()) #unique id converted to string for storing in text
        self.created_at = datetime.now()
        self.updated_at = datetime.now() # both store current time
        
    def save(self):
        """Update the updated_at timestamp to the current time."""
        self.updated_at = datetime.now() #method updates when obj is changed or saved
    
    def update(self, data): #method updates bj attributes using dict.
        for key, value in data.items(): #loop so we apply multi updates at once
            if hasattr(self, key): #check obj(self)has attrb named key
                setattr(self, key, value) #sets attrib on obj to the new value
        self.save() #refresh the timestamp
