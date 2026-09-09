from datetime import datetime
import uuid

from models import db


class Trainee(db.Model):

    __tablename__ = "trainees"

    # =========================================
    # PRIMARY KEY
    # =========================================

    id = db.Column(
        db.Integer,
        primary_key=True
    )


    # =========================================
    # USER CONNECTION
    # =========================================

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        unique=True,
        nullable=False
    )


    # =========================================
    # SKILLTRACK ID
    # =========================================

    skilltrack_id = db.Column(
        db.String(30),
        unique=True,
        nullable=False
    )


    # =========================================
    # BASIC INFORMATION
    # =========================================

    full_name = db.Column(
        db.String(120),
        nullable=False
    )

    age = db.Column(
        db.Integer,
        nullable=True
    )

    gender = db.Column(
        db.String(30),
        nullable=True
    )

    district = db.Column(
        db.String(100),
        nullable=True
    )

    education = db.Column(
        db.String(150),
        nullable=True
    )


    # =========================================
    # TRAINING INFORMATION
    # =========================================

    training_program = db.Column(
        db.String(150),
        nullable=True
    )

    training_provider = db.Column(
        db.String(150),
        nullable=True
    )

    training_start_date = db.Column(
        db.Date,
        nullable=True
    )

    training_completion_date = db.Column(
        db.Date,
        nullable=True
    )

    certificate_status = db.Column(
        db.String(50),
        default="Pending",
        nullable=True
    )


    # =========================================
    # CONSENT
    # =========================================

    consent_status = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )


    # =========================================
    # CREATED DATE
    # =========================================

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


    # =========================================
    # RELATIONSHIP WITH USER
    # =========================================

    user = db.relationship(
        "User",
        backref=db.backref(
            "trainee_profile",
            uselist=False
        )
    )


    # =========================================
    # SKILLTRACK ID GENERATOR
    # =========================================

    @staticmethod
    def generate_skilltrack_id():

        return (
            "ST-MH-"
            + uuid.uuid4().hex[:8].upper()
        )


    # =========================================
    # REPRESENTATION
    # =========================================

    def __repr__(self):

        return (
            f"<Trainee {self.skilltrack_id}>"
        )