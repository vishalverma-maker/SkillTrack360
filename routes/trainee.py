from datetime import datetime

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_required,
    current_user
)

from models import db
from models.trainee import Trainee
from models.outcome import Outcome


trainee_bp = Blueprint(
    "trainee",
    __name__,
    url_prefix="/trainee"
)


# =========================================================
# TRAINEE DASHBOARD
# =========================================================

@trainee_bp.route("/dashboard")
@login_required
def dashboard():

    trainee = current_user.trainee_profile

    # Get all saved outcomes for this trainee
    outcomes = (
        Outcome.query
        .filter_by(trainee_id=trainee.id)
        .order_by(Outcome.id.asc())
        .all()
    )

    # Find specific follow-up outcomes
    outcome_3 = next(
        (
            outcome
            for outcome in outcomes
            if outcome.followup_period == "3-Month"
        ),
        None
    )

    outcome_6 = next(
        (
            outcome
            for outcome in outcomes
            if outcome.followup_period == "6-Month"
        ),
        None
    )

    outcome_12 = next(
        (
            outcome
            for outcome in outcomes
            if outcome.followup_period == "12-Month"
        ),
        None
    )

    return render_template(
        "trainee/dashboard.html",
        user=current_user,
        trainee=trainee,
        outcomes=outcomes,
        outcome_3=outcome_3,
        outcome_6=outcome_6,
        outcome_12=outcome_12
    )

# =========================================================
# FOLLOW-UPS
# =========================================================

@trainee_bp.route("/followups")
@login_required
def followups():

    trainee = current_user.trainee_profile

    # Get all outcomes saved for this trainee
    outcomes = (
        Outcome.query
        .filter_by(trainee_id=trainee.id)
        .order_by(Outcome.id.asc())
        .all()
    )

    # Find individual follow-up records
    outcome_3 = next(
        (
            outcome
            for outcome in outcomes
            if outcome.followup_period == "3-Month"
        ),
        None
    )

    outcome_6 = next(
        (
            outcome
            for outcome in outcomes
            if outcome.followup_period == "6-Month"
        ),
        None
    )

    outcome_12 = next(
        (
            outcome
            for outcome in outcomes
            if outcome.followup_period == "12-Month"
        ),
        None
    )

    return render_template(
        "trainee/followups.html",
        user=current_user,
        trainee=trainee,
        outcome_3=outcome_3,
        outcome_6=outcome_6,
        outcome_12=outcome_12
    )
# =========================================================
# COMPLETE PROFILE
# =========================================================

@trainee_bp.route(
    "/profile",
    methods=["GET", "POST"]
)
@login_required
def profile():

    trainee = current_user.trainee_profile


    # -----------------------------------------------------
    # FORM SUBMITTED
    # -----------------------------------------------------

    if request.method == "POST":

        # Personal information
        full_name = request.form.get(
            "full_name",
            ""
        ).strip()

        age = request.form.get(
            "age",
            ""
        ).strip()

        gender = request.form.get(
            "gender",
            ""
        ).strip()

        district = request.form.get(
            "district",
            ""
        ).strip()

        education = request.form.get(
            "education",
            ""
        ).strip()


        # Training information
        training_program = request.form.get(
            "training_program",
            ""
        ).strip()

        training_provider = request.form.get(
            "training_provider",
            ""
        ).strip()

        start_date = request.form.get(
            "training_start_date",
            ""
        ).strip()

        completion_date = request.form.get(
            "training_completion_date",
            ""
        ).strip()

        certificate_status = request.form.get(
            "certificate_status",
            "Pending"
        ).strip()


        # -------------------------------------------------
        # VALIDATION
        # -------------------------------------------------

        if not full_name:

            flash("Full name is required.")

            return redirect(
                url_for("trainee.profile")
            )


        # -------------------------------------------------
        # PERSONAL INFORMATION
        # -------------------------------------------------

        trainee.full_name = full_name


        if age:

            try:

                trainee.age = int(age)

            except ValueError:

                flash("Age must be a valid number.")

                return redirect(
                    url_for("trainee.profile")
                )

        else:

            trainee.age = None


        trainee.gender = gender or None

        trainee.district = district or None

        trainee.education = education or None


        # -------------------------------------------------
        # TRAINING INFORMATION
        # -------------------------------------------------

        trainee.training_program = (
            training_program or None
        )

        trainee.training_provider = (
            training_provider or None
        )


        # Training start date

        if start_date:

            try:

                trainee.training_start_date = (
                    datetime.strptime(
                        start_date,
                        "%Y-%m-%d"
                    ).date()
                )

            except ValueError:

                flash(
                    "Invalid training start date."
                )

                return redirect(
                    url_for("trainee.profile")
                )

        else:

            trainee.training_start_date = None


        # Training completion date

        if completion_date:

            try:

                trainee.training_completion_date = (
                    datetime.strptime(
                        completion_date,
                        "%Y-%m-%d"
                    ).date()
                )

            except ValueError:

                flash(
                    "Invalid training completion date."
                )

                return redirect(
                    url_for("trainee.profile")
                )

        else:

            trainee.training_completion_date = None


        trainee.certificate_status = (
            certificate_status or "Pending"
        )


        # -------------------------------------------------
        # SAVE
        # -------------------------------------------------

        db.session.commit()


        flash(
            "Your profile has been updated successfully!"
        )


        return redirect(
            url_for("trainee.dashboard")
        )


    return render_template(
        "trainee/profile.html",
        user=current_user,
        trainee=trainee
    )
