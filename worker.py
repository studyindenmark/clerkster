import logging
from google.appengine.ext.ndb import Key
from webapp2 import RequestHandler
from webapp2_extras.appengine.auth.models import User
from models import FacebookPage, FacebookPost, FacebookComment
from facebook import FacebookAPI


class WorkerHandler(RequestHandler):

  def fetch_page(self):
     # User ids are ints while page ids are strings.
    user_id = int(self.request.get('user_id'))
    page_id = self.request.get('page_id')

    # Produce the key and get the page.
    key = Key(User, user_id, FacebookPage, page_id)
    page = key.get()

    logging.info("Fetching page %s" % page.name)

    # Fetch the page feed from the API.
    api = FacebookAPI(page.access_token)
    data = api.fetch(page.key.id() + '/feed')

    for post in data.get('data'):
      m = FacebookPost(
        parent=page.key,
        id=post.get('id'),
        created_time=FacebookAPI.parse_date(post.get('created_time')),
        updated_time=FacebookAPI.parse_date(post.get('created_time')),
        type=post.get('type'),
        from_id=post.get('from').get('id'),
        from_name=post.get('from').get('name'),
        from_category=post.get('from').get('category'),
        message=post.get('message') or post.get('story'),
      )
      m.put()
