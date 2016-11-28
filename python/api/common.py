# ---------- General getters from database ----------
def get_entities_by_name(cls, entity_name, limit_=10, offset_=0):
    query = cls.query(cls.name == entity_name)
    entities = query.fetch(limit=int(limit_), offset=int(offset_))
    if not entities:
        return entities
    else:
        raise ValueError("No such band exists!")


def get_multiple_entities(cls, limit):
    # TODO: filters should be made, also different sortings
    query = cls.query().order(cls.name)
    if limit != "":
        entities = query.fetch(limit)
    else:
        amount = 10
        entities = query.fetch(amount)
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
