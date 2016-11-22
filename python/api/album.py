import webapp2
import json
from python.databaseKinds import Album
from python.databaseKinds import Description
from python import JINJA_ENVIRONMENT
from google.appengine.ext import ndb

class AlbumHandler(webapp2.RequestHandler):
    def post(self):
        album_name = self.request.get("album_name")
        albumDescription = self.request.get("description");
        album = Album(name = album_name, description = Description(description = albumDescription))
        album.put()

class AlbumHandlerByName(webapp2.RequestHandler):
    def get(self, qname):
        limit_ = self.request.get("limit")
        offset_ = self.request.get("offset")

        #albums = get_album_by_name(qname, limit, offset)

        qo = ndb.QueryOptions(offset = int(offset_), limit = int(limit_) )
        albums = get_album_by_(qname, qo)

        album_list = []
        for album in albums:
            album_list.append(album.to_dict())

        albumAsJSON = json.dumps(album_list)

        template_values = {
            #'name': album.name,
            #'description': album.description,
            'json': albumAsJSON
        }

        template = JINJA_ENVIRONMENT.get_template('albumpage/display.html')
        self.response.out.write(template.render(template_values))

def get_album_by_(name_, qo_):
    query = Album.query(Album.name == name_)
    qo1_ = ndb.QueryOptions(offset=0)
    albums = query.fetch(10, qo1_)
    return albums

def get_album_by_name(name_, limit_=10, offset_=0):
    query = Album.query(Album.name == name_)
    albums = query.fetch(int(limit_), offset = int(offset_))
    return albums

# [START app]
app = webapp2.WSGIApplication([
    ('/api/album', AlbumHandler),
    ('/api/album/(\w+)', AlbumHandlerByName)

], debug=True)
# [END app]