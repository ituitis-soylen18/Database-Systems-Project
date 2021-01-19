from flask import Flask, current_app
from flask_login import LoginManager, login_required
import psycopg2
import views
from database import Database
from desk import Desk

try:
    conn = psycopg2.connect(user="gssdudqlhdjxwz",
                            password="e2e3da30ea18d59c2934fe42f8b6f4a0a276e375ea25223098ddeda63a32bc15",
                            host="ec2-54-78-127-245.eu-west-1.compute.amazonaws.com",
                            database="detmhspas3lfv2")
    cursor = conn.cursor()
except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)

lm = LoginManager()


@lm.user_loader
def load_user(username):
    db = current_app.config["db"]
    return db.load_user(username)


def create_app():
    app = Flask(__name__)
    app.config.from_object("settings")

    app.add_url_rule("/", view_func=views.home_page)
    app.add_url_rule(
        "/user", view_func=views.user_page, methods=["GET", "POST"]
    )
    app.add_url_rule(
        "/login", view_func=views.login_page, methods=["GET", "POST"]
    )
    app.add_url_rule(
        "/signin", view_func=views.signin_page, methods=["GET", "POST"]
    )
    app.add_url_rule("/logout", view_func=views.logout_page)
    app.add_url_rule(
        "/search", view_func=views.search_page, methods=["GET", "POST"]
    )
    app.add_url_rule(
        "/desks", view_func=views.desks_page, methods=["GET", "POST"]
    )
    app.add_url_rule("/desks/<int:deskID>", view_func=views.desk_page, methods=["GET", "POST"])
    app.add_url_rule(
        "/desks/<int:deskID>/edit",
        view_func=views.desk_edit_page,
        methods=["GET", "POST"],
    )
    app.add_url_rule(
        "/new-desk", view_func=views.desk_add_page, methods=["GET", "POST"]
    )
    app.add_url_rule("/desks/<int:deskID>/study", view_func=views.study_page, methods=["GET", "POST"])
    app.add_url_rule("/desks/<int:deskID>/add_card", view_func=views.card_add_page, methods=["GET", "POST"])
    app.add_url_rule("/desks/<int:deskID>/<int:flashID>", view_func=views.card_page, methods=["GET", "POST"])
    app.add_url_rule("/desks/<int:deskID>/<int:flashID>/edit", view_func=views.card_edit_page, methods=["GET", "POST"])
    app.add_url_rule("/words", view_func=views.words_page)
    lm.init_app(app)
    lm.login_view = "login_page"

    db = Database(conn)
    app.config["db"] = db

    return app


if __name__ == "__main__":
    app = create_app()
    port = app.config.get("PORT", 5000)
    app.run(host="0.0.0.0", port=port)

if (conn):
    cursor.close()
    conn.close()
    print("PostgreSQL connection is closed")