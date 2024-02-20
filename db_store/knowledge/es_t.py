
from elasticsearch import Elasticsearch
from elasticsearch import helpers

es = Elasticsearch(hosts=["http://elastic:123456@0.0.0.0:19200/"])


print(es.search(index='es_subdocument_store'))