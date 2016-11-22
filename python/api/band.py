import webapp2
import json
from python.databaseKinds import Rating
from python.databaseKinds import Description
from python.databaseKinds import Comment
from python.databaseKinds import Band
from python import JINJA_ENVIRONMENT
from google.appengine.ext import ndb

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

        band_list = []
        bands = get_multiple_bands(limit)
        for band in bands:
            band_list.append(band.to_dict())

        json_list = json.dumps(band_list)
        self.response.out.write(json_list)
    #update
    #def put(self):


    #delete
    #def delete(self):


class BandByNameHandler(webapp2.RequestHandler):
    #returns one band with matching name
    def get(self, band_name):
        try:
            band = get_band_by_name(band_name)
            self.response.out.write(json.dumps(band))
        except Exception as e:
            self.response.set_status(400)
    #updates a band with the new information
    def put(self, band_name):
        try:

            description_text = self.request.get("description")
            comment_text = self.request.get("comment")
            update_band(description_text, comment_text)

        except Exception as e:
            self.response.set_status(400)


def get_band_by_name(band_name):
    band = Band.get_by_id(band_name)
    if band != None:
        return band
    else:
        raise ValueError("No such band exists!")

#Not tested yet.
def update_band(description_text, comment_text):
    band = get_band_by_name(band_name)
    if band != None:
        if description_text != "":
            description = Description(description=description_text)
            band.description = description
        if comment_text != "":
            comment = Comment(content=comment_text)
            rating = Rating(likes=0, dislikes=0)
            comment.rating = rating
            #TODO: also add user key
            band.comment = comment
        #TODO: add rating
        band.put()
    else:
        raise ValueError("No such band exists!")


def create_new_band(band_name, description):
    if band_name == "":
        raise ValueError("Band must have a name.")
    band_key = ndb.Key("Band", band_name)
    if band_key.get() == None:
        band = Band(id=band_name, name=band_name)

        if description != "":
            desc = Description(description=description)
            band.description = desc
        #rating not tested
        rating = Rating(likes=0, dislikes=0)
        band.rating = rating
        band.put()
    else:
        raise ValueError("Band with that name already exists.")

def get_multiple_bands(limit):
    #TODO: filters should be made, also different sortings
    query = Band.query().order(Band.name)
    if amount != "":
        bands = query.fetch(limit)
    else:
        amount = 10
        bands = query.fetch(limit)
    return bands



# [START app]
app = webapp2.WSGIApplication([
    ('/api/band', BandHandler),
    ('/api/band/(\w+)', BandByNameHandler)
], debug=True)
# [END app]
