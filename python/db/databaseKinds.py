from google.appengine.ext import ndb


class Rating(ndb.Model):
    likes = ndb.IntegerProperty()
    dislikes = ndb.IntegerProperty()


class Description(ndb.Model):
    description = ndb.StringProperty()
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
    description = ndb.StructuredProperty(Description)


# Has Band as owner
class Album(ndb.Model):
    name = ndb.StringProperty()
    comment = ndb.StructuredProperty(Comment, repeated=True)
    rating = ndb.StructuredProperty(Rating)
    description = ndb.StructuredProperty(Description)
    owner = ndb.KeyProperty()


# Has Album as owner
class Track(ndb.Model):
    name = ndb.StringProperty()
    comment = ndb.StructuredProperty(Comment, repeated=True)
    rating = ndb.StructuredProperty(Rating)
    owner = ndb.KeyProperty()


class Account(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)


# Has user as owner
class TopList(ndb.Model):
    name = ndb.StringProperty()
    kind = ndb.StringProperty()
    content = ndb.KeyProperty(repeated=True)
    date = ndb.DateTimeProperty(auto_now_add=True)
    rating = ndb.StructuredProperty(Rating)
    owner = ndb.KeyProperty()
