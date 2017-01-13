from google.appengine.ext import ndb
from python.api.exceptions import BadRequest, EntityNotFound
from python.db.databaseKinds import UserRating


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
        raise BadRequest("No entity with name " + entity_name + " exists")


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
    Id may need typecasting to make sure it is int or string.
    :param cls: The Kind in the Database
    :param entity_id: The ID of the entity
    :return: An Entity of the given Kind with the given ID. If no entity is found with the given ID
    a ValueError will be raised.
    """
    entity = cls.get_by_id(entity_id)
    if entity:
        return entity
    else:
        raise EntityNotFound("Entity does not exist!")


def parse_url_query_parameters(query_parameters):
    """
    Parses all the query parameters and but them in a dictionary that is returned.
    The following parameter-keys can be detected: type, limit, offset, order and name.
    :param query_parameters: Parameters of the form key1=value1&key2=value2
    :return: A dictionary with all the query parameters.
    """
    params = {
        'types': [],
        'limit': int(10),
        'offset': int(0),
        'order': None,
        'filters': [],
    }
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
            else:
                raise BadRequest("Bad query")
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
        if len(params['types']) > 0:
            raise BadRequest("Bad query")
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
    property == value, that is only equal-filters are created. NOTE: Right now this
    method can only make name=some_name filters
    :param cls: The Kind in the Database
    :param filters_: List of tuples with property-value pairs.
    :return: A list of filters for the given Kind
    """
    filters_as_list = []
    for f in filters_:
        if f[0] == 'name':
            filters_as_list.append(cls.name == f[1])

    return filters_as_list


def get_children(child_cls, parent_cls, parent_id):
    """
    queries the children of the parent
    :param child_cls: the class of the children
    :param parent_cls: the class of the parent
    :param parent_id: id of the parent
    :return: All the children of the parent
    """
    parent_key = ndb.Key(parent_cls, parent_id)
    query = child_cls.query(child_cls.owner == parent_key)
    children = query.fetch()
    return children


def has_child_with_name(child_cls, child_name, parent_cls, parent_id):
    """
    Check if the parent with the given id has a child with the given name. This
    can be used to avoid having children with identical names.
    :param child_cls: The class of the child
    :param child_name: The name of the child search after
    :param parent_cls: The class of the parent
    :param parent_id: Unique ID of the parent
    :return: True if the parent has a child with the given name, else False
    """
    parent_key = ndb.Key(parent_cls, parent_id)
    query = child_cls.query(child_cls.name == child_name, child_cls.owner == parent_key)
    child = query.fetch(1)

    if child:
        return True
    else:
        return False


def create_key(cls, id):
    """
    creates a key with class cls and id = id
    """
    return ndb.Key(cls, id)


def add_rating(cls, entity, account, rating):
    '''
    Adds rating to entity. Checks so the person can only rate once,
    but can change from like to dislike.
    '''
    already_rated = False
    for user_rating in account.ratings:
        if user_rating.rated_key == entity.key:
            already_rated = True
            value = user_rating.value
            if rating == "1" and not value:
                entity.rating.likes += 1
                entity.rating.dislikes -= 1
                user_rating.value = True
                account.put()
            elif rating == "0" and value:
                entity.rating.dislikes += 1
                entity.rating.likes -= 1
                user_rating.value = False
                account.put()
            return entity

    if not already_rated:
        new_user_rating = UserRating(rated_key=entity.key, value=bool(int(rating)))
        account.ratings.append(new_user_rating)
        account.put()
        if rating == "1":
            entity.rating.likes += 1
        elif rating == "0":
            entity.rating.dislikes += 1
        else:
            raise BadRequest("rating must be 0 or 1")
    return entity


def have_rated(account, entity):
    '''
    Returns true if the person has rated the entity.
    '''
    for user_rating in account.ratings:
        if user_rating.rated_key == entity.key:
            return user_rating
