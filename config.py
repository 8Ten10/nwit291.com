import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'Admin'
    MYSQL_PASSWORD = 'password1234'
    MYSQL_DB = 'nwit_db'
