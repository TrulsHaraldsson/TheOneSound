from google.appengine.ext import ndb


class UserRating(ndb.Model):
    rated_key = ndb.KeyProperty()
    value = ndb.BooleanProperty()  # true = like, false = dislike


class Rating(ndb.Model):
    likes = ndb.IntegerProperty()
    dislikes = ndb.IntegerProperty()


class TrackDescription(ndb.Model):
    description = ndb.TextProperty()
    youtube_url = ndb.StringProperty()


class AlbumDescription(ndb.Model):
    description = ndb.StringProperty()
    picture_url = ndb.StringProperty()
    # more to be added, pics and such.


class BandDescription(ndb.Model):
    biography = ndb.StringProperty()
    members = ndb.StringProperty(repeated=True)
    genres = ndb.StringProperty(repeated=True)
    picture_url = ndb.StringProperty()
    # more to be added, pics and such.


# Has user as owner
class Comment(ndb.Model):
    content = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    rating = ndb.StructuredProperty(Rating)
    owner = ndb.KeyProperty()


class Band(ndb.Model):
    name = ndb.StringProperty()
    comment = ndb.StructuredProperty(Comment, repeated=True)
    rating = ndb.StructuredProperty(Rating)
    description = ndb.StructuredProperty(BandDescription)


# Has Band as owner
class Album(ndb.Model):
    name = ndb.StringProperty()
    comment = ndb.StructuredProperty(Comment, repeated=True)
    rating = ndb.StructuredProperty(Rating)
    description = ndb.StructuredProperty(AlbumDescription)
    owner = ndb.KeyProperty()


# Has Album as owner
class Track(ndb.Model):
    name = ndb.StringProperty()
    comment = ndb.StructuredProperty(Comment, repeated=True)
    rating = ndb.StructuredProperty(Rating)
    owner = ndb.KeyProperty()
    description = ndb.StructuredProperty(TrackDescription)


class Account(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    ratings = ndb.StructuredProperty(UserRating, repeated=True)


# Has user as owner
class TopList(ndb.Model):
    name = ndb.StringProperty()
    kind = ndb.StringProperty()
    content = ndb.KeyProperty(repeated=True)
    date = ndb.DateTimeProperty(auto_now_add=True)
    rating = ndb.StructuredProperty(Rating)
    owner = ndb.KeyProperty()
