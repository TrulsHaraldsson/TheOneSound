import json
import webapp2

from python.db.databaseKinds import Rating, TopList, Account, Track, Album, Band
from python.api import common
from python.api.exceptions import BadRequest
from python.util import entityparser, loginhelper


class TopListHandler(webapp2.RequestHandler):
    def post(self):
        toplist_name = self.request.get("name")
        toplist_type = self.request.get("type")
        print "toplist name: " + toplist_name
        try:
            entity_id = create_toplist(toplist_name, toplist_type)
            json_obj = entityparser.entity_id_to_json(entity_id)
            self.response.out.write(json_obj)
        except Exception as e:
            print e
            self.response.set_status(400)

    def get(self):
        toplists = common.get_kinds(TopList, self.request.query_string)
        toplist_list = entityparser.entities_to_dic_list(toplists)
        json_list = json.dumps(toplist_list)
        self.response.out.write(json_list)


class TopListByIdHandler(webapp2.RequestHandler):
    def get(self, toplist_id):
        try:
            toplist = common.get_entity_by_id(TopList, int(toplist_id))
            toplist_dic = entityparser.entity_to_dic(toplist)
            self.response.out.write(json.dumps(toplist_dic))
        except Exception as e:
            print e
            self.response.set_status(404)

    # updates a toplist with the new information
    def put(self, toplist_id):
        try:
            content_id = self.request.get("content_id")
            update_toplist(int(toplist_id), int(content_id))

        except Exception as e:
            print (e)
            self.response.set_status(404)


# Not tested yet.
def update_toplist(toplist_id, content_id):
    toplist = common.get_entity_by_id(TopList, int(toplist_id))

    if content_id != "":
        if toplist.kind == "track":
            content_key = common.create_key(Track, content_id)
        elif toplist.kind == "album":
            content_key = common.create_key(Album, content_id)
        else:
            content_key = common.create_key(Band, content_id)
        toplist.content.append(content_key)
    # TODO: add rating
    toplist.put()


def create_toplist(toplist_name, toplist_type):
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
