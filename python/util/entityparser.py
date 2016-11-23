
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
######General getters from database######
def get_entities_by_name(cls, entity_name, limit_=10, offset_=0):
    query = cls.query(cls.name==entity_name)
    entities = query.fetch(limit=int(limit_), offset=int(offset_))
    if entities != None:
        return entities
    else:
        raise ValueError("No such band exists!")

def get_multiple_entities(cls, limit):
    #TODO: filters should be made, also different sortings
    query = cls.query().order(cls.name)
    if limit != "":
        entities = query.fetch(limit)
    else:
        amount = 10
        entities = query.fetch(amount)
    return entities

def get_entity_by_id(cls, id):
    entity = cls.get_by_id(id)
    if entity:
        return entity
    else:
        raise ValueError("Entity does not exist!")
