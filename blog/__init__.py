
from flask import Flask
from blog.config import Config
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate(compare_type=True)

def init_app(app):
    db.init_app(app)
    migrate.init_app(app=app, db=db)

    from blog.views import blog,user
    app.register_blueprint(blog.blog_api)
    app.register_blueprint(user.user_api)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())
    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    init_app(app)
    # from blog import models
    # init_app_extensions(app)
    # configure_log(app)
    # init_app_handlers(app)

    return app
