import webapp2

from python.frontend import JINJA_ENVIRONMENT
from python.api import common
from python.db.databaseKinds import Track
from python.util import entityparser, templatehelper
from python.util import loginhelper


class TracksUpdate(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        loginhelper.add_login_values(template_values, self)
        template = JINJA_ENVIRONMENT.get_template('pages/tracks/update.html')
        self.response.write(template.render(template_values))


class TracksDisplay(webapp2.RequestHandler):
    def get(self, track_id):
        template_values = {}
        loginhelper.add_login_values(template_values, self)
        try:
            track = common.get_entity_by_id(Track, int(track_id))
            track_dic = entityparser.entity_to_dic(track)
            template_values["track"] = track_dic
            templatehelper.add_rated(template_values, track)
            template = JINJA_ENVIRONMENT.get_template('pages/tracks/display.html')
            self.response.write(template.render(template_values))
        except Exception as e:
            print(e)
            template = JINJA_ENVIRONMENT.get_template('pages/tracks/update.html')
            self.response.write(template.render(template_values))


# [START app]
app = webapp2.WSGIApplication([
    ('/tracks/update', TracksUpdate),
    ('/tracks/(\d+)', TracksDisplay)
], debug=True)
# [END app]
