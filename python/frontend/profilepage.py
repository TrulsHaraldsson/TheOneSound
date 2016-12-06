import webapp2

from python.frontend import JINJA_ENVIRONMENT
from python.api import common
from python.db.databaseKinds import Account, TopList
from python.util import entityparser, urlhelper
from python.util import loginhelper


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
            account_ = common.get_entity_by_id(Account, str(user_id))
            account_dic = entityparser.entity_to_dic(account_)
            add_account_and_toplists(template_values, account_dic)
            template = JINJA_ENVIRONMENT.get_template('profilepage/display.html')
            self.response.write(template.render(template_values))
        except Exception as e:
            print(e)
            # Redirect to login / create new Account
            template = JINJA_ENVIRONMENT.get_template('profilepage/update.html')
            self.response.write(template.render(template_values))


def add_account_and_toplists(template_values, account):
    template_values['account'] = account
    toplists = common.get_children(TopList, Account, str(account["id"]))
    toplists_dic = entityparser.entities_to_dic_list(toplists)
    urlhelper.attach_links("/toplistpage/", toplists_dic)
    template_values['toplists'] = toplists_dic


# [START app]
app = webapp2.WSGIApplication([
    ('/profilepage/update', AccountPageUpdate),
    ('/profilepage', AccountPageDisplay)
], debug=True)
# [END app]
