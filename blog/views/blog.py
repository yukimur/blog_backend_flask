
from flask import request, Blueprint,jsonify
from flask_restful import Api, Resource
from blog.models import User,Blog
from sqlalchemy.sql import func
from blog.es_manager import BlogEsManager
from utils.es_controller import EsController

blog_api = Blueprint('blog', __name__,url_prefix="/blog")
api = Api(blog_api)

@blog_api.route('/get_web_statis/', methods=['GET'])
def get_web_statis():
    blog_filter = Blog.query.filter()   # 后面加博客过滤
    blog_count = blog_filter.count() # 博文数量
    view_sum = blog_filter.with_entities(func.sum(Blog.view_count)).scalar() # 博文总浏览量
    admire_sum = blog_filter.with_entities(func.sum(Blog.admire_count)).scalar() # 博文总点赞量
    result = {
        "博文数量":blog_count,
        "博文总浏览量":view_sum,
        "博文总点赞量":admire_sum,
    }
    return jsonify(result)

@blog_api.route('/get_group_by_date/', methods=['GET'])
def get_group_by_date():
    blog_es_selector = BlogEsManager()
    blog_es_selector.filter(type_list=["博客"])
    blog_es_selector.set_size_page(0,0) # 只聚合

    blog_es_selector.agg_group_by_date("create_time")

    aggs = blog_es_selector.aggs
    buckets = aggs.get("group_by_%s"%"create_time",{}).get("buckets",[])
    return jsonify(buckets)

@blog_api.route('/get_tag_list/', methods=['GET'])
def get_tag_list():
    blog_es_selector = BlogEsManager()
    blog_es_selector.filter(type_list=["博客"])
    blog_es_selector.set_size_page(0,0) # 只聚合
    
    blog_es_selector.agg_group_by_tag("tag_list")

    aggs = blog_es_selector.aggs
    buckets = aggs.get("group_by_%s"%"tag_list",{}).get("buckets",[])
    return jsonify(buckets)

@blog_api.route('/get_type_list/', methods=['GET'])
def get_type_list():
    blog_es_selector = BlogEsManager()
    blog_es_selector.filter(type_list=["博客"])
    blog_es_selector.set_size_page(0,0) # 只聚合
    
    blog_es_selector.agg_group_by_tag("type_list")

    aggs = blog_es_selector.aggs
    buckets = aggs.get("group_by_%s"%"type_list",{}).get("buckets",[])
    return jsonify(buckets)

@blog_api.route('/get_group_by_tag/', methods=['GET'])
def get_group_by_tag():
    blog_es_selector = BlogEsManager()
    blog_es_selector.filter(type_list=["博客"])
    blog_es_selector.set_size_page(0,0) # 只聚合
    
    blog_es_selector.agg_group_by_tag("tag_list")

    aggs = blog_es_selector.aggs
    buckets = aggs.get("group_by_%s"%"tag_list",{}).get("buckets",[])
    return jsonify(buckets)

class BlogItemViewSet(Resource):
    def get(self, id):
        ec = EsController()
        res = ec.get(id)
        res = res.get("_source",{})
        blog = Blog.query.filter_by(id=id).first()
        res["user"] = blog.user.username
        return res

    def patch(self, id):
        data = request.json
        blog = Blog.query.filter_by(id=id).first()
        for k,v in data.items():
            if k not in ["id","content"]:
                setattr(blog,k,v)
        blog.save()
        
        # 更新es
        blog_es_selector = BlogEsManager()
        blog_es_selector.update(id,data)
        return data

    def delete(self,id):
        pass

class BlogListViewSet(Resource):
    def get(self):
        size = int(request.args.get("size",10))
        page = int(request.args.get("page",1))
        my_type = request.args.get("type","博客")
        tag_list = request.args.get("tag_list")
        if tag_list and not isinstance(tag_list,str):
            tag_list = tag_list.split(",")
        keyword = request.args.get("keyword")
        order_by = request.args.get("order_by",["-update_time"])

        blog_es_selector = BlogEsManager()
        blog_es_selector.filter(type_list=[my_type],tag_list=tag_list,keyword=keyword)
        blog_es_selector.set_size_page(size,page)
        blog_es_selector.set_order(order_by)
        result = blog_es_selector.result
        return result

class ImageViewSet(Resource):
    def post(self):
        pass

api.add_resource(BlogListViewSet, "/blog_list/")
api.add_resource(BlogItemViewSet, "/blogitem/<int:id>/")
api.add_resource(ImageViewSet, "/image/")
