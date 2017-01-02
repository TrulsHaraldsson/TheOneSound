import json
import webapp2
from python.db.databaseKinds import Rating, Comment, Album, Track, Account, TrackDescription
from python.api import common
from python.util import entityparser, loginhelper
from google.appengine.ext import ndb


class TrackHandler(webapp2.RequestHandler):
    """
    The TrackHandler listen for HTTP POST and GET requests on the URL /api/tracks.
    """
    def post(self):
        """
        Creates a new track if the POST request delivered sufficient information. The POST request must
        contain the key "name" and "parent_id" else a HTTP 400 error is returned.
        name: Name of the band
        parent_id: id of parent album
        :return: The newly created track as a JSON string
        """
        track_name = self.request.get("name")
        parent_id = self.request.get("parent_id")
        try:
            entity_id = create_track(parent_id, track_name)
            json_obj = entityparser.entity_id_to_json(entity_id)
            self.response.out.write(json_obj)
        except Exception as e:
            self.response.set_status(400)

    def get(self):
        """
        The GET request can have the following url parameters to specify a query. This method can return HTTP 400
        error code.
        :param name: Return only tracks with the given name, if name is absent all tracks will be queried
        :param limit: Upper bound of tracks that will be returned. Default is 10.
        :param offset_: The number of tracks in the query that are initially skipped. Default is 0
        :return: A list of tracks as a JSON string
        """
        tracks = common.get_kinds(Track, self.request.query_string)
        track_list = entityparser.entities_to_dic_list(tracks)
        json_list = json.dumps(track_list)
        self.response.out.write(json_list)


class TrackByIdHandler(webapp2.RequestHandler):
    """
    The TrackByIdHandler listen for HTTP PUT and GET requests on the URL /api/tracks/id, where the id part is
    a unique id for an track.
    """
    def get(self, track_id):
        """
        Returns a track given a unique id. If the id is not associated with any track an HTTP 404 error is returned.
        :param track_id: A unique track id
        :return: An track as a JSON string
        """
        try:
            track = common.get_entity_by_id(int(track_id))
            track_dic = entityparser.entity_to_dic(track)
            self.response.out.write(json.dumps(track_dic))
        except Exception as e:
            self.response.set_status(400)

    # updates a track with the new information
    def put(self, track_id):
        """
        The PUT method is used to update an existing track with the given id. If the track does not exist an HTTP
        404 error is returned.
        :param track_id: Unique id of an track
        :return:
        """
        try:
            update_track(int(track_id), self.request.POST)

        except Exception as e:
            self.response.set_status(400)


def create_track(album_id, track_name):
    """
    Create a new track and then add the track to the given album associated
    with the given id. If the album already has an track with the given name
    nothing will happen.
    :param album_id: Unique ID of the album
    :param track_name: Name of the Track
    """
    if track_name == "":
        raise ValueError("Track must have a name.")
    track = common.has_child_with_name(Track, track_name, Album, album_id)
    if not track:
        parent_key = ndb.Key(Album, int(album_id))
        descr = TrackDescription(description="", youtube_url="")
        track = Track(owner=parent_key, name=track_name, description=descr)
        track.comment = []
        rating = Rating(likes=0, dislikes=0)
        track.rating = rating
        track.put()
        return track.key.id()


def update_track(track_id, post_params):
    '''
    Updates the description, youtube_url, comment, and rating of the track depending on what params are sent.
    '''
    account = common.get_entity_by_id(Account, str(loginhelper.get_user_id()))
    track = common.get_entity_by_id(Track, int(track_id))
    if 'description' in post_params.keys():
        description = post_params['description']
        if description != "":
            track.description.description = description
    if 'youtube_url' in post_params.keys():
        youtube_url = post_params['youtube_url']
        if youtube_url != "":
            track.description.youtube_url = youtube_url
    if 'comment_text'in post_params:
        comment_text = post_params['comment_text']
        if comment_text != "":
            comment = Comment(content=comment_text)
            rating = Rating(likes=0, dislikes=0)
            comment.rating = rating
            track.comment.insert(0, comment)
    if 'rating' in post_params:
        rating = post_params['rating']
        if rating != "":
            track = common.add_rating(Track, track, account, rating)
    track.put()


# [START app]
app = webapp2.WSGIApplication([
    ('/api/tracks', TrackHandler),
    ('/api/tracks/(\d+)', TrackByIdHandler)
], debug=True)
# [END app]
