import webapp2
import json
from python.databaseKinds import Album
from python.databaseKinds import Description
from python import JINJA_ENVIRONMENT

class AlbumHandler(webapp2.RequestHandler):
    def post(self):
        album_name = self.request.get("album_name")
        query = Album.query(Album.name == album_name)
        album = query.fetch(1)
        if album:
            print ("WTF");
            return
        else:
            albumDescription = self.request.get("description");
            album = Album(name = album_name, description = Description(description = albumDescription))
            album.put()

class AlbumHandlerByName(webapp2.RequestHandler):
    def get(self, qname):
        print("qName = " + qname)
        query = Album.query(Album.name == qname)
        album = query.fetch(1)

        albumAsJSON = json.dumps(album[0].to_dict())

        template_values = {
            #'name': album.name,
            #'description': album.description,
            'json': albumAsJSON
        }

        template = JINJA_ENVIRONMENT.get_template('albumpage/display.html')
        self.response.out.write(template.render(template_values))




# [START app]
app = webapp2.WSGIApplication([
    ('/api/album', AlbumHandler),
    ('/api/album/(\w+)', AlbumHandlerByName)

], debug=True)
# [END app]