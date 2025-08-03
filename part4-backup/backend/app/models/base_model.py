#!/usr/bin/python3

from app import db
import uuid #generates universally unique ID
from datetime import datetime, timezone #gives access to current time for created or update

class BaseModel(db.Model): #defined all other models will inherit from
    __abstract__ = True

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc),
                           onupdate=lambda: datetime.now(timezone.utc))
        
    def save(self):
        """Update the updated_at timestamp to the current time."""
        self.updated_at = datetime.now(timezone.utc) #method updates when obj is changed or saved
        db.session.commit()
        
    def update(self, data): #method updates bj attributes using dict.
        for key, value in data.items(): #loop so we apply multi updates at once
            if hasattr(self, key): #check obj(self)has attrb named key
                setattr(self, key, value) #sets attrib on obj to the new value
        self.save() #refresh the timestamp
