import logging
from google.appengine.ext.ndb import Key
from webapp2 import RequestHandler
from webapp2_extras.appengine.auth.models import User
from page import FacebookPage
from post import FacebookPost
from comment import FacebookComment
from log import FetchLogItem
from facebook import FacebookAPI

def fetch_threads(page):
  api = FacebookAPI(page.access_token)
  data = api.fetch(page.key.id() + '/threads')

  for thread in data.get('data'):
    messages = thread.get('messages').get('data')

    if len(messages) == 0:
      continue

    # Let the first message be the 'post'. First message is the last item.
    message = messages.pop()

    post_model = FacebookPost(
      parent=page.key,
      id=message.get('id'),
      created_time=FacebookAPI.parse_date(message.get('created_time')),
      type='email',
      from_id=message.get('from').get('id'),
      from_name=message.get('from').get('name'),
      message=message.get('message'),
    )
    post_model.put()

    # Let the rest of the messages be comments:
    for comment in messages:
      comment_model = FacebookComment(
        parent=post_model.key,
        id=comment.get('id'),
        created_time=FacebookAPI.parse_date(comment.get('created_time')),
        from_id=comment.get('from').get('id'),
        from_name=comment.get('from').get('name'),
        message=comment.get('message'),
      )
      comment_model.put()

def fetch_feed(page):
  api = FacebookAPI(page.access_token)
  data = api.fetch(page.key.id() + '/feed')

  for post in data.get('data'):
    post_model = FacebookPost(
      parent=page.key,
      id=post.get('id'),
      created_time=FacebookAPI.parse_date(post.get('created_time')),
      updated_time=FacebookAPI.parse_date(post.get('updated_time')),
      type=post.get('type'),
      from_id=post.get('from').get('id'),
      from_name=post.get('from').get('name'),
      from_category=post.get('from').get('category'),
      message=post.get('message') or post.get('story'),
    )
    post_model.put()

    if not 'comments' in data:
      continue

    for comment in post_data.get('comments').get('data'):
      comment_model = FacebookComment(
        parent=post_model.key,
        id=comment.get('id'),
        created_time=FacebookAPI.parse_date(comment.get('created_time')),
        from_id=comment.get('from').get('id'),
        from_name=comment.get('from').get('name'),
        from_category=comment.get('from').get('category'),
        message=comment.get('message'),
      )
      comment_model.put()

class WorkerHandler(RequestHandler):

  def fetch_page(self):
     # User ids are ints while page ids are strings.
    user_id = int(self.request.get('user_id'))
    page_id = self.request.get('page_id')

    key = Key(User, user_id, FacebookPage, page_id)
    page = key.get()

    fetch_feed(page)
    fetch_threads(page)

    FetchLogItem(parent=page.key).put()
