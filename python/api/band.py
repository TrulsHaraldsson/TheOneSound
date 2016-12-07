import json
import webapp2

from python.db.databaseKinds import Rating, Description, Comment, Band, Account
from python.api import common
from python.util import entityparser, loginhelper


class BandHandler(webapp2.RequestHandler):
    def post(self):
        band_name = self.request.get("name")
        description_text = self.request.get("description")
        try:
            entity_id = create_band(band_name, description_text)
            json_obj = entityparser.entity_id_to_json(entity_id)
            self.response.out.write(json_obj)
        except Exception as e:
            print e
            self.response.set_status(404)

    def get(self):
        bands = common.get_kinds(Band, self.request.query_string)
        band_list = entityparser.entities_to_dic_list(bands)
        json_list = json.dumps(band_list)
        self.response.out.write(json_list)


class BandByIdHandler(webapp2.RequestHandler):
    def get(self, band_id):
        try:
            band = common.get_entity_by_id(Band, int(band_id))
            band_dic = entityparser.entity_to_dic(band)
            self.response.out.write(json.dumps(band_dic))
        except Exception as e:
            print e
            self.response.set_status(404)

    # updates a band with the new information
    def put(self, band_id):
        try:
            description_text = self.request.get("description")
            comment_text = self.request.get("comment_text")
            rating = self.request.get("rating")
            update_band(description_text, comment_text, int(band_id), rating)

        except Exception as e:
            print (e)
            self.response.set_status(404)


# Not tested yet.
def update_band(description_text, comment_text, band_id, rating_):
    user_id = loginhelper.get_user_id()
    band = common.get_entity_by_id(Band, int(band_id))
    if description_text != "":
        description = Description(description=description_text)
        band.description = description
    if comment_text != "":
        parent_key = common.create_key(Account, user_id)
        comment = Comment(owner=parent_key, content=comment_text)
        rating = Rating(likes=0, dislikes=0)
        comment.rating = rating
        band.comment.append(comment)
    if rating_ != "":
        if rating_ == "1":
            band.rating.likes += 1
        elif rating_ == "0":
            band.rating.dislikes += 1
    # TODO: add rating
    band.put()


def create_band(band_name, description):
    if band_name == "":
        raise ValueError("Band must have a name.")

    band = Band(name=band_name, comment=[])

    if description != "":
        desc = Description(description=description)
        band.description = desc
    # rating not tested
    rating = Rating(likes=0, dislikes=0)
    band.rating = rating
    band.put()
    return band.key.id()


# [START app]
app = webapp2.WSGIApplication([
    ('/api/bands', BandHandler),
    ('/api/bands/(\d+)', BandByIdHandler)
], debug=True)
# [END app]
