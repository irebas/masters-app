class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///masters.db"
    SECRET_KEY = 'xyz'
    DEBUG = True
