# -*- coding: utf-8 -*-
import sys
from secrets import SESSION_KEY

from webapp2 import WSGIApplication, Route

# inject './lib' dir in the path so that we can simply do "import ndb" 
# or whatever there's in the app lib dir.
if 'lib' not in sys.path:
    sys.path[0:0] = ['lib']

# webapp2 config
app_config = {
  'webapp2_extras.sessions': {
    'cookie_name': '_simpleauth_sess',
    'secret_key': SESSION_KEY,
  },
  'webapp2_extras.auth': {
    'user_attributes': [],
  }
}
    
# Map URLs to handlers
routes = [
  Route('/', handler='handlers.RootHandler'),  
  Route('/add', handler='handlers.AddAccountPageHandler'),
  Route('/twitter/tweets', handler='handlers.TwitterHandler:get_tweets'),
  Route('/facebook/pages', handler='handlers.FacebookHandler:get_listing'),
  Route('/facebook/pages/<page_id>', handler='handlers.FacebookHandler:get_page', methods=['GET']),
  Route('/facebook/pages/<page_id>', handler='handlers.FacebookHandler:post_page', methods=['POST']),
  Route('/profile', handler='handlers.ProfileHandler', name='profile'),
  Route('/logout', handler='handlers.AuthHandler:logout', name='logout'),
  Route('/auth/<provider>', handler='handlers.AuthHandler:_simple_auth', name='auth_login'),
  Route('/auth/<provider>/callback', handler='handlers.AuthHandler:_auth_callback', name='auth_callback'),
]

app = WSGIApplication(routes, config=app_config, debug=True)