# =========================================================
# MY TRAINING
# =========================================================

@trainee_bp.route("/training")
@login_required
def training():

    trainee = current_user.trainee_profile

    return render_template(
        "trainee/training.html",
        user=current_user,
        trainee=trainee
    )

# =========================================================
# CAREER OUTCOMES
# =========================================================

@trainee_bp.route(
    "/outcomes",
    methods=["GET", "POST"]
)
@login_required
def outcomes():

    trainee = current_user.trainee_profile


    # -----------------------------------------------------
    # FORM SUBMITTED
    # -----------------------------------------------------

    if request.method == "POST":

        followup_period = request.form.get(
            "followup_period",
            "3-Month"
        ).strip()


        employment_status = request.form.get(
            "employment_status",
            ""
        ).strip()


        company_name = request.form.get(
            "company_name",
            ""
        ).strip()


        job_role = request.form.get(
            "job_role",
            ""
        ).strip()


        salary = request.form.get(
            "monthly_salary",
            ""
        ).strip()


        joining_date = request.form.get(
            "joining_date",
            ""
        ).strip()


        job_relevance = request.form.get(
            "job_relevance",
            ""
        ).strip()


        # -------------------------------------------------
        # VALIDATION
        # -------------------------------------------------

        if not employment_status:

            flash(
                "Please select your employment status."
            )

            return redirect(
                url_for("trainee.outcomes")
            )


        # -------------------------------------------------
        # FIND EXISTING FOLLOW-UP
        # -------------------------------------------------

        outcome = Outcome.query.filter_by(
            trainee_id=trainee.id,
            followup_period=followup_period
        ).first()


        # If this follow-up doesn't exist,
        # create it.

        if outcome is None:

            outcome = Outcome(
                trainee_id=trainee.id,
                followup_period=followup_period
            )

            db.session.add(outcome)


        # -------------------------------------------------
        # SAVE EMPLOYMENT STATUS
        # -------------------------------------------------

        outcome.employment_status = (
            employment_status
        )


        # -------------------------------------------------
        # SAVE EMPLOYMENT DETAILS
        # -------------------------------------------------

        outcome.company_name = (
            company_name or None
        )

        outcome.job_role = (
            job_role or None
        )


        # -------------------------------------------------
        # SALARY
        # -------------------------------------------------

        if salary:

            try:

                outcome.monthly_salary = float(
                    salary
                )

            except ValueError:

                flash(
                    "Monthly salary must be a valid number."
                )

                return redirect(
                    url_for("trainee.outcomes")
                )

        else:

            outcome.monthly_salary = None


        # -------------------------------------------------
        # JOINING DATE
        # -------------------------------------------------

        if joining_date:

            try:

                outcome.joining_date = (
                    datetime.strptime(
                        joining_date,
                        "%Y-%m-%d"
                    ).date()
                )

            except ValueError:

                flash(
                    "Invalid joining date."
                )

                return redirect(
                    url_for("trainee.outcomes")
                )

        else:

            outcome.joining_date = None


        # -------------------------------------------------
        # JOB RELEVANCE
        # -------------------------------------------------

        outcome.job_relevance = (
            job_relevance or None
        )


        # -------------------------------------------------
        # SAVE DATABASE
        # -------------------------------------------------

        db.session.commit()


        flash(
            f"{followup_period} outcome saved successfully!"
        )


        return redirect(
            url_for("trainee.outcomes")
        )


    # -----------------------------------------------------
    # GET EXISTING OUTCOMES
    # -----------------------------------------------------

    outcomes = (
        Outcome.query
        .filter_by(trainee_id=trainee.id)
        .order_by(Outcome.id.desc())
        .all()
    )


    return render_template(
        "trainee/outcomes.html",
        user=current_user,
        trainee=trainee,
        outcomes=outcomes
    )