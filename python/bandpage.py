import webapp2
import jinja2

from python import JINJA_ENVIRONMENT

class BandPageUpdate(webapp2.RequestHandler):
    def get(self):

        template = JINJA_ENVIRONMENT.get_template('bandpage/update.html')
        self.response.write(template.render())

class BandPageDisplay(webapp2.RequestHandler):
    def get(self):
        band_name = self.request.get("band_name")
        template_values = {
            'band_name': band_name
        }
        template = JINJA_ENVIRONMENT.get_template('bandpage/display.html')
        self.response.write(template.render())

# [START app]
app = webapp2.WSGIApplication([
    ('/bandpage/update', BandPageUpdate),
    ('/bandpage', BandPageDisplay)
], debug=True)
# [END app]
