import webapp2
import json
from python.databaseKinds import Account
from google.appengine.ext import ndb
from python.util import loginhelper
from python.util import entityparser

class AccountHandler(webapp2.RequestHandler):
    def get(self):
        limit = self.request.get("limit")
        accounts = get_multiple_accounts(limit)
        account_list = entityparser.entities_to_dic_list(accounts)

        json_list = json.dumps(account_list)
        self.response.out.write(json_list)

    def post(self):
        account_name = self.request.get("account_name")
        email = self.request.get("email")
        try:
            create_new_account(account_name, email)
        except Exception as e:
            raise

class AccountByIdHandler(webapp2.RequestHandler):
    def get(self, account_id):
        try:
            account = get_account_by_id(account_id)
            account_dic = entityparser.entity_to_dic(account)
            self.response.out.write(json.dumps(account_dic))
        except Exception as e:
            self.response.set_status(400)

    def put(self, account_id):
        try:

            update_account(account_id)
        except Exception as e:
            raise


def get_multiple_accounts(limit):
    return entityparser.get_multiple_entities(Account, limit)

def create_new_account(account_name, email_):
    if account_name != "" and email_ != "" :
        user_id = loginhelper.get_google_user().user_id()
        account = Account(id=user_id, name=account_name, email=email_)
        account.put()
    else:
        raise ValueError("check so all requirements are met.")

def get_account_by_id(account_id):
    return entityparser.get_entity_by_id(Account, account_id)

#
def update_account(account_id, account_name, email_):
    account = entityparser.get_entity_by_id(Account, account_id)
    if email_ != "":
        account.email = email_
    if account_name != "":
        account.name = account_name
    return None

# [START app]
app = webapp2.WSGIApplication([
    ('/api/account', AccountHandler),
    ('/api/account/(\w+)', AccountByIdHandler)
], debug=True)
# [END app]
