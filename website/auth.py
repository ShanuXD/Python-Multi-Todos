from flask import Blueprint, render_template, request, flash
# "views" anme of the blueprint
auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["POST", "GET"])
def login():
    data = request.form
    print(data)
    return render_template("login.html")

@auth.route("/logout")
def logout():
    return "Logout"

@auth.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        name = request.form.get("name")
        password = request.form.get("password")
        cpassword = request.form.get("cpassword")

        print(email, password, cpassword, name)

        if len(email)<5:
            flash("Email length must be greater then 5 charaters", category="error")
        elif len(name)<5:
            flash("User name length must be greater then 5 charaters", category="error")
        elif password != cpassword:
            flash("Password not matched!", category="error")
        elif len(password)<5:
            flash("Password must be greater than 5 characters", category="error")
        else:
            flash("Account created", category="success")
    return render_template("signup.html",)