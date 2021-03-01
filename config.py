import os

# You need to replace the next values with the appropriate values for your configuration

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_ECHO = False
DEBUG = True
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:tech@123@localhost/audiofileserverdb"
SQLALCHEMY_TRACK_MODIFICATIONS = False