import os

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    postgres_url = 'postgresql://masters_app_user:AyvTx0G6KY0worz83Uw1UQRYghUJaLBl@dpg-ch955iukobicv5rll8ag-a.frankfurt-postgres.render.com/masters_app'
    sqlite_url = "sqlite:///masters.db"
    # SQLALCHEMY_DATABASE_URI = postgres_url
    SQLALCHEMY_DATABASE_URI = sqlite_url
    SECRET_KEY = 'xyz'
    DEBUG = True
