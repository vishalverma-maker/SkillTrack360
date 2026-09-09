from datetime import datetime

from models import db


class Outcome(db.Model):

    __tablename__ = "outcomes"

    # =========================================
    # PRIMARY KEY
    # =========================================

    id = db.Column(
        db.Integer,
        primary_key=True
    )


    # =========================================
    # TRAINEE CONNECTION
    # =========================================

    trainee_id = db.Column(
        db.Integer,
        db.ForeignKey("trainees.id"),
        nullable=False
    )


    # =========================================
    # FOLLOW-UP PERIOD
    # =========================================

    followup_period = db.Column(
        db.String(20),
        nullable=False
    )


    # =========================================
    # EMPLOYMENT STATUS
    # =========================================

    employment_status = db.Column(
        db.String(50),
        nullable=False
    )


    # =========================================
    # EMPLOYMENT DETAILS
    # =========================================

    company_name = db.Column(
        db.String(150),
        nullable=True
    )

    job_role = db.Column(
        db.String(150),
        nullable=True
    )

    monthly_salary = db.Column(
        db.Float,
        nullable=True
    )

    joining_date = db.Column(
        db.Date,
        nullable=True
    )


    # =========================================
    # JOB RELEVANCE
    # =========================================

    job_relevance = db.Column(
        db.String(30),
        nullable=True
    )


    # =========================================
    # TIMESTAMP
    # =========================================

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


    # =========================================
    # REPRESENTATION
    # =========================================

    def __repr__(self):

        return (
            f"<Outcome "
            f"{self.trainee_id} "
            f"{self.followup_period}>"
        )