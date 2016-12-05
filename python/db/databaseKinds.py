from google.appengine.ext import ndb


class Rating(ndb.Model):
    likes = ndb.IntegerProperty()
    dislikes = ndb.IntegerProperty()


class Description(ndb.Model):
    description = ndb.StringProperty()
    # more to be added, pics and such.


# Has user as parent
class Comment(ndb.Model):
    content = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    rating = ndb.StructuredProperty(Rating)
    account = ndb.KeyProperty()


class Band(ndb.Model):
    name = ndb.StringProperty()
    comment = ndb.StructuredProperty(Comment, repeated=True)
    rating = ndb.StructuredProperty(Rating)
    description = ndb.StructuredProperty(Description)


# Has Band as parent
class Album(ndb.Model):
    name = ndb.StringProperty()
    comment = ndb.StructuredProperty(Comment, repeated=True)
    rating = ndb.StructuredProperty(Rating)
    description = ndb.StructuredProperty(Description)
    band = ndb.KeyProperty()


# Has Album as parent
class Track(ndb.Model):
    name = ndb.StringProperty()
    comment = ndb.StructuredProperty(Comment, repeated=True)
    rating = ndb.StructuredProperty(Rating)
    album = ndb.KeyProperty()


class Account(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
