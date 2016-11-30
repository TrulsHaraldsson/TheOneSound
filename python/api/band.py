import webapp2
import json
from python.databaseKinds import Rating, Description, Comment, Band, Account
from python.api import common
from python.api import search
from python.util import entityparser
from python import JINJA_ENVIRONMENT
from google.appengine.ext import ndb
from google.appengine.api import users

class BandHandler(webapp2.RequestHandler):
    #create
    #creates one new band
    def post(self):
        band_name = self.request.get("name")
        description_text = self.request.get("description")
        try:
            create_new_band(band_name, description_text)
        except Exception as e:
            self.response.set_status(404)

    #request
    #gives list of matching bands
    def get(self):
        limit = self.request.get("limit")
        query_string = self.request.query_string
        bands = common.get_entities(Band, limit)
        band_list = entityparser.entities_to_dic_list(bands)

        json_list = json.dumps(band_list)
        self.response.out.write(json_list)
    #update
    #def put(self):


    #delete
    #def delete(self):

class BandByIdHandler(webapp2.RequestHandler):
    def get(self, band_id):
        try:
            band = common.get_entity_by_id(Band, int(band_id))
            band_dic = entityparser.entity_to_dic(band)
            self.response.out.write(json.dumps(band_dic))
        except Exception as e:
            self.response.set_status(404)

    #updates a band with the new information
    def put(self, band_id):
        try:
            description_text = self.request.get("description")
            comment_text = self.request.get("comment_text")
            user_id = self.request.get("user_id")
            update_band(description_text, comment_text, int(band_id), user_id)

        except Exception as e:
            print e
            self.response.set_status(404)


class BandByNameHandler(webapp2.RequestHandler):
    #returns all bands with matching name
    def get(self, band_name):
        try:
            bands = common.get_entities_by_name(Band, band_name)
            if len(bands) > 1:
                self.response.set_status(300) #muliple choices
            else:
                band_list = entityparser.entities_to_dic_list(bands)
                self.response.out.write(json.dumps(band_list))
        except Exception as e:
            self.response.set_status(404)


######################
#####API Functions ###
######################


# Not tested yet.
def update_band(description_text, comment_text, band_id, user_id):
    band = common.get_entity_by_id(Band, int(band_id))
    if description_text != "":
        description = Description(description=description_text)
        band.description = description
    if comment_text != "":
        parent_key = ndb.Key(Account, user_id)
        comment = Comment(parent=parent_key, content=comment_text)
        rating = Rating(likes=0, dislikes=0)
        comment.rating = rating

        band.comment.append(comment)
    #TODO: add rating
    band.put()




def create_new_band(band_name, description):
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


# [START app]
app = webapp2.WSGIApplication([
    ('/api/band', BandHandler),
    ('/api/band/(\d+)', BandByIdHandler),
    ('/api/band/(\w+)', BandByNameHandler)
], debug=True)
# [END app]
