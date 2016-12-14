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
    description = ndb.StringProperty()
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

    def to_dict(self):
        dicti = {}
        dicti['content'] = self.content
        dicti['date'] = str(self.date)
        if self.rating:
            dicti['rating'] = {'likes': self.rating.likes, 'dislikes': self.rating.dislikes}
        if self.owner:
            dicti['owner'] = self.owner.id()
        return dicti


class Band(ndb.Model):
    name = ndb.StringProperty()
    comment = ndb.StructuredProperty(Comment, repeated=True)
    rating = ndb.StructuredProperty(Rating)
    description = ndb.StructuredProperty(BandDescription)

    def to_dict(self):
        dicti = {}
        dicti['id'] = self.key.id()
        dicti['name'] = self.name
        dicti['description'] = self.description.to_dict()
        dicti['rating'] = self.rating.to_dict()
        dicti['comment'] = []
        for comment in self.comment:
            dicti['comment'].append(comment.to_dict())
        return dicti


# Has Band as owner
class Album(ndb.Model):
    name = ndb.StringProperty()
    comment = ndb.StructuredProperty(Comment, repeated=True)
    rating = ndb.StructuredProperty(Rating)
    description = ndb.StructuredProperty(AlbumDescription)
    owner = ndb.KeyProperty()

    def to_dict(self):
        dicti = {}
        dicti['id'] = self.key.id()
        dicti['owner'] = self.owner.id()
        dicti['name'] = self.name
        dicti['description'] = self.description.to_dict()
        dicti['rating'] = self.rating.to_dict()
        dicti['comment'] = []
        for comment in self.comment:
            dicti['comment'].append(comment.to_dict())
        return dicti


# Has Album as owner
class Track(ndb.Model):
    name = ndb.StringProperty()
    comment = ndb.StructuredProperty(Comment, repeated=True)
    rating = ndb.StructuredProperty(Rating)
    owner = ndb.KeyProperty()
    description = ndb.StructuredProperty(TrackDescription)

    def to_dict(self):
        dicti = {}
        dicti['id'] = self.key.id()
        dicti['owner'] = self.owner.id()
        dicti['name'] = self.name
        dicti['description'] = self.description.to_dict()
        dicti['rating'] = self.rating.to_dict()
        dicti['comment'] = []
        for comment in self.comment:
            dicti['comment'].append(comment.to_dict())
        return dicti


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

    def to_dict(self):
        dicti = {}
        dicti['id'] = self.key.id()
        dicti['owner'] = self.owner.id()
        dicti['name'] = self.name
        dicti['kind'] = self.kind
        dicti['date'] = str(self.date)
        dicti['rating'] = self.rating.to_dict()
        dicti['content'] = []
        for con in self.content:
            dicti['comment'].append(con.id())
        return dicti
