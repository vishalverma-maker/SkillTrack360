from flask import Flask, redirect, url_for

from flask_login import LoginManager, login_required, current_user

from config import Config

from models import db

from models.user import User
from models.trainee import Trainee

from routes.auth import auth_bp
from routes.trainee import trainee_bp
from routes.government import government_bp
from models.trainee import Trainee

def create_app():

    # =========================================
    # CREATE FLASK APP
    # =========================================

    app = Flask(__name__)

    # Load configuration
    app.config.from_object(Config)


    # =========================================
    # FLASK-LOGIN SETUP
    # =========================================

    login_manager = LoginManager()

    # Where users should be sent if they
    # try to access a protected page
    # without logging in.

    login_manager.login_view = "auth.login"

    # Connect Flask-Login to our Flask app
    login_manager.init_app(app)


    # Tell Flask-Login how to load a user
    # from the ID stored in the login session.

    @login_manager.user_loader
    def load_user(user_id):

        return db.session.get(
            User,
            int(user_id)
        )


    # =========================================
    # DATABASE SETUP
    # =========================================

    db.init_app(app)


    # =========================================
    # REGISTER BLUEPRINTS
    # =========================================

    # Signup / Login / Logout
    app.register_blueprint(auth_bp)

    # Trainee dashboard
    app.register_blueprint(trainee_bp)

    # Government dashboard
    app.register_blueprint(government_bp)


    # =========================================
    # CREATE DATABASE TABLES
    # =========================================

    with app.app_context():

        db.create_all()


        # =====================================
        # CREATE DEMO GOVERNMENT ACCOUNT
        # =====================================

        government_user = User.query.filter_by(
            email="government@skilltrack.com"
        ).first()


        if not government_user:

            government_user = User(

                email="government@skilltrack.com",

                phone=None,

                role="government"

            )

            government_user.set_password(
                "Gov@12345"
            )

            db.session.add(
                government_user
            )

            db.session.commit()

        # Seed synthetic demo data when database is empty
        if Trainee.query.count() == 0:
            from seed_demo import seed_demo_data
            seed_demo_data()
    # =========================================
    # HOME ROUTE
    # =========================================

    @app.route("/")
    @login_required
    def home():

        # -------------------------------------
        # GOVERNMENT USER
        # -------------------------------------

        if current_user.role == "government":

            return redirect(
                url_for(
                    "government.dashboard"
                )
            )


        # -------------------------------------
        # TRAINEE USER
        # -------------------------------------

        return redirect(
            url_for(
                "trainee.dashboard"
            )
        )


    return app


# =============================================
# CREATE APPLICATION
# =============================================

app = create_app()


# =============================================
# RUN SERVER
# =============================================

if __name__ == "__main__":

    app.run(
        debug=True
    )