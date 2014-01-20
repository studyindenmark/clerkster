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
