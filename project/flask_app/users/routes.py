from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user, login_required, login_user, logout_user
import base64
from io import BytesIO
from .. import bcrypt
from werkzeug.utils import secure_filename
from ..forms import RegistrationForm, LoginForm, UpdateUsernameForm, UpdateProfilePicForm
from ..models import User

users = Blueprint("users", __name__)

""" ************ User Management views ************ """


# TODO: implement
@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("tasks.index"))
    registration_form = RegistrationForm()
    if request.method == "POST":
        if registration_form.validate_on_submit():
            username = registration_form.username.data
            email = registration_form.email.data
            password = registration_form.password.data
            hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
            user = User(username=username, email=email, password=hashed_password)
            user.save()
            return redirect(url_for("users.login"))
    return render_template("register.html", form=registration_form)


# TODO: implement
@users.route("/login", methods=["GET", "POST"])
def login():
    # if authenticated, redirect to home
    if current_user.is_authenticated:
        return redirect(url_for("tasks.index"))
    login_form = LoginForm()
    if request.method == "POST":
        if login_form.validate_on_submit():
            username = login_form.username.data
            password = login_form.password.data
            # check if user exists
            user = User.objects(username=username).first()
            # If they are successfully authenticated, redirect to their /account page.
            if (user is not None) and bcrypt.check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for("users.account"))
            else:
                flash("Login Unsuccessful. Please check username and password", "danger")
    return render_template("login.html", form=login_form)
    


# TODO: implement
@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("users.login"))


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    update_username_form = UpdateUsernameForm()
    update_profile_pic_form = UpdateProfilePicForm()
    if request.method == "POST":
        if update_username_form.submit_username.data and update_username_form.validate():
            # TODO: handle update username form submit
            new_username = update_username_form.username.data
            #update in db
            current_user.username = new_username
            current_user.save()

            

        if update_profile_pic_form.submit_picture.data and update_profile_pic_form.validate():
            # TODO: handle update profile pic form submit
            picture = update_profile_pic_form.picture.data
            # update ImageField in db
            current_user.profile_pic = picture
            current_user.save()
        # return redirect(url_for("users.account"))

    # TODO: handle get requests
    # if request.method == "GET":
        
    #     return render_template("account.html",
    #                            update_username_form=update_username_form,
    #                            update_profile_pic_form=update_profile_pic_form,
    #                            image=current_user.profile_pic)
    image = current_user.profile_pic
    if image:
        bytes_im = BytesIO(image.read())
        image = base64.b64encode(bytes_im.getvalue()).decode()
    return render_template("account.html",
                           update_username_form=update_username_form,
                           update_profile_pic_form=update_profile_pic_form,
                           image=image)

