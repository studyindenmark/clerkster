import logging
from google.appengine.ext.ndb import Key
from webapp2 import RequestHandler
from webapp2_extras.appengine.auth.models import User
from page import FacebookPage

class WorkerHandler(RequestHandler):

  def fetch_page(self):
     # User ids are ints while page ids are strings.
    user_id = int(self.request.get('user_id'))
    page_id = self.request.get('page_id')

    key = Key(User, user_id, FacebookPage, page_id)
    page = key.get()

    page.fetch_feed()
    page.fetch_threads()
