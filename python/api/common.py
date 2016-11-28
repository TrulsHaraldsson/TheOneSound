# ---------- General getters from database ----------
def get_entities_by_name(cls, entity_name, limit_=10, offset_=0):
    query = cls.query(cls.name == entity_name)
    entities = query.fetch(limit=int(limit_), offset=int(offset_))
    if not entities:
        return entities
    else:
        raise ValueError("No such band exists!")


def get_entities(cls, limit=10, order_=None):
    """
    Search among all entities of a given Kind and order them by the given
    ordering parameter
    :param cls: The Kind in the Database
    :param limit: Upper bound of entities that will be returned. Default it 10.
    :param order_: An ordering based on the properties of the given Kind. If no order is
    given, the entities are sorted by ascending key-value
    :return: A list with the query result
    """
    #TODO: Add filter
    if not order_:
        order_ = cls.key

    query = cls.query().order(order_)
    entities = query.fetch(limit)
    return entities


def get_entity_by_id(cls, entity_id):
    """
    Search for an entity of a given Kind using the given ID.
    :param cls: The Kind in the Database
    :param entity_id: The ID of the entity
    :return: An Entity of the given Kind with the given ID. If no entity is found with the given ID
    a ValueError will be raised.
    """
    entity = cls.get_by_id(entity_id)
    if entity:
        return entity
    else:
        raise ValueError("Entity does not exist!")
