from ast import Pass
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, DateField
from wtforms.validators import (
    InputRequired,
    Length,
    Email,
    EqualTo,
    ValidationError,
)
from datetime import datetime, timedelta


from .models import User


class SearchForm(FlaskForm):
    ticker = StringField(
        "Ticker", validators=[InputRequired(), Length(min=1, max=100)]
    )
    start_date = DateField(
        "Start Date", 
        format='%Y-%m-%d', 
        validators=[InputRequired()], 
        default=(datetime.utcnow() - timedelta(days=2)).date()
    )
    end_date = DateField(
        "End Date", format='%Y-%m-%d', validators=[InputRequired()],
        default=datetime.utcnow().date()
    )
    submit = SubmitField("Search")


class MovieReviewForm(FlaskForm):
    text = TextAreaField(
        "Comment", validators=[InputRequired(), Length(min=5, max=500)]
    )
    submit = SubmitField("Enter Comment")


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[InputRequired(), Length(min=1, max=40)]
    )
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[InputRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError("Username is taken")

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user is not None:
            raise ValidationError("Email is taken")


# TODO: implement fields
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=1, max=40)])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Log In')

    
class UpdateUsernameForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=1, max=40)])
    submit_username = SubmitField('Update Username')

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError('Username is already taken. Please choose a different one.')

class UpdateProfilePicForm(FlaskForm):
    picture = FileField('Profile Picture', validators=[
        FileRequired(), 
        FileAllowed(['jpg', 'png'], 'Only JPG and PNG images are allowed.')
    ])
    submit_picture = SubmitField('Update Profile Picture')

class SaveTickerForm(FlaskForm):
    ticker1 = StringField('Ticker Symbol 1', validators=[InputRequired(), Length(min=1, max=10)])
    ticker2 = StringField('Ticker Symbol 2', validators=[InputRequired(), Length(min=1, max=10)])
    ticker3 = StringField('Ticker Symbol 3', validators=[InputRequired(), Length(min=1, max=10)])
    submit_tickers = SubmitField('Save Tickers')
