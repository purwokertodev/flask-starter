from datetime import datetime
from uuid import uuid4

from src.shared.base_domain import BaseDomain

class Foo(BaseDomain):
    def __init__(self, name, email, password):
        BaseDomain.__init__(self, str(uuid4()), datetime.now())

        self.name = name
        self.email = email
        self.password = password
    
    def display(self):
        return "Id : %s \nName : %s  \nEmail : %s \nCreated At : %s" % (self.id, self.name, self.email, str(self.created_at))
    
    def is_valid_password(self, password):
        return self.password == password
