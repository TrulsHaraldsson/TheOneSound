import webapp2
import jinja2
import json
from python.api import band



from python import JINJA_ENVIRONMENT

class BandPageUpdate(webapp2.RequestHandler):
    def get(self):

        template = JINJA_ENVIRONMENT.get_template('bandpage/update.html')
        self.response.write(template.render())

class BandPageDisplay(webapp2.RequestHandler):
    def get(self):

        band_name = self.request.get("band_name")
        #print band.BandByNameHandler.get_band_by_name(band_name)
        try:
            template_values = band.BandByNameHandler.get_band_by_name(band_name).to_dict()
            template = JINJA_ENVIRONMENT.get_template('bandpage/display.html')
            self.response.write(template.render(template_values))
        except Exception as e:
            template = JINJA_ENVIRONMENT.get_template('bandpage/update.html')
            self.response.write(template.render())




# [START app]
app = webapp2.WSGIApplication([
    ('/bandpage/update', BandPageUpdate),
    ('/bandpage', BandPageDisplay)
], debug=True)
# [END app]
