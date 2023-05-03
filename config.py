import os

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    if os.getenv('DATABASE_URL'):
        SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL').replace("postgres://", "postgresql://", 1)
    else:
        SQLALCHEMY_DATABASE_URI = "sqlite:///masters.db"
    SECRET_KEY = 'xyz'
    DEBUG = True
