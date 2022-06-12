import os

DEBUG = False
SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///data.sqlite")
SECRET_KEY = os.environ["APP_SECRET_KEY"]