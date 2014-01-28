import json
from webapp2 import RequestHandler
from google.appengine.api import taskqueue
from models import Page
from webapp2_extras.appengine.auth.models import User


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

  def send_reports(self):
    keys = User.query().fetch(keys_only=True)

    for key in keys:
      taskqueue.add(
        url='/worker/send_report',
        params={
          'key': key.urlsafe(),
        }
      )
