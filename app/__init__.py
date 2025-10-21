from flask import Flask
from app.config import Config
from app.database import mongo
from bson.objectid import ObjectId

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mongo.init_app(app)

    app.jinja_env.filters['str_id'] = lambda x: str(x) if isinstance(x, ObjectId) else x

    from . import routes
    app.register_blueprint(routes.bp)

    return app