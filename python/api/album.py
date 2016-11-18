import webapp2
import json
from python import databaseKinds
from python import JINJA_ENVIRONMENT

class AlbumHandler(webapp2.RequestHandler):
    def get(self, name):
        query = databaseKinds.Album.query('name =', name)
        album = query.fetch(1)

        albumAsJSON = json.dumps(album.to_dict())

        template_values = {
            'name': album.name,
            'description': album.description,
            'json': albumAsJSON
        }

        template = JINJA_ENVIRONMENT.get_template('albumapitest.html')
        self.response.out.write(template.render(template_values))



# [START app]
app = webapp2.WSGIApplication([
    ('/api/album/(\w+)', AlbumHandler),
], debug=True)
# [END app]