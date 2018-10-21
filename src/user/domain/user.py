import json
from datetime import datetime
from uuid import uuid4

from src.server.server import app, db, bcrypt

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, name, email, password, is_admin=False):

        self.id = str(uuid4())
        self.name = name
        self.email = email
        self.password = self.decode_password()
        self.created_at = datetime.now()
        self.is_admin = is_admin

    def decode_password(self):
        return bcrypt.generate_password_hash(
            self.password, app.config.get('BCRYPT_LOG_ROUNDS')).decode()
    
    def display(self):
        return "Id : %s \nName : %s  \nEmail : %s \nCreated At : %s" % (self.id, self.name, self.email, str(self.created_at))
    
    def is_valid_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
