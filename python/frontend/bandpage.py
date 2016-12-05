import webapp2

from python.frontend import JINJA_ENVIRONMENT
from python.api import common
from python.db.databaseKinds import Band, Album, Track
from python.util import entityparser
from python.util import loginhelper


class BandPageUpdate(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        loginhelper.add_login_values(template_values, self)
        template = JINJA_ENVIRONMENT.get_template('bandpage/update.html')
        self.response.write(template.render(template_values))


class BandPageDisplay(webapp2.RequestHandler):
    def get(self, band_id):
        template_values = {}
        loginhelper.add_login_values(template_values, self)
        try:
            print "1: -------------"
            band = common.get_entity_by_id(Band, band_id)
            print "2: -------------"
            band_dic = entityparser.entity_to_dic(band)
            add_band_and_decendants(template_values, band_dic)
            template = JINJA_ENVIRONMENT.get_template('bandpage/display.html')
            self.response.write(template.render(template_values))
        except Exception as e:
            print "Bandpage: ", e
            template = JINJA_ENVIRONMENT.get_template('bandpage/update.html')
            self.response.write(template.render(template_values))


def add_band_and_decendants(template_values, band):
    # 1: fetch all albums belonging to band
    #   2: fetch all tracks belonging to album
    template_values["band"] = band
    print "3: -------------"
    albums = common.get_children(Album, Band, band["id"])
    print "4: -------------"
    albums_dic = entityparser.entities_to_dic_list(albums)
    for album in albums_dic:
        print album["id"]
        tracks = common.get_children(Track, Album, album["id"])
        tracks_dic = entityparser.entities_to_dic_list(tracks)
        album["tracks"] = tracks_dic
    template_values["albums"] = albums_dic


# [START app]
app = webapp2.WSGIApplication([
    ('/bandpage/update', BandPageUpdate),
    ('/bandpage/(\d+)', BandPageDisplay)
], debug=True)
# [END app]
