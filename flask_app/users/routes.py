from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user, login_required, login_user, logout_user
import base64,io
from .. import bcrypt
from werkzeug.utils import secure_filename
from ..forms import RegistrationForm, LoginForm, UpdateUsernameForm, UpdateProfilePicForm
from ..models import User

users = Blueprint("users", __name__)

""" ************ User Management views ************ """

def get_b64_img(username):
    user = User.objects(username=username).first()
    bytes_im = io.BytesIO(user.profile_pic.read())
    image = base64.b64encode(bytes_im.getvalue()).decode()
    return image

# TODO: implement
@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        
        return redirect(url_for('stocks.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password
        )
        new_user.save()

        flash('Your account has been created! You can log in the website now ', 'success')
        return redirect(url_for('users.login')) 

    return render_template('register.html', form=form)

# TODO: implement
@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated: 
        return redirect(url_for("stocks.index"))  

    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(username=form.username.data).first() 
        if user is not None and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Login successful!", "success") 
            return redirect(url_for("users.account")) 
        else:
            flash("Invalid username or password.", "error")

    return render_template("login.html", form=form)


# TODO: implement
@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('stocks.index'))


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    update_username_form = UpdateUsernameForm()
    update_profile_pic_form = UpdateProfilePicForm()

    if request.method == "POST":
        if update_username_form.submit_username.data and update_username_form.validate():
            new_username = update_username_form.username.data
            if User.objects(username=new_username).first():
                flash("Username already taken", "warning")
            else:
                current_user.modify(username=new_username)
                current_user.save()
                flash("Username updated successfully!", "success")
                return redirect(url_for("users.account"))

        if update_profile_pic_form.submit_picture.data and update_profile_pic_form.validate():
            img = update_profile_pic_form.picture.data
            filename = secure_filename(img.filename)
            content_type = f'images/{filename[-3:]}'

            if current_user.profile_pic.get() is None:
                current_user.profile_pic.put(img.stream, content_type=content_type)
            else:
                current_user.profile_pic.replace(img.stream, content_type=content_type)
            current_user.save()

            return redirect(url_for("users.account"))

    if current_user.profile_pic.get() is None:
        return render_template(
            "account.html", 
            update_username_form=update_username_form, 
            update_profile_pic_form=update_profile_pic_form
        )
    else:
        return render_template(
            "account.html", 
            update_username_form=update_username_form, 
            update_profile_pic_form=update_profile_pic_form,
            image=get_b64_img(current_user.username)
        )