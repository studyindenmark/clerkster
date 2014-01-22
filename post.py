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
  def json(self):
    return {
      'id': self.key.id(),
      'type': self.type,
      'message': self.message,
      'created_time': self.created_time.strftime('%s'),
      'updated_time': self.updated_time.strftime('%s'),
      'comments': [m.json for m in FacebookComment.\
        query(ancestor=self.key).\
        order(FacebookComment.created_time)],
      'from': {
        'id': self.from_id,
        'name': self.from_name,
        'category': self.from_category,
      },
      'scanned_user_name': self.scanned_user_name,
    }

