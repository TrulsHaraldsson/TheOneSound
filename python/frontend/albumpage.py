import webapp2
from python.db.databaseKinds import Album, Track
from python.frontend import JINJA_ENVIRONMENT
from python.util import loginhelper, entityparser, templatehelper, urlhelper
from python.api import common
from python.api.exceptions import EntityNotFound


class AlbumsDisplay(webapp2.RequestHandler):
    def get(self, album_id):
        template_values = {}
        loginhelper.add_login_values(template_values, self)
        try:
            album = common.get_entity_by_id(Album, int(album_id))
            album_dic = entityparser.entity_to_dic(album)
            add_album_and_decendants(template_values, album_dic)
            templatehelper.add_rated(template_values, album)
            templatehelper.add_toplists(template_values, "album")
            template = JINJA_ENVIRONMENT.get_template('pages/albums/display.html')
            self.response.write(template.render(template_values))
        except EntityNotFound as e:
            self.response.set_status(404)


def add_album_and_decendants(template_values, album):
    template_values["album"] = album
    tracks = common.get_children(Track, Album, int(album["id"]))
    tracks_dic = entityparser.entities_to_dic_list(tracks)
    template_values["tracks"] = tracks_dic
    urlhelper.attach_links("/tracks/", template_values["tracks"])


# [START app]
app = webapp2.WSGIApplication([
    ('/albums/(\d+)', AlbumsDisplay)
], debug=True)
# [END app]
