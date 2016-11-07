from google.appengine.ext import ndb

class Band(ndb.Model):
    name = ndb.StringProperty()

class Album(ndb.Model):
    name = ndb.StringProperty()
    band = ndb.StructuredProperty(Band)

class Track(ndb.Model):
    name = ndb.StringProperty()
    album = ndb.StructuredProperty(Album)

class User(ndb.Model):
    name = ndb.StringProperty()

class Comment(ndb.Model):
    user = ndb.StructuredProperty(User)
    content = ndb.StringProperty()

