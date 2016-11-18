import webapp2
import json
from python.databaseKinds import Rating
from python.databaseKinds import Description
from python.databaseKinds import Comment
from python.databaseKinds import Band
from python import JINJA_ENVIRONMENT

class BandHandler(webapp2.RequestHandler):
    #create
    def post(self):
        band_name = self.request.get("band_name")
        #if band_name == "":
            #exit - band must have name
        band = Band(name=band_name)
        description_text = self.request.get("description")
        if description_text != "":
            desc = Description(description=description_text)
            band.description = desc

        band.put()


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
        self.response.out.write(band.to_dict())

    def put(self, id):
        band = Band.get_by_id(id)
        desc = self.get.request("description")
        if desc != "":
            band.description.description = desc

class BandByNameHandler(webapp2.RequestHandler):
    def get(self, id):
        print("name: " + id)
# [START app]
app = webapp2.WSGIApplication([
    ('/api/band', BandHandler),
    ('/api/band/(\d+)', BandByIdHandler),
    ('/api/band/(\w+)', BandByNameHandler)
], debug=True)
# [END app]
