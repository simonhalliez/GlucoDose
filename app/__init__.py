from flask import Flask
import couchdb


def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_pyfile('../.env')

    # Connexion à CouchDB
    couch = couchdb.Server(app.config['COUCHDB_SERVER'])
    db = couch[app.config['COUCHDB_DATABASE']]
    app.config['COUCHDB_DB'] = db

    with app.app_context():
        from .routes.insulin import insulin_blueprint
        from .routes.meals import meals_blueprint
        from .routes.index import home_blueprint

        app.register_blueprint(insulin_blueprint, url_prefix='/api/v1/insulin')
        app.register_blueprint(meals_blueprint, url_prefix='/api/v1/meals')
        app.register_blueprint(home_blueprint)

    return app
