from google.appengine.ext import ndb


class FacebookPage(ndb.Model):
  name = ndb.StringProperty()
  access_token = ndb.StringProperty()

  @property
  def json(self):
    return {
      'id': self.key.id(),
      'name': self.name,
    }


class FacebookPost(ndb.Model):
  type = ndb.StringProperty()
  message = ndb.StringProperty()
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
      'from': {
        'id': self.from_id,
        'name': self.from_name,
        'category': self.from_category,
      },
      'scanned_user_name': self.scanned_user_name,
    }


class FacebookComment(ndb.Model):
  message = ndb.StringProperty()
  date = ndb.DateTimeProperty()
  facebook_user_id = ndb.StringProperty()
  facebook_user_name = ndb.StringProperty()
  scanned_user_name = ndb.StringProperty()

  @property
  def json(self):
    return {
      'id': self.key.id(),
      'date': self.date.strftime('%s'),
      'facebook_user_id': self.facebook_user_id,
      'facebook_user_name': self.facebook_user_name,
      'scanned_user_name': self.scanned_user_name,
    }
