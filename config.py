import os

POSTGRES_URL = 'postgresql://masters_app_user:AyvTx0G6KY0worz83Uw1UQRYghUJaLBl@dpg-ch955iukobicv5rll8ag-a.frankfurt-postgres.render.com/masters_app'
SQLITE_URL = "sqlite:///masters.db"

# host = dpg-ch955iukobicv5rll8ag-a.frankfurt-postgres.render.com
# username = masters_app_user
# pass = AyvTx0G6KY0worz83Uw1UQRYghUJaLBl
# port = 5432


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    if str(os.getenv('HOME')).lower().find('users'):
        # SQLALCHEMY_DATABASE_URI = POSTGRES_URL
        SQLALCHEMY_DATABASE_URI = SQLITE_URL
    else:
        SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SECRET_KEY = 'xyz'
    DEBUG = True
