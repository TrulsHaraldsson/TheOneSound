import json

import webapp2
from google.appengine.ext import ndb

from python.db.databaseKinds import Album, Band, Description, Account, Comment, Rating
from python.api import common
from python.api.exceptions import BadRequest, EntityNotFound
from python.util import entityparser, loginhelper


class AlbumHandler(webapp2.RequestHandler):
    def post(self):
        try:
            band_id = self.request.get("parent_id")
            entity_id = create_album(band_id, self.request.POST)
            json_obj = entityparser.entity_id_to_json(entity_id)
            self.response.out.write(json_obj)
        except BadRequest:
            self.response.set_status(400)

    def get(self):
        try:
            albums = common.get_kinds(Album, self.request.query_string)
            albums_as_dict = entityparser.entities_to_dic_list(albums)
            albums_as_json = json.dumps(albums_as_dict)
            self.response.out.write(albums_as_json)
        except BadRequest:
            self.response.set_status(400)


class AlbumByIdHandler(webapp2.RequestHandler):
    def get(self, album_id):
        try:
            album = common.get_entity_by_id(Album, int(album_id))
            album_as_dict = entityparser.entity_to_dic(album)
            album_as_json = json.dumps(album_as_dict)
            self.response.out.write(album_as_json)
        except EntityNotFound:
            self.response.set_status(404)

    def put(self, album_id):
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

        if 'description' in post_params.keys():
            desc = Description(description=post_params['description'])

        album = Album(owner=ndb.Key(Band, int(band_id)), name=post_params['name'], description=desc)
        rating = Rating(likes=0, dislikes=0)
        album.rating = rating
        album.put()
        return album.key.id()


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
            description = Description(description=str(post_params['description']))
            album.description = description
        else:
            raise BadRequest("description must be none empty")

    if 'rating' in post_params.keys():
        rating = post_params['rating']
        if rating == "1":
            album.rating.likes += 1
        elif rating == "0":
            album.rating.dislikes += 1

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
