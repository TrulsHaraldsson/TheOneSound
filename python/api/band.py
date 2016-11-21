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
    def post(self):
        band_name = self.request.get("band_name")

        description_text = self.request.get("description")
        try:
            BandHandler.create_new_band(band_name, description_text)
        except Exception as e:
            print e
            self.response.set_status(400)

    @staticmethod
    def create_new_band(band_name, description):
        if band_name == "":
            raise ValueError("Band must have a name.")
        band_key = ndb.Key("Band", band_name)
        if band_key.get() == None:
            band = Band(id=band_name, name=band_name)

            if description != "":
                desc = Description(description=description)
                band.description = desc

            band.put()
        else:
            raise ValueError("Band with that name already exists.")


    #request
    def get(self):
        JINJA_ENVIRONMENT.get_template("about.html")
        amount = self.request.get("amount")
        query = Band.query()
        if amount != "":
            bands = query.fetch(amount)
        else:
            amount = 10
            bands = query.fetch(amount)
        band_list = []
        for band in bands:
            band_list.append(band.to_dict())

        json_list = json.dumps(band_list)
        self.response.out.write(json_list)
    #update
    #def put(self):


    #delete
    #def delete(self):

class BandByIdHandler(webapp2.RequestHandler):
    def get(self, id):
        band = Band.get_by_id(id)
        self.response.out.write(json.dumps(band.to_dict()))

    def put(self, id):
        band = Band.get_by_id(id)
        desc = self.get.request("description")
        if desc != "":
            band.description.description = desc

class BandByNameHandler(webapp2.RequestHandler):
    def get(self, band_name):
        try:
            band = BandByNameHandler.get_band_by_name(band_name)
            self.response.out.write(json.dumps(band))
        except Exception as e:
            self.response.set_status(400)



    @staticmethod
    def get_band_by_name(band_name):
        band_key = ndb.Key("Band", band_name)
        band = band_key.get()
        if band != None:
            return band
        else:
            raise ValueError("No such band exists!")

    def put(self, band_name):
        try:
            band = BandByNameHandler.get_band_by_name(band_name)
            description_text = self.request.get("description")
            comment_text = self.request.get("comment")
            BandByNameHandler.update_band(description_text, comment_text)

        except Exception as e:
            self.response.set_status(400)
    #Not tested yet.
    @staticmethod
    def update_band(description_text, comment_text):
        if description_text != "":
            description = Description(description=description_text)
            band.description = description
        if comment_text != "":
            comment = Comment(content=comment_text)
            rating = Rating(likes=0, dislikes=0)
            comment.rating = rating
            #TODO: also add user key
            band.comment = comment
        rating = Rating(likes=0, dislikes=0)
        band.rating = rating


# [START app]
app = webapp2.WSGIApplication([
    ('/api/band', BandHandler),
    ('/api/band/(\d+)', BandByIdHandler),
    ('/api/band/(\w+)', BandByNameHandler)
], debug=True)
# [END app]
