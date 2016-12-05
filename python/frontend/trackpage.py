import webapp2

from python.frontend import JINJA_ENVIRONMENT
from python.api import common
from python.db.databaseKinds import Track
from python.util import entityparser
from python.util import loginhelper


class TrackPageUpdate(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        loginhelper.add_login_values(template_values, self)
        template = JINJA_ENVIRONMENT.get_template('trackpage/update.html')
        self.response.write(template.render(template_values))


class TrackPageDisplay(webapp2.RequestHandler):
    def get(self, track_id):
        template_values = {}
        loginhelper.add_login_values(template_values, self)
        try:
            track = common.get_entity_by_id(Track, track_id)
            track_dic = entityparser.entity_to_dic(track)
            template_values["track"] = track_dic
            template = JINJA_ENVIRONMENT.get_template('trackpage/display.html')
            self.response.write(template.render(template_values))
        except Exception as e:
            print(e)
            template = JINJA_ENVIRONMENT.get_template('trackpage/update.html')
            self.response.write(template.render(template_values))


# [START app]
app = webapp2.WSGIApplication([
    ('/trackpage/update', TrackPageUpdate),
    ('/trackpage/(\d+)', TrackPageDisplay)
], debug=True)
# [END app]
