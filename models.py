from google.appengine.ext import ndb
from google.appengine.api import taskqueue


class FetchLogItem(ndb.Model):
  date = ndb.DateTimeProperty(auto_now_add=True)


class FacebookPage(ndb.Model):
  name = ndb.StringProperty()
  access_token = ndb.StringProperty()

  @property
  def last_fetch_log_item(self):
    return FetchLogItem.query(ancestor=self.key)\
      .order(-FetchLogItem.date)\
      .fetch(limit=1)

  @property
  def posts(self):
    return FacebookPost\
      .query(ancestor=self.key)\
      .order(-FacebookPost.created_time)

  def _post_put_hook(self, future):
    taskqueue.add(
      url='/worker/fetch_page',
      params={
        'user_id': self.key.parent().id(),
        'page_id': self.key.id(),
      }
    )


class FacebookComment(ndb.Model):
  message = ndb.TextProperty()
  created_time = ndb.DateTimeProperty()
  from_id = ndb.StringProperty()
  from_name = ndb.StringProperty()
  from_category = ndb.StringProperty()


class FacebookPost(ndb.Model):
  type = ndb.StringProperty()
  message = ndb.TextProperty()
  created_time = ndb.DateTimeProperty()
  updated_time = ndb.DateTimeProperty()
  from_id = ndb.StringProperty()
  from_name = ndb.StringProperty()
  from_category = ndb.StringProperty()
  scanned_user_name = ndb.StringProperty()

  @property
  def comments(self):
    return FacebookComment.\
      query(ancestor=self.key).\
      order(FacebookComment.created_time)
