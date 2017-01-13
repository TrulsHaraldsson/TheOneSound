import json
import webapp2

from python.db.databaseKinds import Rating, TopList, Account, Track, Album, Band
from python.api import common
from python.api.exceptions import BadRequest, NotAuthorized
from python.util import entityparser, loginhelper


class TopListHandler(webapp2.RequestHandler):
    """
    The TopListHandler listen for HTTP POST and GET requests on the URL /api/toplists.
    """
    def post(self):
        """
        Creates a new toplist if the POST request delivered sufficient information. The POST request must
        contain the key "name" and type, else a HTTP 400 error is returned.
        :param name: Name of the toplist
        :param type: wich type of content is to be in the toplist
        :return: The newly created toplist as a JSON string
        """
        toplist_name = self.request.get("name")
        toplist_type = self.request.get("type")
        try:
            loginhelper.check_logged_in()
            entity_id = create_toplist(toplist_name, toplist_type)
            json_obj = entityparser.entity_id_to_json(entity_id)
            self.response.out.write(json_obj)
        except NotAuthorized:
            self.response.set_status(401)
        except Exception:
            self.response.set_status(400)

    def get(self):
        """
        The GET request can have the following url parameters to specify a query. This method can return HTTP 400
        error code.
        :param name: Return only toplists with the given name, if name is absent all toplists will be queried
        :param limit: Upper bound of toplists that will be returned. Default is 10.
        :param offset_: The number of toplists in the query that are initially skipped. Default is 0
        :return: A list of toplists as a JSON string
        """
        toplists = common.get_kinds(TopList, self.request.query_string)
        toplist_list = entityparser.entities_to_dic_list(toplists)
        json_list = json.dumps(toplist_list)
        self.response.out.write(json_list)


class TopListByIdHandler(webapp2.RequestHandler):
    """
    The TopListByIdHandler listen for HTTP PUT and GET requests on the URL /api/toplists/id, where the id part is
    a unique id for an toplist.
    """
    def get(self, toplist_id):
        """
        Returns an toplist given a unique id. If the id is not associated with any toplist an HTTP 404 error is returned.
        :param toplist_id: A unique toplist id
        :return: An toplist as a JSON string
        """
        try:
            toplist = common.get_entity_by_id(TopList, int(toplist_id))
            toplist_dic = entityparser.entity_to_dic(toplist)
            self.response.out.write(json.dumps(toplist_dic))
        except Exception:
            self.response.set_status(404)

    # updates a toplist with the new information
    def put(self, toplist_id):
        """
        The PUT method is used to update an existing toplist with the given id. If the toplist does not exist an HTTP
        404 error is returned.
        :param toplist_id: Unique id of an toplist
        :return: a toplist as a json string
        """
        try:
            loginhelper.check_logged_in()
            update_toplist(int(toplist_id), self.request.POST)
        except NotAuthorized:
            self.response.set_status(401)
        except Exception:
            self.response.set_status(404)


def update_toplist(toplist_id, post_params):
    '''
    adds content or rating to toplist with specified id.
    '''
    toplist = common.get_entity_by_id(TopList, int(toplist_id))
    if 'content_id' in post_params:
        content_id = int(post_params['content_id'])
        if toplist.kind == "track":
            content_key = common.create_key(Track, content_id)
        elif toplist.kind == "album":
            content_key = common.create_key(Album, content_id)
        else:
            content_key = common.create_key(Band, content_id)
        if content_key.get():
            toplist.content.append(content_key)
    if 'rating' in post_params:
        rating = post_params['rating']
        account = common.get_entity_by_id(Account, str(loginhelper.get_user_id()))
        toplist = common.add_rating(TopList, toplist, account, rating)
    toplist.put()


def create_toplist(toplist_name, toplist_type):
    '''
    creates new toplist with specified name and type. also sets default values.
    '''
    if toplist_name == "":
        raise BadRequest("toplist must have a name.")
    if toplist_type != "track" and toplist_type != "album" and toplist_type != "band":
        raise BadRequest("toplist type is incorrect.")
    owner_key = common.create_key(Account, str(loginhelper.get_user_id()))
    toplist = TopList(name=toplist_name, content=[], owner=owner_key, kind=toplist_type)
    rating = Rating(likes=0, dislikes=0)
    toplist.rating = rating
    toplist.put()
    return toplist.key.id()


# [START app]
app = webapp2.WSGIApplication([
    ('/api/toplists', TopListHandler),
    ('/api/toplists/(\d+)', TopListByIdHandler)
], debug=True)
# [END app]
