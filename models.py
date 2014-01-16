from google.appengine.ext import ndb

class FacebookPage(ndb.Model):
	name = ndb.StringProperty()
	access_token = ndb.StringProperty()
