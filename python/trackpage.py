import webapp2

from python import JINJA_ENVIRONMENT
from python.api import common
from python.db.databaseKinds import Track
from python.util import entityparser
from python.util import loginhelper


class TrackPageUpdate(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        loginhelper.add_login_values(template_values, self)
        template = JINJA_ENVIRONMENT.get_template('trackpage/update.html')
        self.response.write(template.render())


class TrackPageDisplay(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        loginhelper.add_login_values(template_values, self)
        track_name = self.request.get("name")
        try:
            tracks = common.get_entities_by_name(Track, track_name)
            tracks_dic = entityparser.entities_to_dic_list(tracks)
            if len(tracks_dic) > 1:
                pass
                #redirect to page where you can choose which one you want
            else:
                template_values["track"] = tracks_dic[0]
                template = JINJA_ENVIRONMENT.get_template('trackpage/display.html')
                self.response.write(template.render(template_values))
        except Exception as e:
            print(e)
            template = JINJA_ENVIRONMENT.get_template('trackpage/update.html')
            self.response.write(template.render(template_values))


# [START app]
app = webapp2.WSGIApplication([
    ('/trackpage/update', TrackPageUpdate),
    ('/trackpage', TrackPageDisplay)
], debug=True)
# [END app]
