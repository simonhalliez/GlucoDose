import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    COUCHDB_SERVER = os.getenv('COUCHDB_SERVER', 'http://localhost:5984/')
    COUCHDB_DATABASE = os.getenv('COUCHDB_DATABASE', 'insulin-database')
