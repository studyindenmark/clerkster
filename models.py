from google.appengine.ext import ndb
from google.appengine.api import taskqueue


class FacebookPage(ndb.Model):
  name = ndb.StringProperty()
  access_token = ndb.StringProperty()

  @property
  def posts(self):
    return FacebookPost\
      .query(ancestor=self.key)\
      .order(-FacebookPost.created_time)

  def _post_put_hook(self, future):
    taskqueue.add(
      url='/worker/fetch_page',
      params={
        'key': self.key.urlsafe(),
      }
    )


class FacebookComment(ndb.Model):
  message = ndb.TextProperty()
  created_time = ndb.DateTimeProperty()
  from_id = ndb.StringProperty()
  from_name = ndb.StringProperty()
  from_category = ndb.StringProperty()
  author = ndb.StringProperty()


class FacebookPost(ndb.Model):
  type = ndb.StringProperty()
  message = ndb.TextProperty()
  created_time = ndb.DateTimeProperty()
  updated_time = ndb.DateTimeProperty()
  from_id = ndb.StringProperty()
  from_name = ndb.StringProperty()
  from_category = ndb.StringProperty()
  author = ndb.StringProperty()

  @property
  def comments(self):
    return FacebookComment.\
      query(ancestor=self.key).\
      order(FacebookComment.created_time)
