
from blog import db
from sqlalchemy import (
    Column, Integer, String,Boolean,
    Text, DateTime, Enum, ForeignKey
)
from blog.utils import *
from sqlalchemy import TypeDecorator
import json

class ModelMixin(object):
    def save(self):
        db.session.add(self)
        db.session.commit()

class JSONType(TypeDecorator):
    impl = Text

    def process_bind_param(self, value, dialect):
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        if not value:
            return value
        return json.loads(value)

class User(db.Model,ModelMixin):
    """用户表"""
    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False, unique=True)
    email = Column(String(255), nullable=True)
    password = Column(String(255), nullable=False)
    last_login = Column(DateTime,default=now)
    token = Column(String(255))

    def update_login_time(self,save_now=False):
        self.last_login = now()
        if save_now:
            self.save()

    def update_token(self,save_now=False):
        self.token = generate_token()
        if save_now:
            self.save()

class Image(db.Model,ModelMixin):
    """图片表"""
    id = Column(Integer, primary_key=True)
    create_time = Column(DateTime, default=now, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'),nullable=False)
    user = db.relationship('User',backref=db.backref('image_list', lazy=True))
    md5 = Column(String(255), nullable=False)
    url = Column(String(255), nullable=False)


class TimestampMixin(object):
    create_time = Column(DateTime, default=now, nullable=False)
    update_time = Column(DateTime, default=now, onupdate=now, nullable=False)

class Blog(db.Model,ModelMixin,TimestampMixin):
    """博客表"""
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'),nullable=False)
    user = db.relationship('User',backref=db.backref('blog_list', lazy=True))
    type_list = Column(JSONType, default=["博客"])
    tag_list = Column(JSONType, default=[])
    admire_count = Column(Integer, default=0)
    view_count = Column(Integer, default=0)
    delete = Column(Boolean,default=False)
    extra = Column(JSONType, default={})
    title_page_id = Column(Integer, ForeignKey('image.id'),nullable=True)
    title_page = db.relationship('Image',uselist=False)    # 封面外键

    def save(self):
        super().save()

    def delete(self):
        pass

class Comment(db.Model,ModelMixin,TimestampMixin):
    """评论表"""
    id = Column(Integer, primary_key=True)
    content = Column(Text,nullable=False)
    blog_id = Column(Integer, ForeignKey('blog.id'),nullable=False)
    blog = db.relationship('Blog',backref=db.backref('comment_list', lazy=True))
    # comment_id = db.Column(Integer, ForeignKey('blog.id'),nullable=False)
    # comment = db.relationship('Comment',backref=db.backref('comment_list', lazy=True))
    name = Column(String(255), nullable=False)
    email = Column(String(255))
    phone = Column(String(255))
