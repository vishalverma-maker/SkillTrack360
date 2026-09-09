import os


class Config:
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "skilltrack-dev-secret-key"
    )

    SQLALCHEMY_DATABASE_URI = "sqlite:///skilltrack.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False