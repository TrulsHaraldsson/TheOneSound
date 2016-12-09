import webapp2
from python.frontend import JINJA_ENVIRONMENT
from python.util import loginhelper, entityparser, urlhelper, templatehelper
from python.api import common
from python.db.databaseKinds import TopList


class TopListPageCreate(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        loginhelper.add_login_values(template_values, self)
        template = JINJA_ENVIRONMENT.get_template('toplistpage/create.html')
        self.response.write(template.render(template_values))


class TopListPageDisplay(webapp2.RequestHandler):
    def get(self, toplist_id):
        template_values = {}
        loginhelper.add_login_values(template_values, self)
        try:
            toplist = common.get_entity_by_id(TopList, int(toplist_id))
            add_toplist_and_content(template_values, toplist)
            templatehelper.add_rated(template_values, toplist)
            template = JINJA_ENVIRONMENT.get_template('toplistpage/display.html')
            self.response.write(template.render(template_values))
        except Exception as e:
            print "toplistpage: ", e
            template = JINJA_ENVIRONMENT.get_template('toplistpage/create.html')
            self.response.write(template.render(template_values))


def add_toplist_and_content(template_values, toplist):
    toplist_dic = entityparser.entity_to_dic(toplist)
    template_values["toplist"] = toplist_dic
    content_list = []
    for content_key in toplist.content:
        content = content_key.get()
        print content
        content_list.append(entityparser.entity_to_dic(content))
    urlhelper.attach_links("/" + toplist_dic["kind"] + "page/", content_list)
    template_values["content_list"] = content_list


# [START app]
app = webapp2.WSGIApplication([
    ('/toplistpage/create', TopListPageCreate),
    ('/toplistpage/(\d+)', TopListPageDisplay)
], debug=True)
# [END app]
