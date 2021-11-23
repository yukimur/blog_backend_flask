
from utils.dsl_controller import *
from utils.es_controller import *

class BlogEsManager(object):
    def __init__(self):
        self.es_controller = EsController()
        self.dsl_controller = DslController()
        self.select_type = "source" # source aggs 
        # 默认过滤删除
        self.dsl_controller.add_must_not_term_filter("delete",True)
    
    def set_select_type(self,select_type):
        self.select_type = select_type

    def filter(self,**kwargs):
        for k,v in kwargs.items():
            if isinstance(v,list):
                self.dsl_controller.add_must_terms_filter(k,v)
            else:
                self.dsl_controller.add_must_term_filter(k,v)

    def set_size_page(self,size:int,page:int):
        self.dsl_controller.set_size_page(size,page)

    def set_order(self,order_by):
        if not isinstance(order_by,list):
            order_by = [order_by]
        for item in order_by:
            if item.startswith("-"):
                order_tag = "desc"
                item = item[1:]
            else:
                order_tag = "asc"
            self.dsl_controller.set_field_order(item,order_tag)

    def select(self):
        query = self.dsl_controller.query
        res = self.es_controller.select(query)
        return res
    
    @property
    def result(self):
        data = self.select()
        return data.get("hits",[])
    
    def agg_group_by_date(self,field):
        self.dsl_controller.agg_group_by_date("group_by_%s"%field,field)
    
    def agg_group_by_tag(self,field):
        self.dsl_controller.agg_group_by_tag("group_by_%s"%field,field)

    @property
    def aggs(self):
        data = self.select()
        return data.get("aggregations",{})