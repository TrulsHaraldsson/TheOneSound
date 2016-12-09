import loginhelper
from python.api import common
from python.db.databaseKinds import Account


def add_rated(template_values, entity):
    if loginhelper.get_google_user:
        account = common.get_entity_by_id(Account, str(loginhelper.get_user_id()))
        rating = common.have_rated(account, entity)
        if rating:
            template_values["rated"] = rating.value
        else:
            template_values["rated"] = None
    else:
        template_values["rated"] = None
