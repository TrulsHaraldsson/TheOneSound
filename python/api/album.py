import webapp2
import json
from python.databaseKinds import Album, Band, Description
from google.appengine.ext import ndb
from python.util import entityparser


class AlbumHandler(webapp2.RequestHandler):
    def post(self):
        band_id = self.request.get("band_id")
        album_name = self.request.get("album_name")
        album_description = self.request.get("album_description");
        add_album(band_id, album_name, album_description)

    def get(self):
        album_name = self.request.get("album_name")
        albums = get_albums_by_name(album_name)

        albums_as_dict = entityparser.entities_to_dic_list(albums)

        album_as_json = json.dumps(albums_as_dict)

        self.response.out.write(album_as_json)


def add_album(band_id_, album_name_, description_):
    """
    Add an album with the given name to the given band.

    :param band_id_: Unique id for an entity of type Band
    :param album_name_: Name of album
    :param description_: Description for the album
    """

    album = does_album_exist(band_id_, album_name_)
    if not album:
        desc = Description(description=description_)
        desc.put()
        album = Album(parent=ndb.Key(Band, band_id_), name=album_name_, description=desc)
        album.put()


def remove_album(band_id_, album_name_):
    """
    Remove an album with the given name that belongs to the band with
    the given band name.

    :param band_id_: Unique id for an entity of type Band
    :param album_name_: Name of the album
    """

    album = does_album_exist(band_id_, album_name_)
    if album:
        album.key.delete()


def get_album_by_name(band_id_, album_name_):
    """
    Returns the album with the given name for the band with the given band name.

    :param band_id_: Unique id for an entity of type Band
    :param album_name_: Name of the album
    """

    query = Album.query(Album.name == album_name_, Album.parent.key == band_id_)
    album = query.get()
    return album


def get_albums_by_name(album_name_, limit_=10, offset_=0):
    """
    Returns the albums with the given name. By default the maximum number of
    albums returned is 10 with an offset of 0. E.g. if limit_ = 5 and offset_ = 4 the
    query will return at maximum one album, that is there are more than 4 albums with the given name.

    :param album_name_: Name of album
    :param limit_: Maximum number of albums returned
    :param offset_: Offset
    """

    query = Album.query(Album.name == album_name_)
    albums = query.fetch(int(limit_), offset=int(offset_))
    return albums


def does_album_exist(band_id_, album_name_):
    """
    Check if the album with the given name exists and is associated with
    the band. Returns the album object if it exists, else
    None is returned.

    :param band_id_: Unique id for an entity of type Band
    :param album_name_: Name of album
    """

    query = Album.query(Album.name == album_name_, ancestor=ndb.Key(Band, band_id_))
    album = query.get()
    if album:
        return album
    else:
        return None

# [START app]
app = webapp2.WSGIApplication([
    ('/api/album', AlbumHandler)
], debug=True)
# [END app]
