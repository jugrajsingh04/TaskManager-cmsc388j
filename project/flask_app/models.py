from flask_login import UserMixin
from datetime import datetime
from . import db, login_manager


# TODO: implement
@login_manager.user_loader
def load_user(user_id):
    db_user = User.objects(username=user_id).first()
    return db_user

# TODO: implement fields
class User(db.Document, UserMixin):
    username = db.StringField(unique=True, required=True)
    email = db.StringField(unique=True, required=True)
    password = db.StringField(required=True)
    #profile pic if optional
    profile_pic = db.ImageField()

    # Returns unique string identifying our object
    def get_id(self):
        return self.username



# TODO: implement fields
class Task(db.Document):
    user = db.ReferenceField(User)
    task = db.StringField(max_length=500)
    date = db.DateTimeField(default=datetime.utcnow)
    completed = db.BooleanField(default=False)
    description = db.StringField(min_length=5, max_length=500)
    
    #Uncomment when other fields are ready for review pictures