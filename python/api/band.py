import json
import webapp2

from python.db.databaseKinds import Rating, BandDescription, Comment, Band, Account
from python.api import common
from python.api.exceptions import BadRequest, EntityNotFound
from python.util import entityparser, loginhelper


class BandHandler(webapp2.RequestHandler):
    def post(self):
        band_name = self.request.get("name")
        try:
            entity_id = create_band(band_name)
            json_obj = entityparser.entity_id_to_json(entity_id)
            self.response.out.write(json_obj)
        except BadRequest:
            self.response.set_status(400)

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
        except BadRequest:
            self.response.set_status(400)
        except EntityNotFound:
            self.response.set_status(404)

    # updates a band with the new information
    def put(self, band_id):
        try:
            update_band(int(band_id), self.request.POST)
        except BadRequest:
            self.response.set_status(400)
        except EntityNotFound:
            self.response.set_status(404)


# Not tested yet.
def update_band(band_id, post_params):
    user_id = loginhelper.get_user_id()
    band = common.get_entity_by_id(Band, int(band_id))
    if 'description' in post_params.keys():
        description = post_params['description']
        band.description.description = description
    if 'genre' in post_params.keys():
        print("genre")
        genre = post_params['genre']
        band.description.genres.append(genre)
    if 'member' in post_params.keys():
        member = post_params['member']
        band.description.members.append(member)
    if 'picture_url' in post_params.keys():
        picture_url = post_params['picture_url']
        band.description.picture_url = picture_url
    if 'comment_text' in post_params.keys():
        comment_text = post_params['comment_text']
        parent_key = common.create_key(Account, user_id)
        comment = Comment(owner=parent_key, content=comment_text)
        rating = Rating(likes=0, dislikes=0)
        comment.rating = rating
        band.comment.insert(0, comment)
    if 'rating' in post_params.keys():
        rating = post_params['rating']
        account = common.get_entity_by_id(Account, str(user_id))
        band = common.add_rating(Band, band, account, rating)
    band.put()


def create_band(band_name):
    if band_name == "":
        raise ValueError("Band must have a name.")

    band = Band(name=band_name, comment=[])
    desc = BandDescription(description="", members=[], genres=[])
    band.description = desc
    # rating not tested
    rating = Rating(likes=0, dislikes=0)
    band.rating = rating
    band_key = band.put()
    picture_url = "https://storage.googleapis.com/theonesound-148310.appspot.com/bands/"+str(band_key.id())
    band.description.picture_url = picture_url
    band.put()
    return band_key.id()


# [START app]
app = webapp2.WSGIApplication([
    ('/api/bands', BandHandler),
    ('/api/bands/(\d+)', BandByIdHandler)
], debug=True)
# [END app]
