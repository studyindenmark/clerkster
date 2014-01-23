from google.appengine.ext import ndb
from comment import FacebookComment

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
