
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

# class Image(db.Model):
#     """图片表"""
#     id = Column(Integer, primary_key=True)
#     image = models.ImageField(upload_to="images")
#     create_time = models.DateTimeField(auto_now_add=True)   # 创建时间
#     is_public = models.BooleanField(default=False)  # 是否公有
#     md5 = models.CharField(max_length=64,blank=True,null=True)  # md5

class TimestampMixin(object):
    create_time = Column(DateTime, default=now, nullable=False)
    update_time = Column(DateTime, default=now, onupdate=now, nullable=False)

class Blog(db.Model,TimestampMixin):
    """博客表"""
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    user_id = db.Column(Integer, ForeignKey('user.id'),nullable=False)
    user = db.relationship('User',backref=db.backref('blog_list', lazy=True))
    type_list = Column(JSONType, default=["博客"])
    tag_list = Column(JSONType, default=[])
    admire_count = Column(Integer, default=0)
    view_count = Column(Integer, default=0)
    delete = Column(Boolean,default=False)
    extra = Column(JSONType, default={})
    # title_page = models.ForeignKey(Image,on_delete=models.SET_NULL,blank=True,null=True) # 封面外键

    def delete(self):
        pass

class Comment(db.Model,TimestampMixin):
    """评论表"""
    id = Column(Integer, primary_key=True)
    content = Column(Text,nullable=False)
    blog_id = db.Column(Integer, ForeignKey('blog.id'),nullable=False)
    blog = db.relationship('Blog',backref=db.backref('comment_list', lazy=True))
    # comment = Column(Text, nullable=False)
    # comment = models.ForeignKey(to='self',on_delete=models.CASCADE,blank=True,null=True,related_name="comment_set")
    name = Column(String(255), nullable=False)
    email = Column(String(255)) 
    phone = Column(String(255)) 
