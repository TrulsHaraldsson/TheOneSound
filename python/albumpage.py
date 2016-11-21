import webapp2

from python import JINJA_ENVIRONMENT

class AlbumPageUpdate(webapp2.RequestHandler):
    def get(self):

        template = JINJA_ENVIRONMENT.get_template('albumpage/update.html')
        self.response.write(template.render())

class AlbumPageDisplay(webapp2.RequestHandler):
    def get(self):

        template_values = {}

        template = JINJA_ENVIRONMENT.get_template('albumpage/display.html')
        self.response.out.write(template.render(template_values))

# [START app]
app = webapp2.WSGIApplication([
    ('/albumpage/update', AlbumPageUpdate),
    ('/albumpage/display', AlbumPageDisplay)
], debug=True)
# [END app]
