import webapp2
import jinja2
import json
from python.databaseKinds import Band
from python.util import loginhelper
from python.util import entityparser
from python.api import common
from python.api import band



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
                #redirect to page where you can choose which one you want
            else:
                template_values["band"] = bands_dic[0]
                template = JINJA_ENVIRONMENT.get_template('bandpage/display.html')
                self.response.write(template.render(template_values))
        except Exception as e:
            print(e)
            template = JINJA_ENVIRONMENT.get_template('bandpage/update.html')
            self.response.write(template.render(template_values))




# [START app]
app = webapp2.WSGIApplication([
    ('/bandpage/update', BandPageUpdate),
    ('/bandpage', BandPageDisplay)
], debug=True)
# [END app]
