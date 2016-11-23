import webapp2
import json
from python.databaseKinds import Rating
from python.databaseKinds import Description
from python.databaseKinds import Comment
from python.databaseKinds import Band
from python import JINJA_ENVIRONMENT
from google.appengine.ext import ndb
from google.appengine.api import users


class TrackHandler(webapp2.RequestHandler):
    def get(self):
        

# [START app]
app = webapp2.WSGIApplication([
    ('/api/track', BandHandler),
    ('/api/track/(\w+)', BandByNameHandler)
], debug=True)
# [END app]
