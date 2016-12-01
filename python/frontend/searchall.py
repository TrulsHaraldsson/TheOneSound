import webapp2
from python.db.databaseKinds import Band, Album, Track
from python.frontend import JINJA_ENVIRONMENT, bandpage
from python.util import loginhelper, entityparser, urlhelper
from python.api import common


# [START main_page]
class SearchHandler(webapp2.RequestHandler):
    def get(self):
        query_string = self.request.query_string
        template_values = {}
        loginhelper.add_login_values(template_values, self)
        bands = common.get_kinds(Band, query_string)
        albums = common.get_kinds(Album, query_string)
        tracks = common.get_kinds(Track, query_string)
        numberOfHits = len(bands) + len(albums) + len(tracks)
        if numberOfHits == 0:
            # should redirect to page when asked to create new entity
            template = JINJA_ENVIRONMENT.get_template('multiplehitspage.html')
        elif numberOfHits == 1:
            if bands:
                band = entityparser.entities_to_dic_list(bands)[0]
                bandpage.add_band_and_decendants(template_values, band)
                template = JINJA_ENVIRONMENT.get_template('bandpage/display.html')
            if albums:
                album = entityparser.entities_to_dic_list(albums)[0]
                template_values["album"] = album  # TODO: fix so it does like for band, gets all tracks too.
                template = JINJA_ENVIRONMENT.get_template('albumpage/display.html')
            if tracks:
                track = entityparser.entities_to_dic_list(tracks)[0]
                template_values["track"] = track
                template = JINJA_ENVIRONMENT.get_template('trackpage/display.html')
        else:
            if bands:
                template_values["bands"] = entityparser.entities_to_dic_list(bands)
                urlhelper.attach_links("/bandpage/", template_values["bands"])
            if albums:
                template_values["albums"] = entityparser.entities_to_dic_list(albums)
                urlhelper.attach_links("/albumpage/", template_values["albums"])
            if tracks:
                template_values["tracks"] = entityparser.entities_to_dic_list(tracks)
                urlhelper.attach_links("/trackpage/", template_values["tracks"])
            template = JINJA_ENVIRONMENT.get_template('multiplehitspage.html')
        self.response.write(template.render(template_values))
# [END main_page]


# [START app]
app = webapp2.WSGIApplication([
    ('/searchall', SearchHandler)
], debug=True)
# [END app]
