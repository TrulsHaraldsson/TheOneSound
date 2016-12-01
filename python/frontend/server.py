# [START imports]
import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2
from python.frontend import JINJA_ENVIRONMENT
from python.util import loginhelper


# [START main_page]
class MainPage(webapp2.RequestHandler):

    def get(self):
        template_values = {}
        loginhelper.add_login_values(template_values, self)
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))
# [END main_page]



#[START TestPage]
class TestPage(webapp2.RequestHandler):
    def get(self):
        template_value = {
            'text': "This is a text specified in the server script",
            'integer': 1337,
            'float': 2.000001,
            'listWithText':["This","is","a","list","containing","text"]
        }
        
        loginhelper.add_login_values(template_values, self)
        template = JINJA_ENVIRONMENT.get_template('testpage.html')
        self.response.write(template.render(template_value))
#[END TestPage]


# [START app]
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/testpage', TestPage)
], debug=True)
# [END app]
