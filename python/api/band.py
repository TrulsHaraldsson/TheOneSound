import webapp2
import jinja2
import databaseKinds
import json

from python import JINJA_ENVIRONMENT

class Band(webapp2.RequestHandler):
    #create
    def post(self):
        band_name = self.request.get("band_name")
        band = databaseKinds.Band(name=band_name)
        band.put()


    #request
    def get(self):

    #update
    def put(self):

    #delete
    def delete(self):


# [START app]
app = webapp2.WSGIApplication([
    ('/api/band', Band)
], debug=True)
# [END app]
