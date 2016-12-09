import json

import webapp2

from python.db.databaseKinds import Account
from python.api import common
from python.util import entityparser, loginhelper


class AccountHandler(webapp2.RequestHandler):
    def get(self):
        limit = self.request.get("limit")
        accounts = common.get_entities(Account, limit)
        account_list = entityparser.entities_to_dic_list(accounts)

        json_list = json.dumps(account_list)
        self.response.out.write(json_list)

    def post(self):
        account_name = self.request.get("name")
        email = self.request.get("email")
        try:
            entity_id = create_account(account_name, email)
            json_obj = entityparser.entity_id_to_json(entity_id)
            self.response.out.write(json_obj)
        except Exception as e:
            print e
            self.response.set_status(400)


class AccountByIdHandler(webapp2.RequestHandler):
    def get(self, account_id):
        try:
            account = common.get_entity_by_id(Account, account_id)
            account_dic = entityparser.entity_to_dic(account)
            self.response.out.write(json.dumps(account_dic))
        except Exception as e:
            print e
            self.response.set_status(400)

    def put(self, account_id):
        try:

            update_account(account_id)
        except Exception as e:
            print e
            raise


def create_account(account_name, email_):
    print "in create account"
    if account_name != "" and email_ != "":
        user_id = loginhelper.get_user_id()
        account = Account(id=str(user_id), name=account_name, email=email_, ratings=[])
        account.put()
        return account.key.id()
    else:
        raise ValueError("check so all requirements are met.")


def update_account(account_id, account_name, email_):
    account = common.get_entity_by_id(Account, account_id)
    if email_ != "":
        account.email = email_
    if account_name != "":
        account.name = account_name
    return None


# [START app]
app = webapp2.WSGIApplication([
    ('/api/accounts', AccountHandler),
    ('/api/accounts/(\w+)', AccountByIdHandler)
], debug=True)
# [END app]
