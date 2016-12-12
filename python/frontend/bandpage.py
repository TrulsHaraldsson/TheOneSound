import webapp2

from python.frontend import JINJA_ENVIRONMENT
from python.api import common
from python.db.databaseKinds import Band, Album, Track
from python.util import entityparser
from python.util import loginhelper, templatehelper, urlhelper


class BandsCreate(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        loginhelper.add_login_values(template_values, self)
        template = JINJA_ENVIRONMENT.get_template('pages/bands/create.html')
        self.response.write(template.render(template_values))


class BandsDisplay(webapp2.RequestHandler):
    def get(self, band_id):
        template_values = {}
        loginhelper.add_login_values(template_values, self)
        try:
            band = common.get_entity_by_id(Band, int(band_id))
            band_dic = entityparser.entity_to_dic(band)
            add_band_and_decendants(template_values, band_dic)
            templatehelper.add_rated(template_values, band)
            template = JINJA_ENVIRONMENT.get_template('pages/bands/display.html')
            self.response.write(template.render(template_values))
        except Exception as e:
            print "Bandpage: ", e
            template = JINJA_ENVIRONMENT.get_template('pages/bands/create.html')
            self.response.write(template.render(template_values))


def add_band_and_decendants(template_values, band):
    # 1: fetch all albums belonging to band
    #   2: fetch all tracks belonging to album
    template_values["band"] = band
    albums = common.get_children(Album, Band, int(band["id"]))
    albums_dic = entityparser.entities_to_dic_list(albums)
    for album in albums_dic:
        tracks = common.get_children(Track, Album, int(album["id"]))
        tracks_dic = entityparser.entities_to_dic_list(tracks)
        album["tracks"] = tracks_dic
    template_values["albums"] = albums_dic
    urlhelper.attach_links("/albums/", template_values["albums"])


# [START app]
app = webapp2.WSGIApplication([
    ('/bands/create', BandsCreate),
    ('/bands/(\d+)', BandsDisplay)
], debug=True)
# [END app]
