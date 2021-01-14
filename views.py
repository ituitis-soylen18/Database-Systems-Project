from datetime import datetime
from flask import current_app, render_template, request, redirect, url_for, abort, flash
from flask_login import LoginManager, login_required, login_user, current_user, logout_user
from desk import Desk
from user import User
from forms import DeskEditForm, LoginForm, SigninForm
from database import Database
from passlib.hash import pbkdf2_sha256 as hasher

def home_page():
    return render_template("home.html")


def desks_page():
    db = current_app.config["db"]
    if request.method == "GET":
        desks = db.get_desks()
        return render_template("desks.html", desks=sorted(desks))
    else:
        if not current_user.is_admin:
            abort(401)
        form_deskIDs = request.form.getlist("deskIDs")
        for form_deskID in form_deskIDs:
            db.delete_desk(int(form_deskID))
        flash("%(num)d desks deleted." % {"num": len(form_deskIDs)})
        return redirect(url_for("desks_page"))

def desk_page(deskID):
    db = current_app.config["db"]
    desk = db.get_desk(deskID)
    if desk is None:
        abort(404)
    return render_template("desk.html", desk=desk)

@login_required
def desk_add_page():
    # if not current_user.is_admin:
    #     abort(401)
    form = DeskEditForm()
    if form.validate_on_submit():
        deskName = form.data["deskName"]
        db = current_app.config["db"]
        desk = Desk(deskName)
        deskID = db.add_desk(desk, current_user.userID)
        print("----------------------",deskID)
        flash("Desk added.")
        return redirect(url_for("desk_page", deskID=deskID))
    return render_template("desk_edit.html", form=form)


@login_required
def desk_edit_page(deskID):
    db = current_app.config["db"]
    desk = db.get_desk(deskID)
    form = DeskEditForm()
    if form.validate_on_submit():
        deskName = form.data["deskName"]
        desk = Desk(deskName)
        db.update_desk(deskID, desk)
        flash("Desk data updated.")
        return redirect(url_for("desk_page", deskID=deskID))
    form.deskName.data = desk.deskName
    return render_template("desk_edit.html", form=form)

def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        db = current_app.config["db"]
        username = form.data["username"]
        user = db.load_user(username)
        if user is not None:
            print("------usernotnone---passed------")
            password = form.data["password"]
            print("-----password-----", password)
            if hasher.verify(password, user.passwordHash):
                login_user(user)
                flash("You have logged in.")
                next_page = request.args.get("next", url_for("home_page"))
                return redirect(next_page)
        flash("Invalid credentials.")
    return render_template("login.html", form=form)


def logout_page():
    logout_user()
    flash("You have logged out.")
    return redirect(url_for("home_page"))

def signin_page():
    form = SigninForm()
    if form.validate_on_submit():
        db = current_app.config["db"]
        username = form.data["username"]
        mail = form.data["mail"]
        if db.check_username(username):
            flash("Username already taken.")
        elif db.check_usermail(mail):
            flash("There is an already registered account with given mail address.")
        else:
            passwordHash =  hasher.hash(form.data["password"])
            firstName = form.data["firstName"]
            lastName = form.data["lastName"]
            user = User(username, passwordHash, mail, firstName, lastName)
            db.add_user(user)
            next_page = request.args.get("next", url_for("home_page"))
            return redirect(next_page)
    return render_template("signin.html", form=form)