from google.appengine.ext import ndb

class FetchLogItem(ndb.Model):
  date = ndb.DateTimeProperty(auto_now_add=True)
