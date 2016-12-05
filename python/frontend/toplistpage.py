import webapp2
from python.frontend import JINJA_ENVIRONMENT
from python.util import loginhelper, entityparser
from python.api import common
from python.db.databaseKinds import TopList


# [START main_page]
class TopListPageUpdate(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        loginhelper.add_login_values(template_values, self)
        template = JINJA_ENVIRONMENT.get_template('toplistpage/update.html')
        self.response.write(template.render(template_values))


class TopListPageDisplay(webapp2.RequestHandler):
    def get(self, toplist_id):
        template_values = {}
        loginhelper.add_login_values(template_values, self)
        try:
            toplist = common.get_entity_by_id(TopList, int(toplist_id))
            toplist_dic = entityparser.entity_to_dic(toplist)
            template_values["toplist"] = toplist_dic
            template = JINJA_ENVIRONMENT.get_template('toplistpage/display.html')
            self.response.write(template.render(template_values))
        except Exception as e:
            print "toplistpage: ", e
            template = JINJA_ENVIRONMENT.get_template('toplistpage/update.html')
            self.response.write(template.render(template_values))
# [END main_page]


# [START app]
app = webapp2.WSGIApplication([
    ('/toplistpage/update', TopListPageUpdate),
    ('/toplistpage/(\d+)', TopListPageDisplay)
], debug=True)
# [END app]
