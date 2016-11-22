from google.appengine.api import users

def add_login_values(dic, rqhandler):
    user = users.get_current_user()
    if user:
        dic["logged_in"] = True
        dic["user_url"] = users.create_logout_url(rqhandler.request.uri)
        dic["username"] = user.nickname()
    else:
        dic["logged_in"] = False
        dic["user_url"] = users.create_login_url(rqhandler.request.uri)
