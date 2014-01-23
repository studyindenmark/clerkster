from google.appengine.ext import ndb

class FacebookComment(ndb.Model):
  message = ndb.TextProperty()
  created_time = ndb.DateTimeProperty()
  from_id = ndb.StringProperty()
  from_name = ndb.StringProperty()
  from_category = ndb.StringProperty()
