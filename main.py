# -*- coding: utf-8 -*-
import sys
from webapp2 import WSGIApplication, Route
from secrets import SESSION_KEY


# webapp2 config
app_config = {
  'webapp2_extras.sessions': {
    'cookie_name': '_simpleauth_sess',
    'secret_key': SESSION_KEY,
  },
  'webapp2_extras.auth': {
    'user_model': 'models.User',
    'user_attributes': [],
  }
}
    
# Map URLs to handlers
routes = [
  Route('/cron/fetch_pages', handler='cron.CronHandler:fetch_pages'),
  Route('/cron/send_reports', handler='cron.CronHandler:send_reports'),
  
  Route('/worker/fetch_page', handler='worker.WorkerHandler:fetch_page'),
  Route('/worker/fetch_pages', handler='worker.WorkerHandler:fetch_pages'),
  Route('/worker/send_report', handler='worker.WorkerHandler:send_report'),

  Route('/api/user', handler='handlers.ApiHandler:get_user'),
  Route('/api/pages', handler='handlers.ApiHandler:get_pages'),
  Route('/api/pages/<page_id>', handler='handlers.ApiHandler:get_page', methods=['GET']),
  Route('/api/pages/<page_id>/search', handler='handlers.ApiHandler:search', methods=['GET']),

  Route('/api/facebook/pages/<page_id>/feed', handler='handlers.FacebookHandler:get_feed', methods=['GET']),
  Route('/api/facebook/pages/<page_id>/threads', handler='handlers.FacebookHandler:get_threads', methods=['GET']),

  Route('/logout', handler='handlers.AuthHandler:logout', name='logout'),
  Route('/auth/<provider>', handler='handlers.AuthHandler:_simple_auth', name='auth_login'),
  Route('/auth/<provider>/callback', handler='handlers.AuthHandler:_auth_callback', name='auth_callback'),
  Route(r'<path:.*>', handler='handlers.RootHandler'),  
]

app = WSGIApplication(routes, config=app_config, debug=True)
