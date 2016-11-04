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
        user = users.get_current_user()
        if user:
            url_linktext = 'logout'
            url = users.create_logout_url('/')
            text = "what's up " + user.nickname() + "!?"
        else:
            url_linktext = 'login'
            url = users.create_login_url('/')
            text = "what's up anonymous!?"

        template_values = {
            'url': url,
            'url_linktext': url_linktext,
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
