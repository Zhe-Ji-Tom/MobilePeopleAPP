import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:admin@localhost/people_counter'
    SQLALCHEMY_TRACK_MODIFICATIONS = False