from google.appengine.ext import ndb

class FacebookComment(ndb.Model):
  message = ndb.TextProperty()
  created_time = ndb.DateTimeProperty()
  from_id = ndb.StringProperty()
  from_name = ndb.StringProperty()
  from_category = ndb.StringProperty()

  @property
  def json(self):
    return {
      'id': self.key.id(),
      'message': self.message,
      'created_time': self.created_time.strftime('%s'),
      'from': {
        'id': self.from_id,
        'name': self.from_name,
        'category': self.from_category,
      },
    }
