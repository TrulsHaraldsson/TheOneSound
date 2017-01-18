import loginhelper
import entityparser
from python.api import common
from python.db.databaseKinds import Account,  TopList


def add_rated(template_values, entity):
    if loginhelper.get_google_user():
        account = common.get_entity_by_id(Account, str(loginhelper.get_user_id()))
        rating = common.have_rated(account, entity)
        if rating:
            template_values["rated"] = rating.value
        else:
            template_values["rated"] = None
    else:
        template_values["rated"] = None


def add_toplists(template_values, kind):
    user = loginhelper.get_google_user()
    if user:
        toplists = common.get_children(TopList, Account, user.user_id())
        toplists = entityparser.entities_to_dic_list(toplists)
        template_list = []
        for toplist in toplists:
            if toplist["kind"] == kind:
                template_list.append(toplist)
        if len(template_list) != 0:
            template_values["toplists"] = template_list
