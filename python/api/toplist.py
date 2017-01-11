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
        try:
            toplist = common.get_entity_by_id(TopList, int(toplist_id))
            toplist_dic = entityparser.entity_to_dic(toplist)
            self.response.out.write(json.dumps(toplist_dic))
        except Exception:
            self.response.set_status(404)

    # updates a toplist with the new information
    def put(self, toplist_id):
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
