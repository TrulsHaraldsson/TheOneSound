import webapp2

from python import JINJA_ENVIRONMENT
from python.util import loginhelper


class AlbumPageUpdate(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        loginhelper.add_login_values(template_values, self)
        template = JINJA_ENVIRONMENT.get_template('albumpage/update.html')
        self.response.write(template.render(template_values))


class AlbumPageDisplay(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        loginhelper.add_login_values(template_values, self)
        template = JINJA_ENVIRONMENT.get_template('albumpage/display.html')
        self.response.out.write(template.render(template_values))

# [START app]
app = webapp2.WSGIApplication([
    ('/albumpage/update', AlbumPageUpdate),
    ('/albumpage/display', AlbumPageDisplay)
], debug=True)
# [END app]
