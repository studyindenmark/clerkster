import logging
from google.appengine.ext.ndb import Key
from webapp2 import RequestHandler
from models import Post
from facebook import FacebookAPI
from utils import scan_for_author


def fetch_threads(page):
  api = FacebookAPI(page.access_token)
  data = api.fetch(page.key.id() + '/threads')

  for thread in data.get('data'):
    messages = thread.get('messages').get('data')

    if len(messages) == 0:
      continue

    # Let the first message be the 'post'.
    message = messages.pop()

    post_model = Post(
      parent=page.key,
      is_private=True,
      is_reply=False,
      id=message.get('id'),
      created_time=FacebookAPI.parse_date(message.get('created_time')),
      from_id=message.get('from').get('id'),
      from_name=message.get('from').get('name'),
      message=message.get('message'),
      author=scan_for_author(message.get('message')),
    )
    post_model.put()

    # Let the rest of the messages be replies:
    for reply in messages:
      reply_model = Post(
        parent=post_model.key,
        is_private=True,
        is_reply=True,
        id=reply.get('id'),
        created_time=FacebookAPI.parse_date(reply.get('created_time')),
        from_id=reply.get('from').get('id'),
        from_name=reply.get('from').get('name'),
        message=reply.get('message'),
        author=scan_for_author(reply.get('message')),
      )
      reply_model.put()

def fetch_feed(page):
  api = FacebookAPI(page.access_token)
  data = api.fetch(page.key.id() + '/feed')

  for post in data.get('data'):
    post_model = Post(
      parent=page.key,
      id=post.get('id'),
      created_time=FacebookAPI.parse_date(post.get('created_time')),
      updated_time=FacebookAPI.parse_date(post.get('updated_time')),
      from_id=post.get('from').get('id'),
      from_name=post.get('from').get('name'),
      from_category=post.get('from').get('category'),
      message=post.get('message') or post.get('story'),
      author=scan_for_author(post.get('message')),
    )
    post_model.put()

    if not 'comments' in post:
      continue

    for comment in post.get('comments').get('data'):
      comment_model = Post(
        parent=post_model.key,
        is_reply=True,
        id=comment.get('id'),
        created_time=FacebookAPI.parse_date(comment.get('created_time')),
        from_id=comment.get('from').get('id'),
        from_name=comment.get('from').get('name'),
        from_category=comment.get('from').get('category'),
        message=comment.get('message'),
        author=scan_for_author(comment.get('message')),
      )
      comment_model.put()

class WorkerHandler(RequestHandler):

  def fetch_page(self):
    key = Key(urlsafe=self.request.get('key'))
    page = key.get()

    fetch_feed(page)
    fetch_threads(page)
