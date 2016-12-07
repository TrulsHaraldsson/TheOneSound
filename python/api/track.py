import json
import webapp2
from python.db.databaseKinds import Rating, Comment, Album, Track
from python.api import common
from python.util import entityparser
from google.appengine.ext import ndb


class TrackHandler(webapp2.RequestHandler):
    # creates one new track
    # maybe make so multiple can be made ?
    def post(self):
        track_name = self.request.get("name")
        parent_id = self.request.get("parent_id")
        try:
            create_track(parent_id, track_name)
        except Exception as e:
            print e
            self.response.set_status(400)

    # request
    # gives list of matching tracks
    def get(self):
        tracks = common.get_kinds(Track, self.request.query_string)
        track_list = entityparser.entities_to_dic_list(tracks)
        json_list = json.dumps(track_list)
        self.response.out.write(json_list)


class TrackByIdHandler(webapp2.RequestHandler):
    def get(self, track_id):
        try:
            track = common.get_entity_by_id(int(track_id))
            track_dic = entityparser.entity_to_dic(track)
            self.response.out.write(json.dumps(track_dic))
        except Exception as e:
            print e
            self.response.set_status(400)

    # updates a track with the new information
    def put(self, track_id):
        try:
            comment_text = self.request.get("comment_text")
            update_track(comment_text, int(track_id))

        except Exception as e:
            print e
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
        track = Track(owner=parent_key, name=track_name)
        track.comment = []
        rating = Rating(likes=0, dislikes=0)
        track.rating = rating
        track.put()


def update_track(comment_text, track_id):
    track = common.get_entity_by_id(track_id)
    if comment_text != "":
        comment = Comment(content=comment_text)
        rating = Rating(likes=0, dislikes=0)
        comment.rating = rating
        # TODO: also add user key
        track.comment.append(comment)
    # TODO: add rating
    track.put()


# [START app]
app = webapp2.WSGIApplication([
    ('/api/tracks', TrackHandler)
], debug=True)
# [END app]
