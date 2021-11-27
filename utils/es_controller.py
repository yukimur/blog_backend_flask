
from elasticsearch import Elasticsearch
from blog.config import Config

class EsController(object):
    
    def __init__(self,index=Config.ELASTICSEARCH_INDEX):
        self.es = Elasticsearch()   # 直接查本地
        self._index = index

    def select(self,body):
        res = self.es.search(index=self._index, body=body)
        return res

    def get(self,id):
        res = self.es.get(index=self._index, id=id)
        return res

    def index(self,id,body):
        self.es.index(self._index, body, id=id)

    def update(self,id,body):
        body = {
            "doc":body
        }
        self.es.update(self._index, body=body, id=id)

if __name__ == "__main__":
    es_controller = EsController()
    es_controller.select()
