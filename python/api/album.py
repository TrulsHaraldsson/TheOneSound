import json

import webapp2
from google.appengine.ext import ndb

from python.db.databaseKinds import Album, Band, AlbumDescription, Account, Comment, Rating
from python.api import common
from python.api.exceptions import BadRequest, EntityNotFound
from python.util import entityparser, loginhelper


class AlbumHandler(webapp2.RequestHandler):
    """
    The AlbumHandler listen for HTTP POST and GET requests on the URL /api/albums.
    """
    def post(self):
        """
        Creates a new album if the POST request delivered sufficient information. The POST request must
        contain the following two keys, parent_id and name else a HTTP 400 error is returned.
        parent_id: A unique id for the band that owns this album
        name: Name of the album
        :return: The newly created album as a JSON string
        """
        try:
            band_id = self.request.get("parent_id")
            entity_id = create_album(band_id, self.request.POST)
            json_obj = entityparser.entity_id_to_json(entity_id)
            self.response.out.write(json_obj)
        except BadRequest:
            self.response.set_status(400)

    def get(self):
        """
        The GET request can have the following url parameters to specify a query. This method can return HTTP 400
        error code.
        :param name: Return only albums with the given name, if name is absent all Albums will be queried
        :param limit: Upper bound of Albums that will be returned. Default it 10.
        :param offset_: The number of Albums in the query that are initially skipped. Default is 0
        :return: A list of Albums as a JSON string
        """
        try:
            albums = common.get_kinds(Album, self.request.query_string)
            albums_as_dict_list = entityparser.entities_to_dic_list(albums)
            albums_as_json = json.dumps(albums_as_dict_list)
            self.response.out.write(albums_as_json)
        except BadRequest:
            self.response.set_status(400)


class AlbumByIdHandler(webapp2.RequestHandler):
    """
    The AlbumByIdHandler listen for HTTP POST and GET requests on the URL /api/albums/id, where the id part is
    a unique id for an album.
    """
    def get(self, album_id):
        """
        Returns an album given a unique id. If the id is not associated with any album an HTTP 404 error is returned.
        :param album_id: A unique album id
        :return: An Album as a JSON string
        """
        try:
            album = common.get_entity_by_id(Album, int(album_id))
            album_as_dict = entityparser.entity_to_dic(album)
            album_as_json = json.dumps(album_as_dict)
            self.response.out.write(album_as_json)
        except EntityNotFound:
            self.response.set_status(404)

    def put(self, album_id):
        """
        The PUT method is used to update an existing Album with the given id. If the album does not exist an HTTP
        404 error is returned.
        :param album_id: Unique id of an Album
        :return:
        """
        try:
            update_album(album_id, self.request.POST)
        except BadRequest:
            self.response.set_status(400)
        except EntityNotFound:
            self.response.set_status(404)

    def delete(self, album_id):
        raise NotImplementedError


def create_album(band_id, post_params):
    """
    Create and album and add it the specific band given by the band ID.
    Will not add the album if the band already has an album with the given album name.
    :param band_id: Unique id for an entity of type Album
    :param post_params: A dictionary with data containing information about album name and description
    """

    user_id = loginhelper.get_user_id()  # TODO: Check if user_id exists in our database in order for them to submit

    if 'name' not in post_params.keys() or post_params['name'] == "":
        raise BadRequest('Album must have name')

    album_exists = common.has_child_with_name(Album, post_params['name'], Band, band_id)
    if not album_exists:

        desc = AlbumDescription(description="", picture_url="")

        album = Album(owner=ndb.Key(Band, int(band_id)), name=post_params['name'], description=desc)
        rating = Rating(likes=0, dislikes=0)
        album.rating = rating
        album_key = album.put()
        picture_url = "https://storage.googleapis.com/theonesound-148310.appspot.com/albums/"+str(album_key.id())
        album.description.picture_url = picture_url
        album.put()
        return album_key.id()


def update_album(album_id, post_params):
    """
    Update the Album with the given ID. The attributes that can be update for an Album
    is the description, rating and adding a comment.
    :param album_id: Unique ID for an entity of type Album
    :param post_params: A dictionary with the new value that will update or be appended to the Album
    """
    album = common.get_entity_by_id(Album, int(album_id))
    user_id = loginhelper.get_user_id()

    if 'comment_text' in post_params.keys():
        parent_key = ndb.Key(Account, user_id)
        if post_params['comment_text'] != "":
            comment = Comment(owner=parent_key, content=post_params['comment_text'])
            album.comment.insert(0, comment)
        else:
            raise BadRequest("comment must be none empty")

    if 'description' in post_params.keys():
        if post_params['description'] != "":
            description = post_params['description']
            album.description.description = description
        else:
            raise BadRequest("description must be none empty")

    if 'picture_url' in post_params.keys():
        if post_params['picture_url'] != "":
            picture_url = post_params['picture_url']
            album.description.picture_url = picture_url
        else:
            raise BadRequest("picture url must be none empty")

    if 'rating' in post_params.keys():
        rating = post_params['rating']
        account = common.get_entity_by_id(Account, str(user_id))
        album = common.add_rating(Band, album, account, rating)

    album.put()


def remove_album(band_id, album_name):
    """
    Remove an album with the given name that belongs to the band with
    the given band name.

    :param band_id: Unique id for an entity of type Band
    :param album_name: Name of the album
    """

    album = common.has_child_with_name(Album, album_name, Band, band_id)
    if album:
        album.key.delete()


# [START app]
app = webapp2.WSGIApplication([
    ('/api/albums', AlbumHandler),
    ('/api/albums/(\d+)', AlbumByIdHandler)
], debug=True)
# [END app]
