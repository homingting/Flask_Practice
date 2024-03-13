from flask import Flask, jsonify
from db import db
from resource.StoreResource import blp as StoreBLP
from resource.ItemResource import blp as ItemBLP
from resource.TagResourece import blp as TagBLP
from resource.UserResource import blp as UserBLP
import Models
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from blocklist import BLOCKLIST
from flask_migrate import Migrate


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
    app.config["OPENAPI_SQAGGER_UI_URL"] = (
        "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    )

    app.config["JWT_SECRET_KEY"] = "hello"
    jwt = JWTManager(app)

    @jwt.additional_claims_loader  # 反傳一個dictionary至每一個創建的access_token中
    def add_claim_to_jwt(identity):
        if identity == 1:
            return {"is_admin": True}
        return {"is_admin": False}

    @jwt.expired_token_loader  # access_token已經過期了
    def expire_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired.", "error": "token_expired"}),
            401,
        )

    @jwt.invalid_token_loader  # 有提供但是無效
    def invalid_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader  # 未提供access_token 時
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )

    @jwt.token_in_blocklist_loader  # jti全名為jwt ID ，用於檢查token是否有在blocklist裡面
    def check_if_token_in_blocklist(jet_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.revoked_token_loader  # 檢查token是否已經被註銷了
    def revoke_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "the token has been revoke.", "error": "token _revoked"}
            ),
            401,
        )

    @jwt.needs_fresh_token_loader   # 若需要fresh_toekn時所發出的回應
    def need_fresh_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description": "the token is not fresh.",
                    "error": "fresh_token required.",
                }
            ),
            401,
        )

    api = Api(app)
    db.init_app(app)
    migrate = Migrate(app,db)

    api.register_blueprint(StoreBLP)
    api.register_blueprint(ItemBLP)
    api.register_blueprint(TagBLP)
    api.register_blueprint(UserBLP)

    return app
