import webapp2
import jinja2
import json

from python.databaseKinds import Account
from python.util import loginhelper
from python.util import entityparser
from python.api import account, common



from python import JINJA_ENVIRONMENT

class AccountPageUpdate(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        loginhelper.add_login_values(template_values, self)
        template = JINJA_ENVIRONMENT.get_template('profilepage/update.html')
        self.response.write(template.render())

class AccountPageDisplay(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        loginhelper.add_login_values(template_values, self)

        try:
            user_id = loginhelper.get_user_id()
            account_ = common.get_entity_by_id(Account, user_id)
            account_dic = entityparser.entity_to_dic(account_)
            template_values['account'] = account_dic
            template = JINJA_ENVIRONMENT.get_template('profilepage/display.html')
            self.response.write(template.render(template_values))
            #redirect to profilepage

        except Exception as e:
            print(e)
            #Redirect to login / create new Account
            template = JINJA_ENVIRONMENT.get_template('profilepage/update.html')
            self.response.write(template.render(template_values))




# [START app]
app = webapp2.WSGIApplication([
    ('/profilepage/update', AccountPageUpdate),
    ('/profilepage', AccountPageDisplay)
], debug=True)
# [END app]
