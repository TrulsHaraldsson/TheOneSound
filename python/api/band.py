import webapp2
import jinja2
import python.databaseKinds
import json

from python import JINJA_ENVIRONMENT

class Band(webapp2.RequestHandler):
    #create
    def post(self):
        band_name = self.request.get("band_name")
        band = databaseKinds.Band(name=band_name)
        description_text = self.request.get("description")
        if description_text != "":
            desc = Description(description=description_text)
            band.description = desc

        band.put()


    #request
    #def get(self):

    #update
    #def put(self):

    #delete
    #def delete(self):

class BandById(webapp2.RequestHandler):
    def get(self, id):
        print("id: " +id)

class BandByName(webapp2.RequestHandler):
    def get(self, id):
        print("name: " + id)
# [START app]
app = webapp2.WSGIApplication([
    ('/api/band', Band),
    ('/api/band/(\d+)', BandById),
    ('/api/band/(\w+)', BandByName)
], debug=True)
# [END app]
