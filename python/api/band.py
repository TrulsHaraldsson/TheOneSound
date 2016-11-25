import webapp2
import json
from python.databaseKinds import Rating
from python.databaseKinds import Description
from python.databaseKinds import Comment
from python.databaseKinds import Band
from python.util import entityparser
from python import JINJA_ENVIRONMENT
from google.appengine.ext import ndb
from google.appengine.api import users

class BandHandler(webapp2.RequestHandler):
    #create
    #creates one new band
    def post(self):
        band_name = self.request.get("band_name")
        description_text = self.request.get("description")
        try:
            create_new_band(band_name, description_text)
        except Exception as e:
            self.response.set_status(400)

    #request
    #gives list of matching bands
    def get(self):
        limit = self.request.get("limit")
        bands = get_multiple_bands(limit)
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
            band = get_band_by_id(band_id)
            band_dic = entityparser.entity_to_dic(band)
            self.response.out.write(json.dumps(band_dic))
        except Exception as e:
            self.response.set_status(400)

    #updates a band with the new information
    def put(self, band_id):
        try:
            description_text = self.request.get("description")
            comment_text = self.request.get("comment")
            update_band(description_text, comment_text, band_id)

        except Exception as e:
            self.response.set_status(400)


class BandByNameHandler(webapp2.RequestHandler):
    #returns all bands with matching name
    def get(self, band_name):
        try:
            bands = get_bands_by_name(band_name)
            if len(bands) > 1:
                self.response.set_status(300) #muliple choices
            else:
                band_list = entityparser.entities_to_dic_list(bands)
                self.response.out.write(json.dumps(band_list))
        except Exception as e:
            self.response.set_status(400)


######################
#####API Functions ###
######################

def get_bands_by_name(band_name):
    return entityparser.get_entities_by_name(Band, band_name)


# Not tested yet.
def update_band(description_text, comment_text, band_id):
    band = entityparser.get_entity_by_id(band_id)
    if description_text != "":
        description = Description(description=description_text)
        band.description = description
    if comment_text != "":
        comment = Comment(content=comment_text)
        comment.rating = rating
        #TODO: also add user key
        band.comment = comment
    #TODO: add rating
    band.put()



def create_new_band(band_name, description):
    if band_name == "":
        raise ValueError("Band must have a name.")

    band = Band(name=band_name)

    if description != "":
        desc = Description(description=description)
        band.description = desc
    # rating not tested
    rating = Rating(likes=0, dislikes=0)
    band.rating = rating
    band.put()


def get_multiple_bands(limit):
    return entityparser.get_multiple_entities(Band, limit)


def get_band_by_id(id):
    return entityparser.get_entity_by_id(Band, id)

# [START app]
app = webapp2.WSGIApplication([
    ('/api/band', BandHandler),
    ('/api/band/(\d+)', BandByIdHandler),
    ('/api/band/(\w+)', BandByNameHandler)
], debug=True)
# [END app]
