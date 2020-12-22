from datetime import datetime
from flask import current_app, render_template, request, redirect, url_for, abort, flash
from flask_login import LoginManager, login_required, login_user, current_user, logout_user
from desk import Desk
from forms import DeskEditForm, LoginForm
from user import get_user
from passlib.hash import pbkdf2_sha256 as hasher

def home_page():
    today = datetime.today()
    day_name = today.strftime("%A")
    return render_template("home.html", day=day_name)


def desks_page():
    db = current_app.config["db"]
    if request.method == "GET":
        desks = db.get_desks()
        return render_template("desks.html", desks=sorted(desks))
    else:
        if not current_user.is_admin:
            abort(401)
        form_desk_keys = request.form.getlist("desk_keys")
        for form_desk_key in form_desk_keys:
            db.delete_desk(int(form_desk_key))
        flash("%(num)d desks deleted." % {"num": len(form_desk_keys)})
        return redirect(url_for("desks_page"))

def desk_page(desk_key):
    db = current_app.config["db"]
    desk = db.get_desk(desk_key)
    if desk is None:
        abort(404)
    return render_template("desk.html", desk=desk)

@login_required
def desk_add_page():
    if not current_user.is_admin:
        abort(401)
    form = DeskEditForm()
    if form.validate_on_submit():
        deskName = form.data["deskName"]
        db = current_app.config["db"]
        desk = Desk(deskName)
        desk_key = db.add_desk(desk)
        flash("Desk added.")
        return redirect(url_for("desk_page", desk_key=desk_key))
    return render_template("desk_edit.html", form=form)


@login_required
def desk_edit_page(desk_key):
    db = current_app.config["db"]
    desk = db.get_desk(desk_key)
    form = DeskEditForm()
    if form.validate_on_submit():
        deskName = form.data["deskName"]
        desk = Desk(deskName)
        db.update_desk(desk_key, desk)
        flash("Desk data updated.")
        return redirect(url_for("desk_page", desk_key=desk_key))
    form.deskName.data = desk.deskName
    return render_template("desk_edit.html", form=form)

def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.data["username"]
        user = get_user(username)
        if user is not None:
            password = form.data["password"]
            if hasher.verify(password, user.password):
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