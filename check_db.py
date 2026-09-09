from app import app
from models import db
from models.user import User
from models.trainee import Trainee


with app.app_context():

    print("\n========== SKILLTRACK DATABASE ==========\n")

    print("Users:", User.query.count())
    print("Trainees:", Trainee.query.count())

    print("\n========== USERS ==========\n")

    users = User.query.all()

    for user in users:
        print(
            f"ID: {user.id} | "
            f"Email: {user.email} | "
            f"Phone: {user.phone} | "
            f"Role: {user.role}"
        )

    print("\n========== TRAINEES ==========\n")

    trainees = Trainee.query.all()

    for trainee in trainees:
        print(
            f"ID: {trainee.id} | "
            f"SkillTrack ID: {trainee.skilltrack_id} | "
            f"Name: {trainee.full_name} | "
            f"Consent: {trainee.consent_status}"
        )

    print("\n=========================================\n")