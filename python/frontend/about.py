import webapp2
from python.frontend import JINJA_ENVIRONMENT
from python.util import loginhelper


class About(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        loginhelper.add_login_values(template_values, self)
        template = JINJA_ENVIRONMENT.get_template('pages/about.html')
        self.response.write(template.render(template_values))

# [START app]
app = webapp2.WSGIApplication([
    ('/about', About)
], debug=True)
# [END app]
