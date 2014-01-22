import json
from webapp2 import RequestHandler
from google.appengine.api import taskqueue
from page import FacebookPage

class CronHandler(RequestHandler):

  def fetch_pages(self):
    keys = FacebookPage.query().fetch(keys_only=True)

    for key in keys:
      taskqueue.add(
        url='/worker/fetch_page',
        params={
          'user_id': key.parent().id(),
          'page_id': key.id(),
        }
      )
