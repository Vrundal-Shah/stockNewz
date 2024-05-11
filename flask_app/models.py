from flask_login import UserMixin
from datetime import datetime
from . import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.objects(username=user_id).first()  

class User(db.Document, UserMixin):
    username = db.StringField(required=True, min_length=1, max_length=40, unique=True)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True) 
    profile_pic = db.ImageField()
    # id of saved news articles
    saved_news = db.ListField(db.StringField(), default=list)
    favorite_tickers = db.ListField(db.StringField(), default=list)
    def get_id(self):
        return self.username
    
class Review(db.Document):
    commenter = db.ReferenceField(User, required=True)  
    content = db.StringField(required=True, min_length=5, max_length=500)
    date = db.StringField(required=True)  
    imdb_id = db.StringField(required=True, max_length=9)  
    movie_title = db.StringField(required=True, min_length=1, max_length=100)
    image = db.StringField() 
