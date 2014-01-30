from google.appengine.ext import ndb
from google.appengine.api import taskqueue
from webapp2_extras.appengine.auth import models as webappmodels


class User(webappmodels.User):

  last_fetched = ndb.DateTimeProperty()
  author = ndb.StringProperty()

  def delete(self):
    ndb.delete_multi(ndb.Query(ancestor=self.key).iter(keys_only=True))
    webappmodels.Unique.delete_multi(
      map(lambda s: 'User.auth_id:' + s, self.auth_ids)
    )

  @property
  def pages(self):
    return Page.query(ancestor=self.key)


class Page(ndb.Model):
  name = ndb.StringProperty()
  access_token = ndb.StringProperty()
  last_fetched = ndb.DateTimeProperty()

  @property
  def authors(self):
    return [post.author for post in Post.query(
      ancestor=self.key,
      projection=['author'],
      distinct=True
    ) if post.author != None]

  @property
  def posts(self):
    return Post\
      .query(ancestor=self.key)\
      .order(-Post.created_time)\
      .filter(Post.is_reply == False)


class Post(ndb.Model):
  is_reply = ndb.BooleanProperty(indexed=True, default=False)
  is_private = ndb.BooleanProperty(default=False)
  message = ndb.TextProperty()
  created_time = ndb.DateTimeProperty()
  updated_time = ndb.DateTimeProperty()
  from_id = ndb.StringProperty()
  from_name = ndb.StringProperty()
  from_category = ndb.StringProperty()
  author = ndb.StringProperty(indexed=True)

  @property
  def replies(self):
    return Post\
      .query(ancestor=self.key)\
      .filter(Post.is_reply == True)\
      .order(Post.created_time)
