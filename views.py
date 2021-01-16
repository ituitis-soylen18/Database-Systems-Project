from datetime import datetime
from flask import current_app, render_template, request, redirect, url_for, abort, flash
from flask_login import LoginManager, login_required, login_user, current_user, logout_user
from desk import Desk, Flashcard
from user import User
from forms import DeskEditForm, LoginForm, SigninForm, CardEditForm
from database import Database
from passlib.hash import pbkdf2_sha256 as hasher

def home_page():
    return render_template("home.html")


def desks_page():
    db = current_app.config["db"]
    if request.method == "POST":
        deskID = request.form["deskID"]
        db.delete_desk(int(deskID))
        flash("Desk deleted.")
        return redirect(url_for("desks_page"))
    desks = db.get_desks(current_user.userID)
    return render_template("desks.html", desks=sorted(desks))

def desk_page(deskID):
    db = current_app.config["db"]
    desk = db.get_desk(deskID)
    if desk is None:
        abort(404)
    if request.method == "POST":
        flashIDs = request.form.getlist("flashIDs")
        for flashID in flashIDs:
            db.delete_card(int(flashID), deskID)
        flash("%(num)d cards deleted." % {"num": len(flashIDs)})
        return redirect(url_for("desk_page", deskID=deskID))
    cards = db.get_cards(deskID)
    return render_template("desk.html", desk=desk, cards=cards, deskID=deskID)    

@login_required
def desk_add_page():
    form = DeskEditForm()
    if form.validate_on_submit():
        deskName = form.data["deskName"]
        db = current_app.config["db"]
        desk = Desk(deskName)
        deskID = db.add_desk(desk, current_user.userID)
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

@login_required
def card_page(flashID, deskID):
    db = current_app.config["db"]
    card = db.get_card(flashID)
    if card is None:
        abort(404)
    return render_template("card.html", card=card)

@login_required
def card_add_page(deskID):
    form = CardEditForm()
    if form.validate_on_submit():
        word = form.data["word"]
        translation = form.data["translation"]
        flashcard = Flashcard(word, translation)
        db = current_app.config["db"]
        flashID = db.add_card(flashcard, deskID)
        flash("Flashcard added.")
        return redirect(url_for("card_page", flashID=flashID, deskID=deskID))
    return render_template("card_edit.html", form=form)

@login_required
def card_edit_page(flashID, deskID):
    db = current_app.config["db"]
    card = db.get_card(flashID)
    form = CardEditForm()
    if form.validate_on_submit():
        word = form.data["word"]
        translation = form.data["translation"]
        flashcard = Flashcard(word, translation)
        db = current_app.config["db"]
        db.update_card(flashID, flashcard)
        flash("Flashcard data updated.")
        return redirect(url_for("card_page", flashID=flashID, deskID=deskID))
    form.word.data = card.word
    return render_template("card_edit.html", form=form)

@login_required
def study_page(deskID):
    db = current_app.config["db"]
    cards = db.get_cards(deskID)
    cardno = int(request.args.get('cardno',0))
    print("************",cardno)
    if request.method == "POST":
        return redirect(url_for("study_page", deskID=deskID, cardno=cardno+1))
    db.study_card(cards[cardno][0], current_user.userID)
    finished = (cardno >= len(cards)-1) 
    return render_template("study.html", card = cards[cardno][1], finished = finished, deskID=deskID)

def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        db = current_app.config["db"]
        username = form.data["username"]
        user = db.load_user(username)
        if user is not None:
            password = form.data["password"]
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
            #user = User(username, passwordHash, mail, firstName, lastName)
            db.add_user(username, passwordHash, mail, firstName, lastName)
            next_page = request.args.get("next", url_for("home_page"))
            return redirect(next_page)
    return render_template("signin.html", form=form)