
from elasticsearch import Elasticsearch
from blog.config import Config

class EsController(object):
    
    def __init__(self,index=Config.ELASTICSEARCH_INDEX):
        self.es = Elasticsearch()   # 直接查本地
        self.index = index

    def select(self,body):
        res = self.es.search(index=self.index, body=body)
        return res

if __name__ == "__main__":
    es_controller = EsController()
    es_controller.select()