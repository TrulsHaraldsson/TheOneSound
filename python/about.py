
import webapp2
import jinja2

from python import JINJA_ENVIRONMENT

class About(webapp2.RequestHandler):
    def get(self):

        template = JINJA_ENVIRONMENT.get_template('about.html')
        self.response.write(template.render())

# [START app]
app = webapp2.WSGIApplication([
    ('/about', About)
], debug=True)
# [END app]
