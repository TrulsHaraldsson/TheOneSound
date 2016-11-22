import webapp2
import jinja2
import json
from python.api import band
from python.util import loginhelper



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
        band_name = self.request.get("band_name")
        try:
            template_values["band"] = band.get_band_by_name(band_name).to_dict()
            template = JINJA_ENVIRONMENT.get_template('bandpage/display.html')
            self.response.write(template.render(template_values))
        except Exception as e:
            template = JINJA_ENVIRONMENT.get_template('bandpage/update.html')
            self.response.write(template.render(template_values))




# [START app]
app = webapp2.WSGIApplication([
    ('/bandpage/update', BandPageUpdate),
    ('/bandpage', BandPageDisplay)
], debug=True)
# [END app]
