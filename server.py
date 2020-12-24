from flask import Flask, jsonify
from flask_login import LoginManager, login_required
import psycopg2
import views
from database import Database
from desk import Desk
from user import get_user

try:
    conn = psycopg2.connect(user="postgres",
                            password="egf110",
                            host="127.0.0.1",
                            database="flashapp")
    cursor = conn.cursor()
except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)

lm = LoginManager()


@lm.user_loader
def load_user(user_id):
    return get_user(user_id)


def create_app():
    app = Flask(__name__)
    app.config.from_object("settings")

    app.add_url_rule("/", view_func=views.home_page)

    app.add_url_rule(
        "/login", view_func=views.login_page, methods=["GET", "POST"]
    )
    app.add_url_rule("/logout", view_func=views.logout_page)

    app.add_url_rule(
        "/desks", view_func=views.desks_page, methods=["GET", "POST"]
    )
    app.add_url_rule("/desks/<int:deskID>", view_func=views.desk_page)
    app.add_url_rule(
        "/desks/<int:deskID>/edit",
        view_func=views.desk_edit_page,
        methods=["GET", "POST"],
    )
    app.add_url_rule(
        "/new-desk", view_func=views.desk_add_page, methods=["GET", "POST"]
    )

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