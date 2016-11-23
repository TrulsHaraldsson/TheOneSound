def entities_to_dic_list(entities):
    dic_list = []
    for entity in entites:
        dic_with_id =entity_to_dic(entity)
        dic_list.append(dic_with_id)
    return dic_list

def entity_to_dic(entity):
    dic = entity.to_dic()
    dic["id"] = entity.key.id()
    return dic
