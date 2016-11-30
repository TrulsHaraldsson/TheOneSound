import webapp2
import json
from python.databaseKinds import Rating, Comment, Album, Track
from python import JINJA_ENVIRONMENT
from google.appengine.ext import ndb
from google.appengine.api import users
from python.util import entityparser
from python.api import common


class TrackHandler(webapp2.RequestHandler):
    # creates one new track
    # maybe make so multiple can be made ?
    def post(self):
        track_name = self.request.get("name")
        parent_id = self.request.get("parent_id")
        try:
            create_new_track(track_name, parent_id)
        except Exception as e:
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
            self.response.set_status(400)

    # updates a track with the new information
    def put(self, track_id):
        try:
            comment_text = self.request.get("comment_text")
            update_track(comment_text, int(track_id))

        except Exception as e:
            self.response.set_status(400)


class TrackByNameHandler(webapp2.RequestHandler):
    # returns all tracks with matching name
    def get(self, track_name):
        try:
            tracks = get_tracks_by_name(track_name)
            if len(tracks) > 1:
                self.response.set_status(300)  # multiple choices
            else:
                track_list = entityparser.entities_to_dic_list(tracks)
                self.response.out.write(json.dumps(track_list))
        except Exception as e:
            self.response.set_status(400)


# Should make parent_id as parent!
def create_new_track(track_name, parent_id):
    if track_name == "":
        raise ValueError("track must have a name.")
    track = Track(name=track_name)
    rating = Rating(likes=0, dislikes=0)
    track.rating = rating
    track.put()


def update_track(comment_text, track_id):
    track = common.get_entity_by_id(track_id)
    if comment_text != "":
        comment = Comment(content=comment_text)
        comment.rating = rating
        # TODO: also add user key
        track.comment = comment
    # TODO: add rating
    track.put()


# [START app]
app = webapp2.WSGIApplication([
    ('/api/tracks', TrackHandler),
    ('/api/tracks/(\w+)', TrackByNameHandler)
], debug=True)
# [END app]
