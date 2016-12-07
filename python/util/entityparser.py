import json


def entities_to_dic_list(entities):
    dic_list = []
    for entity in entities:
        dic_with_id = entity_to_dic(entity)
        dic_list.append(dic_with_id)
    return dic_list


def entity_to_dic(entity):
    dic = entity.to_dict()
    dic["id"] = entity.key.id()
    return dic


def entity_id_to_json(entity_id):
    id_dict = {'id': entity_id}
    return json.dumps(id_dict)
