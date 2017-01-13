from google.appengine.api import users
from python.api import exceptions


def add_login_values(dic, rqhandler):
    user = users.get_current_user()
    user_dic = {}
    if user:
        user_dic["logged_in"] = True
        user_dic["url"] = users.create_logout_url(rqhandler.request.uri)
        user_dic["name"] = user.nickname()
        user_dic["id"] = user.user_id()
    else:
        user_dic["logged_in"] = False
        user_dic["url"] = users.create_login_url("/profiles")
    dic["user"] = user_dic


def get_google_user():
    return users.get_current_user()


def get_user_id():
    return get_google_user().user_id()


def check_logged_in():
    user = users.get_current_user()
    if user:
        pass
    else:
        raise exceptions.NotAuthorized("User is not logged in")
