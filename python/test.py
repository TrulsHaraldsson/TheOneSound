
import webapp2
import jinja2
import databaseKinds
import json

from google.appengine.ext import ndb

from python import JINJA_ENVIRONMENT
from python.util import loginhelper

class Test(webapp2.RequestHandler):
    def post(self):
        band_name = self.request.get("band_name")
        band = databaseKinds.Band(name=band_name)
        album_name = self.request.get("album_name")
        track_name = self.request.get("track_name")
        band_key = band.put()
        album = databaseKinds.Album(parent=band_key, name=album_name)
        album_key = album.put()
        track = databaseKinds.Track(parent=album_key, name=track_name)
        track.put()
        track_json = json.dumps(track)
        print(track_json)
        template = JINJA_ENVIRONMENT.get_template('about.html')
        self.response.write(template.render())

# [START app]
app = webapp2.WSGIApplication([
    ('/test', Test)
], debug=True)
# [END app]
