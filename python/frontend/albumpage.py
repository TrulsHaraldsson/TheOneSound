import webapp2
from python.db.databaseKinds import Album, Track
from python.frontend import JINJA_ENVIRONMENT
from python.util import loginhelper, entityparser, templatehelper
from python.api import common


class AlbumPageUpdate(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        loginhelper.add_login_values(template_values, self)
        template = JINJA_ENVIRONMENT.get_template('albumpage/update.html')
        self.response.write(template.render(template_values))


class AlbumPageDisplay(webapp2.RequestHandler):
    def get(self, album_id):
        template_values = {}
        loginhelper.add_login_values(template_values, self)
        try:
            album = common.get_entity_by_id(Album, int(album_id))
            album_dic = entityparser.entity_to_dic(album)
            add_album_and_decendants(template_values, album_dic)
            templatehelper.add_rated(template_values, album)
            template = JINJA_ENVIRONMENT.get_template('albumpage/display.html')
            self.response.write(template.render(template_values))
        except Exception as e:
            print(e)
            template = JINJA_ENVIRONMENT.get_template('albumpage/update.html')
            self.response.out.write(template.render(template_values))


def add_album_and_decendants(template_values, album):
    # 1: fetch all tracks belonging to album
    template_values["album"] = album
    tracks = common.get_children(Track, Album, int(album["id"]))
    tracks_dic = entityparser.entities_to_dic_list(tracks)
    template_values["tracks"] = tracks_dic


# [START app]
app = webapp2.WSGIApplication([
    ('/albumpage/update', AlbumPageUpdate),
    ('/albumpage/(\d+)', AlbumPageDisplay)
], debug=True)
# [END app]
