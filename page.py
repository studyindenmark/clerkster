from google.appengine.ext import ndb
from post import FacebookPost
from comment import FacebookComment
from facebook import FacebookAPI

class FacebookPage(ndb.Model):
  name = ndb.StringProperty()
  access_token = ndb.StringProperty()

  @property
  def json(self):
    return {
      'id': self.key.id(),
      'name': self.name,
    }

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
