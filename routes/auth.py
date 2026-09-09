from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_user,
    logout_user,
    login_required
)

from models import db
from models.user import User
from models.trainee import Trainee


auth_bp = Blueprint("auth", __name__)


# =========================================================
# SIGNUP
# =========================================================

@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        # -------------------------------------------------
        # GET FORM DATA
        # -------------------------------------------------

        full_name = request.form.get(
            "full_name",
            ""
        ).strip()

        phone = request.form.get(
            "phone",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        confirm_password = request.form.get(
            "confirm_password",
            ""
        )

        consent = request.form.get("consent")


        # -------------------------------------------------
        # VALIDATION
        # -------------------------------------------------

        if not full_name:

            flash(
                "Full name is required."
            )

            return redirect(
                url_for("auth.signup")
            )


        if not phone and not email:

            flash(
                "Please provide either a mobile number or email."
            )

            return redirect(
                url_for("auth.signup")
            )


        if len(password) < 8:

            flash(
                "Password must contain at least 8 characters."
            )

            return redirect(
                url_for("auth.signup")
            )


        if password != confirm_password:

            flash(
                "Passwords do not match."
            )

            return redirect(
                url_for("auth.signup")
            )


        if not consent:

            flash(
                "Consent is required to create your account."
            )

            return redirect(
                url_for("auth.signup")
            )


        # -------------------------------------------------
        # CHECK DUPLICATE MOBILE
        # -------------------------------------------------

        if phone:

            existing_phone = User.query.filter_by(
                phone=phone
            ).first()

            if existing_phone:

                flash(
                    "This mobile number is already registered."
                )

                return redirect(
                    url_for("auth.signup")
                )


        # -------------------------------------------------
        # CHECK DUPLICATE EMAIL
        # -------------------------------------------------

        if email:

            existing_email = User.query.filter_by(
                email=email
            ).first()

            if existing_email:

                flash(
                    "This email address is already registered."
                )

                return redirect(
                    url_for("auth.signup")
                )


        # -------------------------------------------------
        # CREATE USER
        # -------------------------------------------------

        user = User(

            phone=phone if phone else None,

            email=email if email else None,

            role="trainee"

        )


        # Never store the actual password.
        # Store only a secure password hash.

        user.set_password(
            password
        )


        db.session.add(user)

        # Generate user ID before creating trainee profile.
        db.session.flush()


        # -------------------------------------------------
        # CREATE TRAINEE PROFILE
        # -------------------------------------------------

        trainee = Trainee(

            user_id=user.id,

            skilltrack_id=(
                Trainee.generate_skilltrack_id()
            ),

            full_name=full_name,

            consent_status=True

        )


        db.session.add(trainee)

        db.session.commit()


        # -------------------------------------------------
        # SUCCESS
        # -------------------------------------------------

        flash(
            "Account created successfully! "
            f"Your SkillTrack ID is "
            f"{trainee.skilltrack_id}."
        )


        return redirect(
            url_for("auth.login")
        )


    # -------------------------------------------------
    # GET REQUEST
    # -------------------------------------------------

    return render_template(
        "signup.html"
    )


# =========================================================
# LOGIN
# =========================================================

@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        identifier = request.form.get(
            "identifier",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )


        user = None


        # -------------------------------------------------
        # FIND USER BY EMAIL OR PHONE
        # -------------------------------------------------

        if "@" in identifier:

            user = User.query.filter_by(
                email=identifier.lower()
            ).first()

        else:

            user = User.query.filter_by(
                phone=identifier
            ).first()


        # -------------------------------------------------
        # VERIFY PASSWORD
        # -------------------------------------------------

        if user and user.check_password(password):

            # Create authenticated Flask-Login session.

            login_user(
                user,
                remember=True
            )


            # -------------------------------------------------
            # ROLE-BASED REDIRECT
            # -------------------------------------------------

            if user.role == "government":

                return redirect(
                    url_for(
                        "government.dashboard"
                    )
                )


            # All normal users go to trainee dashboard.

            return redirect(
                url_for(
                    "trainee.dashboard"
                )
            )


        # -------------------------------------------------
        # LOGIN FAILED
        # -------------------------------------------------

        flash(
            "Invalid mobile/email or password."
        )


    return render_template(
        "login.html"
    )


# =========================================================
# LOGOUT
# =========================================================

@auth_bp.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(
        url_for("auth.login")
    )