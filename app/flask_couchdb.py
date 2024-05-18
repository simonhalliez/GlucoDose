from flask import Flask
import couchdb


class CouchDB:
    def __init__(self):
        self.db = None

    def init_app(self, app: Flask):
        server_url = app.config['COUCHDB_SERVER']
        db_name = app.config['COUCHDB_DATABASE']
        server = couchdb.Server(server_url)
        if db_name in server:
            self.db = server[db_name]
        else:
            self.db = server.create(db_name)
