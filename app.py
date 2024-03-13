from flask import Flask
from db import db
from resource.StoreResource import blp as StoreBLP
from resource.ItemResource import blp as ItemBLP
from resource.TagResourece import blp as TagBLP
import Models
from flask_smorest import Api



def create_app():
    app = Flask(__name__)
    app.config["API_TITLE"] = "REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.1.0"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SQAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    api = Api(app)
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        
    api.register_blueprint(StoreBLP)
    api.register_blueprint(ItemBLP)
    api.register_blueprint(TagBLP)
    return app