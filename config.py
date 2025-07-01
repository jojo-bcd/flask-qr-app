import os

class Config:
    SECRET_KEY = 'dev'  # à remplacer par une vraie clé en prod
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/banque_app'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
