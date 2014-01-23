from datetime import datetime
from google.appengine.ext import ndb
from google.appengine.api import taskqueue

class FacebookPage(ndb.Model):
  name = ndb.StringProperty()
  access_token = ndb.StringProperty()

  @property
  def json(self):
    return {
      'id': self.key.id(),
      'name': self.name,
    }

  def _post_put_hook(self, future):
    taskqueue.add(
      url='/worker/fetch_page',
      params={
        'user_id': self.key.parent().id(),
        'page_id': self.key.id(),
      }
    )
