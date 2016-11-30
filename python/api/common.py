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

    if entities:
        return entities
    else:
        raise ValueError("No entity with name " + entity_name + " exists")


def get_entities(cls, limit=10, offset_=0, order_=None, filters=None):
    """
    Search among all entities of a given Kind and order them by the given
    ordering parameter.

    :param cls: The Kind in the Database
    :param limit: Upper bound of entities that will be returned. Default it 10.
    :param offset_: The number of entities in the query that are initially skipped. Default is 0
    :param order_: An ordering based on the properties of the given Kind. If no order is
    given, the entities are sorted by ascending key-value.
    :param filters: A list of filters that the will be applied on the query
    :return: A list with the query result
    """
    print("limit: ", limit)
    if not order_:
        order_ = cls.key

    query = cls.query().order(order_)
    if filters:
        for filter_ in filters:
            query = query.filter(filter_)

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


def parse_url_query_parameters(query_parameters):
    """
    Parses all the query parameters and but them in a dictionary that is returned.
    The following parameter-keys can be detected: type, limit, offset, order and name.
    :param query_parameters: Parameters of the form key1=value1&key2=value2
    :return: A dictionary with all the query parameters.
    """
    params = {'types': [], 'limit': int(10), 'offset': int(0), 'order': None, 'filters': []}
    query_parameters_as_list = query_parameters.split('&')
    for query_tuple in query_parameters_as_list:
        key = query_tuple.split('=')[0]
        value = query_tuple.split('=')[1]
        if value != '':
            if key == 'type':
                params['types'].append(value)
            elif key == 'name':
                params['filters'].append(('name', value))
            elif key == 'limit':
                params['limit'] = int(value)
            elif key == 'offset':
                params['offset'] = int(value)
    print("Params: ", params)
    return params


def get_kinds(cls, url_query_string):
    """
    Query entities of the given Kind using the query parameters of the
    :param cls: The Kind in the Database
    :param url_query_string: Query parameters of the form key=value&key=value...
    :return: A set of entities of the given Kind
    """
    if url_query_string:
        params = parse_url_query_parameters(url_query_string)
        filters_ = create_filters(cls, params['filters'])
        entities = get_entities(cls, limit=params['limit'], offset_=params['offset'], filters=filters_)
        return entities
    else:
        entities = get_entities(cls)
        return entities


def create_filters(cls, filters_):
    """
    Given a list of tuples of the following form [(property,value), (property,value)...] a
    list of ndb filters are created for the given Kind. The filters created are of the form
    property == value, that is only equal-filters are created.
    :param cls: The Kind in the Database
    :param filters_: List of tuples with property-value pairs.
    :return: A list of filters for the given Kind
    """
    filters_as_list = []
    for f in filters_:
        if f[0] == 'name':
            filters_as_list.append(cls.name == f[1])

    print("Filters: ", filter)
    return filters_as_list
