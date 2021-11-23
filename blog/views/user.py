
from flask import request, Blueprint,abort,jsonify
from flask_restful import Api, Resource
from blog.models import User
from blog.utils import *
import functools
from werkzeug.local import LocalProxy
from flask import g, current_app, abort
from blog.config import Config

user_api = Blueprint('user', __name__,url_prefix="/user")
api = Api(user_api)

def find_current_user():
    authorization = request.headers.get("Authorization")
    if authorization:
        token = authorization.split()[-1]
        user = User.query.filter_by(token=token).first()
        if user:
            if user.last_login >= get_time_relative_now(-Config.TOKEN_EXPIRED):
                return user
            else:
                abort(401,"token 已过期.")
    abort(401)

# 当前用户
current_user = LocalProxy(find_current_user)

def login_required(view_func):
    @functools.wraps(view_func)
    def wrapper(*args, **kwargs):
        if not current_user:
            abort(401)
        return view_func(*args, **kwargs)

    return wrapper

class UserInfoViewSet(Resource):
    @login_required
    def get(self):
        return jsonify({
            "username": current_user.username,
            "email": current_user.email,
            "last_login": current_user.last_login
        })

class LoginViewSet(Resource):
    """登陆用户"""

    def post(self):
        data = request.json
        username = data.get("username")
        password = data.get("password")
        print(data)
        if username and password:
            password_md5 = md5(password)
            user = User.query.filter_by(username=username,password=password_md5).first()
            if user:
                user.update_login_time()    # 更新登陆时间
                user.update_token()
                user.save()
                return jsonify({
                    "token":user.token,
                    "last_login":user.last_login
                })
            abort(401,"username or password error.")
        abort(401,"username or password must required.")

api.add_resource(UserInfoViewSet, '/userinfo/')
api.add_resource(LoginViewSet, '/login/')
