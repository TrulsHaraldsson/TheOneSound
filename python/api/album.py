import webapp2
import json
from python.databaseKinds import Album, Band, Description
from google.appengine.ext import ndb
from python.api import common
from python.util import entityparser


class AlbumHandler(webapp2.RequestHandler):
    def post(self):
        band_id = self.request.get("parent_id")
        album_name = self.request.get("name")
        album_description = self.request.get("description")
        add_album(band_id, album_name, album_description)

    def get(self):
        albums = common.get_kinds(Album, self.request.query_string)
        albums_as_dict = entityparser.entities_to_dic_list(albums)
        albums_as_json = json.dumps(albums_as_dict)
        self.response.out.write(albums_as_json)


class AlbumByIdHandler(webapp2.RequestHandler):
    def get(self, album_id):
        album = common.get_entity_by_id(Album, int(album_id))
        album_as_dict = entityparser.entity_to_dic(album)
        album_as_json = json.dumps(album_as_dict)
        self.response.out.write(album_as_json)

    def put(self, album_id):
        raise NotImplementedError

    def delete(self, album_id):
        raise NotImplementedError


def add_album(band_id, album_name, description):
    """
    Create and add an album with the given name to the given band
    specified by the id. Will not add the album if the band already has
    an album with the given name.

    :param band_id: Unique id for an entity of type Band
    :param album_name: Name of album
    :param description: Description for the album
    """

    album = common.has_child_with_name(Album, album_name, Band, band_id)
    if not album:
        desc = Description(description=description)
        desc.put()
        album = Album(parent=ndb.Key(Band, int(band_id)), name=album_name, description=desc)
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
