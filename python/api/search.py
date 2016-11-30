from python.api import common
from python.databaseKinds import Album, Band, Track


def query_kind_by_name(cls, query_parameters):
    """
    Query all entities for a given Kind that matches the given query parameters. This function also
    check if the query parameters follows the format i.e. type1=value1?type2=value2 etc. And will
    in the case of bad format raise an error
    NOTE: Right now this function only query entities by name.
    :param cls: The Kind in the Database
    :param query_parameters: The query parameters
    :return: A list of entities from the given Kind
    """
    query_parameters_as_list = query_parameters.split('&')
    for query_tuple in query_parameters_as_list:
        type_ = query_tuple.split('=')[0]
        value = query_tuple.split('=')[1]
        if type_ == 'name' and value != '':
            entities = common.get_entities_by_name(cls, value)
            return entities
        else:
            raise ValueError("Bad request")


def query_kinds_by_name(query_parameters):
    """
    Query all entities that matches the given query parameters. This function also
    check if the query parameters follows the format i.e. type1=value1?type2=value2 etc. And will
    in the case of bad format raise an error
    NOTE: Right now this function only query entities by name
    :param query_parameters: The query parameters
    :return: A dictionary with Kind names as keys and the found entities for each Kind as values.
    """
    query_parameters_as_list = query_parameters.split('&')
    for query_tuple in query_parameters_as_list:
        type_ = query_tuple.split('=')[0]
        value = query_tuple.split('=')[1]
        if type_ == 'name' and value != '':
            bands = common.get_entities_by_name(Band, value)
            albums = common.get_entities_by_name(Album, value)
            tracks = common.get_entities_by_name(Track, value)
            dictionary = {'Bands':bands, 'Albums':albums, 'Tracks':tracks}
            return dictionary
        else:
            raise ValueError("Bad request")
