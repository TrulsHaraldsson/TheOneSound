import json

import webapp2

from python.db.databaseKinds import Account
from python.api import common
from python.api.exceptions import NotAuthorized
from python.util import entityparser, loginhelper


class AccountHandler(webapp2.RequestHandler):
    """
    The AccountHandler listen for HTTP POST and GET requests on the URL /api/accounts.
    """
    def get(self):
        """
        The GET request can have the following url parameters to specify a query. This method can return HTTP 400
        error code.
        :param name: Return only Accounts with the given name, if name is absent all Albums will be queried
        :param limit: Upper bound of Accounts that will be returned. Default it 10.
        :param offset_: The number of Accounts in the query that are initially skipped. Default is 0
        :return: A list of Accounts as a JSON string
        """
        accounts = common.get_entities(Account)
        account_list = entityparser.entities_to_dic_list(accounts)

        json_list = json.dumps(account_list)
        self.response.out.write(json_list)

    def post(self):
        """
        Creates a new account if the POST request delivered sufficient information. The POST request must
        contain the following two keys, email and name else a HTTP 400 error is returned.
        :param email: email of the user
        :param name: Name of the user
        :return: The newly created account as a JSON
        """
        account_name = self.request.get("name")
        email = self.request.get("email")
        try:
            entity_id = create_account(account_name, email)
            json_obj = entityparser.entity_id_to_json(entity_id)
            self.response.out.write(json_obj)
        except Exception as e:
            self.response.set_status(400)


class AccountByIdHandler(webapp2.RequestHandler):
    """
    The AccountByIdHandler listen for HTTP POST and GET requests on the URL /api/accounts/id, where the id part is
    a unique id for an account.
    """
    def get(self, account_id):
        try:
            account = common.get_entity_by_id(Account, account_id)
            account_dic = entityparser.entity_to_dic(account)
            self.response.out.write(json.dumps(account_dic))
        except Exception:
            self.response.set_status(400)

    def put(self, account_id):
        try:
            loginhelper.check_logged_in()
            update_account(account_id)
        except NotAuthorized:
            self.response.set_status(401)
        except Exception:
            self.response.set_status(400)


def create_account(account_name, email_):
    '''
    Creates an account for the signed in user.
    Sets its user id as id.
    '''
    if account_name != "" and email_ != "":
        user_id = loginhelper.get_user_id()
        account = Account(id=str(user_id), name=account_name, email=email_, ratings=[])
        account.put()
        return account.key.id()
    else:
        raise ValueError("check so all requirements are met.")


def update_account(account_id, account_name, email_):
    '''
    Updates the email and/or the username for the logged in account.
    '''
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
