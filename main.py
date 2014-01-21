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
  Route('/api/user', handler='handlers.UserHandler:get_info'),
  Route('/api/twitter/tweets', handler='handlers.TwitterHandler:get_tweets'),
  Route('/api/pages', handler='handlers.FacebookHandler:get_pages'),
  Route('/api/pages/<page_id>', handler='handlers.FacebookHandler:get_page', methods=['GET']),
  Route('/api/pages/<page_id>/feed', handler='handlers.FacebookHandler:get_feed', methods=['GET']),
  Route('/api/pages/<page_id>/threads', handler='handlers.FacebookHandler:get_threads', methods=['GET']),
  Route('/logout', handler='handlers.AuthHandler:logout', name='logout'),
  Route('/auth/<provider>', handler='handlers.AuthHandler:_simple_auth', name='auth_login'),
  Route('/auth/<provider>/callback', handler='handlers.AuthHandler:_auth_callback', name='auth_callback'),
  Route(r'<path:.*>', handler='handlers.RootHandler'),  
]

app = WSGIApplication(routes, config=app_config, debug=True)
