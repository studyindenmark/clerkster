from google.appengine.ext import ndb

class FetchLogItem(ndb.Model):
  date = ndb.DateTimeProperty(auto_now_add=True)

  @property
  def json(self):
    return {
      'date': self.date.strftime('%s'),
    }
