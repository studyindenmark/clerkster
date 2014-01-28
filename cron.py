import json
from webapp2 import RequestHandler
from google.appengine.api import taskqueue
from models import Page
from webapp2_extras.appengine.auth.models import User


class CronHandler(RequestHandler):

  def fetch_pages(self):
    queue = taskqueue.Queue('facebook')
    keys = Page.query().fetch(keys_only=True)

    for key in keys:
      task = taskqueue.Task(
        url='/worker/fetch_page',
        params={
          'key': key.urlsafe(),
        }
      )
      queue.add(task)

  def send_reports(self):
    queue = taskqueue.Queue('mail')
    keys = User.query().fetch(keys_only=True)

    for key in keys:
      task = taskqueue.Task(
        url='/worker/send_report',
        params={
          'key': key.urlsafe(),
        }
      )
      queue.add(task)
