from flask_smorest import Blueprint, abort
from flask.views import MethodView
from db import db
from Models import UserModel
from schema import UserSchema
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    jwt_required,
    get_jti,
    create_refresh_token,
    get_jwt_identity,
)
from blocklist import BLOCKLIST

blp = Blueprint("user", __name__)
"""
一個jwt 裡面包含了jwt header,jwt payload,signature
header:包含token的類型，以及簽名算法
payload:裡面包含了聲明、相關的資料等，其中jti(jwt id)也是儲存於此
signature:由header、payload、secret key所組成的雜湊亂碼，用於檢查jwt是否經過篡改
"""


@blp.route("/register")
class Register(MethodView):

    @blp.arguments(schema=UserSchema)  # 註冊USER
    def post(self, data):
        if UserModel.query.filter(UserModel.username == data["username"]).first():
            abort(409, message="This account is exist")

        # 不能直接將資料傳入，需先將資料進行加密
        new_account = UserModel(
            username=data["username"], password=pbkdf2_sha256.hash(data["password"])
        )
        db.session.add(new_account)
        db.session.commit()
        return {"message": "Create user successfully"}, 201


@blp.route("/user/<int:user_id>")  # 方便測試用
class User(MethodView):
    """
    This resource can be useful when testing our Flask app.
    We may not want to expose it to public users, but for the
    sake of demonstration in this course, it can be useful
    when we are manipulating data regarding the users.
    """

    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted."}, 200


@blp.route("/login")
class Login(MethodView):

    @blp.arguments(schema=UserSchema)  # 使用者確認後給予access_token
    def post(self, data):
        user = UserModel.query.filter(UserModel.username == data["username"]).first()
        if user and pbkdf2_sha256.verify(data["password"], user.password):
            access_token = create_access_token(
                identity=user.id, fresh=True
            )  # fresh的token可以做更進一步的動作，可由required(fresh=True)來決定
            refresh_token = create_refresh_token(user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200
        abort(401, message="not a valid account")


@blp.route("/logout")  # 使用者登出時將jti of user jwt加入到BLOCKLIST中
class Logout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "successfully logged out"}, 200


@blp.route("/refresh")  # 當token過期時可以refresh token而不用進行重新登入獲取新的token
class Refresh(MethodView):

    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        origin_jti = get_jti()
        BLOCKLIST.add(origin_jti)
        return {"access_token": new_token}, 200
