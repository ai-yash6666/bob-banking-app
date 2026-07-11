import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = "dev-secret-key-change-in-production"
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "banking.db")
SQLALCHEMY_TRACK_MODIFICATIONS = False
DEBUG = True
