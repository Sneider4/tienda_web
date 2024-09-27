import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123@localhost:3306/Malcon'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'programanike@gmail.com'
    MAIL_PASSWORD = 'ghgu sumn kckx dfbk'