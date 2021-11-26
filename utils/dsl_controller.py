

class DslController(object):
    def __init__(self):
        self.body = {
            "query": {
                "bool":{
                    "must":[ ],
                    "must_not":[ ],
                    "should":[ ],
                    "filter":[ ]
                }
            },
            "aggs":{

            },
            "sort":{

            }
        }

    @property
    def query(self):
        return self.body

    def set_size_page(self,size:int,page:int):
        self.body["size"] = size
        self.body["from"] = size * (page-1)

    def _term_filter(self,f,v):
        return {
            "term":{ f:v }
        }

    def _terms_filter(self,f,v):
        if not isinstance(v,list):
            v = [v]
        return {
            "terms":{ f:v }
        }

    def add_must_term_filter(self,f,v):
        self.body["query"]["bool"]["must"].append(self._term_filter(f,v))
    
    def add_must_not_term_filter(self,f,v):
        self.body["query"]["bool"]["must_not"].append(self._term_filter(f,v))

    def add_must_terms_filter(self,f,v):
        self.body["query"]["bool"]["must"].append(self._terms_filter(f,v))
    
    def add_must_not_terms_filter(self,f,v):
        self.body["query"]["bool"]["must_not"].append(self._terms_filter(f,v))

    def set_field_order(self,field,order_tag):
        self.body["sort"][field] = {
            "order":order_tag
        }
    
    def agg_group_by_date(self,name,field):
        self.body["aggs"][name] = {
            "date_histogram": {
                "field": field,
                "interval": "month",
                "format": "yyyy年MM月"
            }
        }
    
    def agg_group_by_tag(self,name,field):
        self.body["aggs"][name] = {
            "terms": {
                "field": field
            }
        }

    def add_must_multi_match_filter(self,search_field_list,keyword):
        self.body["query"]["bool"]["must"].append({
            "multi_match" : {
                "query": keyword,
                "fields": search_field_list,
            }
        })
