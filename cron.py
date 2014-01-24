import json
from webapp2 import RequestHandler
from google.appengine.api import taskqueue
from models import Page


class CronHandler(RequestHandler):

  def fetch_pages(self):
    keys = Page.query().fetch(keys_only=True)

    for key in keys:
      taskqueue.add(
        url='/worker/fetch_page',
        params={
          'key': key.urlsafe(),
        }
      )
