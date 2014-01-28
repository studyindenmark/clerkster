import json
from webapp2 import RequestHandler
from google.appengine.api import taskqueue
from webapp2_extras.appengine.auth.models import User
from google.appengine.ext import ndb

class FacebookPost(ndb.Model):
  pass

class FacebookPage(ndb.Model):
  pass

class FacebookComment(ndb.Model):
  pass

class MigrateHandler(RequestHandler):

  def reset(self):
    ndb.delete_multi(FacebookPost.query().fetch(keys_only=True))
    ndb.delete_multi(FacebookComment.query().fetch(keys_only=True))
    ndb.delete_multi(FacebookPage.query().fetch(keys_only=True))
