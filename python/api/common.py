def get_entities_by_name(cls, entity_name, limit=10, offset_=0, order_=None):
    """
    Returns the entities with the given name and Kind. By default the maximum number of
    entities returned is 10 with an offset of 0. E.g. if limit_ = 5 and offset_ = 4 the
    query will return at maximum one entity. That is, there are more than 4 albums with that name.

    :param cls: The Kind in the Database
    :param entity_name: Name of entities which are queried
    :param limit: Upper bound of entities that will be returned. Default it 10.
    :param offset_: The number of entities in the query that are initially skipped. Default is 0
    :param order_: An ordering based on the properties of the given Kind. If no order is
    given, the entities are sorted by ascending key-value.
    :return:
    """
    if not order_:
        order_ = cls.key

    query = cls.query(cls.name == entity_name).order(order_)
    entities = query.fetch(limit, offset=offset_)

    if not entities:
        return entities
    else:
        raise ValueError("No entity with name " + entity_name + " exists")


def get_entities(cls, limit=10, offset_=0, order_=None):
    """
    Search among all entities of a given Kind and order them by the given
    ordering parameter.

    :param cls: The Kind in the Database
    :param limit: Upper bound of entities that will be returned. Default it 10.
    :param offset_: The number of entities in the query that are initially skipped. Default is 0
    :param order_: An ordering based on the properties of the given Kind. If no order is
    given, the entities are sorted by ascending key-value.
    :return: A list with the query result
    """
    #TODO: Add filter
    if not order_:
        order_ = cls.key

    query = cls.query().order(order_)
    entities = query.fetch(limit, offset=offset_)
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
