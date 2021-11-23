
from flask import request, Blueprint,jsonify
from flask_restful import Api, Resource
from blog.models import User,Blog
from sqlalchemy.sql import func
from blog.es_manager import BlogEsManager

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
        # abort_if_todo_doesnt_exist(todo_id)
        return 1

    def post(self,id):
        pass

    def patch(self, id):
        args = parser.parse_args()
        return 1, 201

    def delete(self,id):
        pass

class BlogListViewSet(Resource):
    def get(self):
        size = int(request.args.get("size",10))
        page = int(request.args.get("page",0))
        my_type = request.args.get("type","博客")
        order_by = request.args.get("order_by",["-update_time"])

        blog_es_selector = BlogEsManager()
        blog_es_selector.filter(type_list=[my_type])
        blog_es_selector.set_size_page(size,page)
        blog_es_selector.set_order(order_by)
        result = blog_es_selector.result
        return result


api.add_resource(BlogListViewSet, '/blog_list/')
api.add_resource(BlogItemViewSet, '/blogitem/<id>')
