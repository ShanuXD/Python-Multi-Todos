from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, logout_user, current_user

# "views" anme of the blueprint
auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["POST", "GET"])
def login():

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Incorrect password, try againg!", category="error")
        else:
            flash("Email does not exits!", category="error")

    return render_template("login.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        name = request.form.get("name")
        password = request.form.get("password")
        cpassword = request.form.get("cpassword")

        # print(email, password, cpassword, name)
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exits", category="error")
        elif len(email)<5:
            flash("Email length must be greater then 5 charaters", category="error")
        elif len(name)<5:
            flash("User name length must be greater then 5 charaters", category="error")
        elif password != cpassword:
            flash("Password not matched!", category="error")
        elif len(password)<5:
            flash("Password must be greater than 5 characters", category="error")
        else:
            new_user = User(name=name,
            password=generate_password_hash(password, method='sha256'),
            email=email)

            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Account created", category="success")
            return redirect(url_for("views.home"))

    return render_template("signup.html", user=current_user)