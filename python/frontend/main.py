import webapp2
from python.frontend import JINJA_ENVIRONMENT
from python.util import loginhelper


# [START main_page]
class MainPage(webapp2.RequestHandler):

    def get(self):
        template_values = {}
        loginhelper.add_login_values(template_values, self)
        template = JINJA_ENVIRONMENT.get_template('pages/index.html')
        self.response.write(template.render(template_values))
# [END main_page]


# [START app]
app = webapp2.WSGIApplication([
    ('/', MainPage)
], debug=True)
# [END app]
