from python.databaseKinds import Rating
from python.databaseKinds import Description
from python.databaseKinds import Comment
from python.databaseKinds import Band
from google.appengine.ext import ndb

def entities_to_dic_list(entities):
    dic_list = []
    print("in dic_list function")
    for entity in entities:
        dic_with_id = entity_to_dic(entity)
        dic_list.append(dic_with_id)
    return dic_list

def entity_to_dic(entity):
    dic = entity.to_dict()
    dic["id"] = entity.key.id()
    return dic
