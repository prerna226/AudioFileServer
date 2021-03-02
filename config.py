import os

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_ECHO = False
DEBUG = True
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:********@localhost/audiofileserverdb"
SQLALCHEMY_TRACK_MODIFICATIONS = False