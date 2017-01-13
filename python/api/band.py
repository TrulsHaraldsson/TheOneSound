import json
import webapp2

from python.db.databaseKinds import Rating, BandDescription, Comment, Band, Account
from python.api import common
from python.api.exceptions import BadRequest, EntityNotFound, NotAuthorized
from python.util import entityparser, loginhelper


class BandHandler(webapp2.RequestHandler):
    """
    The BandHandler listen for HTTP POST and GET requests on the URL /api/bands.
    """
    def post(self):
        """
        Creates a new band if the POST request delivered sufficient information. The POST request must
        contain the key "name" else a HTTP 400 error is returned.
        :param name: Name of the band
        :return: The newly created band as a JSON string
        """
        band_name = self.request.get("name")
        try:
            loginhelper.check_logged_in()
            entity_id = create_band(band_name)
            json_obj = entityparser.entity_id_to_json(entity_id)
            self.response.out.write(json_obj)
        except BadRequest:
            self.response.set_status(400)
        except NotAuthorized:
            self.response.set_status(401)

    def get(self):
        """
        The GET request can have the following url parameters to specify a query. This method can return HTTP 400
        error code.
        :param name: Return only bands with the given name, if name is absent all Bands will be queried
        :param limit: Upper bound of bands that will be returned. Default is 10.
        :param offset_: The number of bands in the query that are initially skipped. Default is 0
        :return: A list of bands as a JSON string
        """
        try:
            bands = common.get_kinds(Band, self.request.query_string)
            band_list = entityparser.entities_to_dic_list(bands)
            json_list = json.dumps(band_list)
            self.response.out.write(json_list)
        except BadRequest as e:
            self.response.set_status(400)


class BandByIdHandler(webapp2.RequestHandler):
    """
    The BandByIdHandler listen for HTTP PUT and GET requests on the URL /api/bands/id, where the id part is
    a unique id for an band.
    """
    def get(self, band_id):
        """
        Returns an band given a unique id. If the id is not associated with any band an HTTP 404 error is returned.
        :param band_id: A unique band id
        :return: An band as a JSON string
        """
        try:
            band = common.get_entity_by_id(Band, int(band_id))
            band_dic = entityparser.entity_to_dic(band)
            self.response.out.write(json.dumps(band_dic))
        except EntityNotFound:
            self.response.set_status(404)

    # updates a band with the new information
    def put(self, band_id):
        """
        The PUT method is used to update an existing Band with the given id. If the band does not exist an HTTP
        404 error is returned.
        :param band_id: Unique id of an band
        :return: a band as a json string
        """
        try:
            loginhelper.check_logged_in()
            update_band(int(band_id), self.request.POST)
        except BadRequest:
            self.response.set_status(400)
        except EntityNotFound:
            self.response.set_status(404)
        except NotAuthorized:
            self.response.set_status(401)


def update_band(band_id, post_params):
    '''
    Updates the description, genres, members, picture_url, comment_text and rating for the chosen band.
    '''
    user_id = loginhelper.get_user_id()
    band = common.get_entity_by_id(Band, int(band_id))
    if 'description' in post_params.keys():
        description = post_params['description']
        band.description.description = description
    if 'genre' in post_params.keys():
        genre = post_params['genre']
        band.description.genres.append(genre)
    if 'member' in post_params.keys():
        member = post_params['member']
        band.description.members.append(member)
    if 'picture_url' in post_params.keys():
        picture_url = post_params['picture_url']
        band.description.picture_url = picture_url
    if 'comment_text' in post_params.keys():
        comment_text = post_params['comment_text']
        parent_key = common.create_key(Account, user_id)
        comment = Comment(owner=parent_key, content=comment_text)
        rating = Rating(likes=0, dislikes=0)
        comment.rating = rating
        band.comment.insert(0, comment)
    if 'rating' in post_params.keys():
        rating = post_params['rating']
        account = common.get_entity_by_id(Account, str(user_id))
        band = common.add_rating(Band, band, account, rating)
    band.put()


def create_band(band_name):
    '''
    Creates a new band with the specified name. Sets all the default values.
    If no name is set, it raise an error.
    returns the id for the band.
    '''
    if band_name == "":
        raise BadRequest("Band must have a name.")

    band = Band(name=band_name, comment=[])
    desc = BandDescription(description="", members=[], genres=[])
    band.description = desc
    rating = Rating(likes=0, dislikes=0)
    band.rating = rating
    band_key = band.put()
    picture_url = "https://storage.googleapis.com/theonesound-148310.appspot.com/bands/"+str(band_key.id())
    band.description.picture_url = picture_url
    band.put()
    return band_key.id()


# [START app]
app = webapp2.WSGIApplication([
    ('/api/bands', BandHandler),
    ('/api/bands/(\d+)', BandByIdHandler)
], debug=True)
# [END app]
