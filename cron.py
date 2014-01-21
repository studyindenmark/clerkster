import json
from webapp2 import RequestHandler
from google.appengine.api import taskqueue
from models import FacebookPage


class CronHandler(RequestHandler):

  def fetch_pages(self):
    keys = FacebookPage.query().fetch(keys_only=True)
    data = []

    for key in keys:
      data.append({
        'user_id': key.parent().id(),
        'page_id': key.id(),
      })
      taskqueue.add(
        url='/worker/fetch_page',
        params={
          'user_id': key.parent().id(),
          'page_id': key.id(),
        }
      )

    self.response.headers['Content-Type'] = 'application/json'
    self.response.write(json.dumps(data))

