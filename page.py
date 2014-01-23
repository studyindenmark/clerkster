from datetime import datetime
from google.appengine.api import taskqueue
from google.appengine.ext import ndb
from post import FacebookPost
from comment import FacebookComment
from facebook import FacebookAPI
from log import FetchLogItem

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

  def fetch(self):
    self.fetch_feed()
    self.fetch_threads()
    self.fetched_time = datetime.now()
    FetchLogItem(parent=self.key).put()

  def fetch_threads(self):
    api = FacebookAPI(self.access_token)
    data = api.fetch(self.key.id() + '/threads')

    for thread in data.get('data'):
      messages = thread.get('messages').get('data')

      if len(messages) == 0:
        continue

      # Let the first message be the 'post'. First message is the last item.
      message = messages.pop()

      post_model = FacebookPost(
        parent=self.key,
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

  def fetch_feed(self):
    api = FacebookAPI(self.access_token)
    data = api.fetch(self.key.id() + '/feed')

    for post in data.get('data'):
      post_model = FacebookPost(
        parent=self.key,
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
