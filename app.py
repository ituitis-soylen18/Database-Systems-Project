from flask import Flask, render_template
from flask_login import LoginManager

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    @app.route("/")
    def home_page():
        return render_template("home.html")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8080, debug=True)