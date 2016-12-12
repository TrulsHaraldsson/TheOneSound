import webapp2

from python.frontend import JINJA_ENVIRONMENT
from python.api import common, account
from python.db.databaseKinds import Account, TopList
from python.util import entityparser, urlhelper
from python.util import loginhelper


class AccountsUpdate(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        loginhelper.add_login_values(template_values, self)
        template = JINJA_ENVIRONMENT.get_template('pages/profiles/update.html')
        self.response.write(template.render())


class AccountsDisplay(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        loginhelper.add_login_values(template_values, self)
        try:
            user = loginhelper.get_google_user()
            user_id = user.user_id()
            try:
                account_ = common.get_entity_by_id(Account, str(user_id))
            except Exception as e:
                account.create_account(user.nickname(), user.email())
                account_ = common.get_entity_by_id(Account, str(user_id))
            account_dic = entityparser.entity_to_dic(account_)
            add_account_and_toplists(template_values, account_dic)
            template = JINJA_ENVIRONMENT.get_template('pages/profiles/display.html')
            self.response.write(template.render(template_values))
        except Exception as e:
            print(e)
            # Redirect to login / create new Account
            template = JINJA_ENVIRONMENT.get_template('pages/profiles/update.html')
            self.response.write(template.render(template_values))


def add_account_and_toplists(template_values, account):
    template_values['account'] = account
    toplists = common.get_children(TopList, Account, str(account["id"]))
    toplists_dic = entityparser.entities_to_dic_list(toplists)
    urlhelper.attach_links("/toplists/", toplists_dic)
    template_values['toplists'] = toplists_dic


# [START app]
app = webapp2.WSGIApplication([
    ('/profiles/update', AccountsUpdate),
    ('/profiles', AccountsDisplay)
], debug=True)
# [END app]
