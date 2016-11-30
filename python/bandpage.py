import webapp2
from python.databaseKinds import Band, Album, Track
from python.util import loginhelper
from python.util import entityparser
from python.api import common
from python import JINJA_ENVIRONMENT


class BandPageUpdate(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        loginhelper.add_login_values(template_values, self)
        template = JINJA_ENVIRONMENT.get_template('bandpage/update.html')
        self.response.write(template.render())


class BandPageDisplay(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        loginhelper.add_login_values(template_values, self)
        band_name = self.request.get("name")
        try:
            bands = common.get_entities_by_name(Band, band_name)
            bands_dic = entityparser.entities_to_dic_list(bands)
            if len(bands_dic) > 1:
                pass
                # redirect to page where you can choose which one you want
            else:
                # 1: fetch all albums belonging to band
                #   2: fetch all tracks belonging to album
                template_values["band"] = bands_dic[0]
                print bands_dic[0]["id"]
                albums = common.get_children(Album, Band, bands_dic[0]["id"])
                albums_dic = entityparser.entities_to_dic_list(albums)
                for album in albums_dic:
                    print album["id"]
                    tracks = common.get_children(Track, Album, album["id"])
                    tracks_dic = entityparser.entities_to_dic_list(tracks)
                    album["tracks"] = tracks_dic
                template_values["albums"] = albums_dic
                template = JINJA_ENVIRONMENT.get_template('bandpage/display.html')
                self.response.write(template.render(template_values))
        except Exception as e:
            print "Bandpage: ", e
            template = JINJA_ENVIRONMENT.get_template('bandpage/update.html')
            self.response.write(template.render(template_values))


# [START app]
app = webapp2.WSGIApplication([
    ('/bandpage/update', BandPageUpdate),
    ('/bandpage', BandPageDisplay)
], debug=True)
# [END app]
