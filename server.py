# [START imports]
import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
# [END imports]



# [START DataBase Classes]

    #Put ndb classes here

# [END DataBase Classes]


# [START main_page]
class MainPage(webapp2.RequestHandler):

    def get(self):

        text = "what's up!?"
        template_values = {
            'text': text
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))
# [END main_page]





# [START app]
app = webapp2.WSGIApplication([
    ('/', MainPage)
], debug=True)
# [END app]
