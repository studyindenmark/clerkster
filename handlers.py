# -*- coding: utf-8 -*-
import logging
import secrets
import json
import os.path
import webapp2
from google.appengine.api import taskqueue
from webapp2_extras import auth, sessions
from simpleauth import SimpleAuthHandler
from facebook import FacebookAPI
from models import Page
from search import search_posts


class BaseRequestHandler(webapp2.RequestHandler):
  def dispatch(self):
    # Get a session store for this request.
    self.session_store = sessions.get_store(request=self.request)
    
    try:
      # Dispatch the request.
      webapp2.RequestHandler.dispatch(self)
    finally:
      # Save all sessions.
      self.session_store.save_sessions(self.response)
  
  @webapp2.cached_property
  def session(self):
    """Returns a session using the default cookie key"""
    return self.session_store.get_session()
    
  @webapp2.cached_property
  def auth(self):
      return auth.get_auth()
  
  @webapp2.cached_property
  def current_user(self):
    """Returns currently logged in user"""
    user_dict = self.auth.get_user_by_session()
    return self.auth.store.user_model.get_by_id(user_dict['user_id'])
      
  @webapp2.cached_property
  def logged_in(self):
    """Returns true if a user is currently logged in, false otherwise"""
    return self.auth.get_user_by_session() is not None
      
  def render(self, html_file):
    root = os.path.dirname(__file__)
    path = os.path.join(root, html_file)
    content = open(path).read()
    self.response.out.write(content)
    
    
class RootHandler(BaseRequestHandler):
  def get(self, **kwargs):
    """Handles default landing page"""
    if self.logged_in:
      self.render('index.html')
    else:
      self.render('login.html')
    

class ApiHandler(BaseRequestHandler):

  @classmethod
  def _user_to_json(cls, user):
    return {
      'avatar_url': user.avatar_url,
      'name': user.name,
      'author': user.author,
      'first_name': user.first_name,
      'last_name': user.last_name,
      'email': user.email,
      'last_fetched': user.last_fetched.strftime('%Y-%m-%d %H:%M')
        if user.last_fetched else None,
    }

  @classmethod
  def _page_to_json(cls, page):
    return {
      'id': page.key.id(),
      'name': page.name,
      'authors': page.authors,
      'last_fetched': page.last_fetched.strftime('%Y-%m-%d %H:%M')
        if page.last_fetched else None,
    }

  @classmethod
  def _doc_to_json(cls, doc, include_replies=False):
    return {
      'message': doc['message'],
      'created_time': doc['created_time'].strftime('%Y-%m-%d %H:%M'),
      'from': {
        'name': doc['from_name'],
      },
      'replies': [ApiHandler._doc_to_json(reply) for reply in
        reversed(doc['replies'])]
        if doc.get('replies') else None,
      'author': doc['author'],
    }

  def post_settings(self):
    input_data = json.loads(self.request.body)
    author = input_data.get('author')

    self.current_user.author = author
    self.current_user.put()

    data = ApiHandler._user_to_json(self.current_user)
    self.response.headers['Content-Type'] = 'application/json'
    self.response.write(json.dumps(data))

  def get_user(self):
    data = ApiHandler._user_to_json(self.current_user)
    self.response.headers['Content-Type'] = 'application/json'
    self.response.write(json.dumps(data))

  def get_pages(self):
    pages = self.current_user.pages
    data = [ApiHandler._page_to_json(m) for m in pages]
    self.response.headers['Content-Type'] = 'application/json'
    self.response.write(json.dumps(data))

  def get_page(self, page_id):
    m = Page.get_by_id(page_id, parent=self.current_user.key)

    if m == None:
      self.error(404)
      return

    data = ApiHandler._page_to_json(m)
    self.response.headers['Content-Type'] = 'application/json'
    self.response.write(json.dumps(data))

  def search(self, page_id):
    q = self.request.get('q')
    page = Page.get_by_id(page_id, parent=self.current_user.key)

    results = search_posts(page, q)
    results['posts'] = [ApiHandler._doc_to_json(doc)
      for doc in results['posts']]

    self.response.headers['Content-Type'] = 'application/json'
    self.response.write(json.dumps(results))


class FacebookHandler(BaseRequestHandler):

  def __init__(self, request, response):
    self.initialize(request, response)
    self.api = FacebookAPI(self.current_user.facebook_access_token)

  def _set_access_token_from_page(self, page_id):
    m = Page.get_by_id(page_id, parent=self.current_user.key)
    self.api.access_token = m.access_token

  def get_feed(self, page_id):
    self._set_access_token_from_page(page_id)
    data = self.api.fetch(page_id + "/feed")
    self.response.headers['Content-Type'] = 'application/json'
    self.response.write(json.dumps(data))

  def get_threads(self, page_id):
    self._set_access_token_from_page(page_id)
    data = self.api.fetch(page_id + "/threads")
    self.response.headers['Content-Type'] = 'application/json'
    self.response.write(json.dumps(data))


class AuthHandler(BaseRequestHandler, SimpleAuthHandler):
  """Authentication handler for OAuth 2.0, 1.0(a) and OpenID."""

  # Enable optional OAuth 2.0 CSRF guard
  OAUTH2_CSRF_STATE = True
  
  # Map Facebook API properties to our local DB User model properties.
  # Facebook = LEFT, our User model = RIGHT.
  USER_ATTRS = {
    'facebook' : {
      'id'     : lambda id: ('avatar_url', 
        'http://graph.facebook.com/{0}/picture?type=square'.format(id)),
      'name'   : 'name',
      'first_name'   : 'first_name',
      'last_name'   : 'last_name',
      'link'   : 'link',
      'email'   : 'email',
    },
  }

  def delete_account(self):
    user = self.current_user.delete()
    self.auth.unset_session()
    self.redirect('/')

  def _on_signin(self, data, auth_info, provider):
    """Callback whenever a new or existing user is logging in.
     data is a user info dictionary.
     auth_info contains access token or oauth token and secret.
    """
    auth_id = '%s:%s' % (provider, data['id'])
    logging.info('Looking for a user with id %s', auth_id)
    
    user = self.auth.store.user_model.get_by_auth_id(auth_id)
    _attrs = self._to_user_model_attrs(data, self.USER_ATTRS[provider])
    _attrs['facebook_access_token'] = auth_info['access_token']

    if user:
      logging.info('Found existing user to log in')
      # Existing users might've changed their profile data so we update our
      # local model anyway. This might result in quite inefficient usage
      # of the Datastore, but we do this anyway for demo purposes.
      #
      # In a real app you could compare _attrs with user's properties fetched
      # from the datastore and update local user in case something's changed.
      user.populate(**_attrs)
      user.put()
      self.auth.set_session(self.auth.store.user_to_dict(user))
      
    else:
      # check whether there's a user currently logged in
      # then, create a new user if nobody's signed in, 
      # otherwise add this auth_id to currently logged in user.

      if self.logged_in:
        logging.info('Updating currently logged in user')
        
        u = self.current_user
        u.populate(**_attrs)
        # The following will also do u.put(). Though, in a real app
        # you might want to check the result, which is
        # (boolean, info) tuple where boolean == True indicates success
        # See webapp2_extras.appengine.auth.models.User for details.
        u.add_auth_id(auth_id)
        
      else:
        logging.info('Creating a brand new user')
        ok, user = self.auth.store.user_model.create_user(auth_id, **_attrs)
        if ok:
          self.auth.set_session(self.auth.store.user_to_dict(user))

    taskqueue.Queue('facebook').add(
      taskqueue.Task(
        url='/worker/fetch_pages_for_user',
        params={
          'key': user.key.urlsafe(),
        }
      )
    )

    self.redirect('/')

  def logout(self):
    self.auth.unset_session()
    self.redirect('/')

  def _callback_uri_for(self, provider):
    return self.uri_for('auth_callback', provider=provider, _full=True)
    
  def _get_consumer_info_for(self, provider):
    """Returns a tuple (key, secret) for auth init requests."""
    return secrets.AUTH_CONFIG[provider]
    
  def _to_user_model_attrs(self, data, attrs_map):
    """Get the needed information from the provider dataset."""
    user_attrs = {}
    for k, v in attrs_map.iteritems():
      attr = (v, data.get(k)) if isinstance(v, str) else v(data.get(k))
      user_attrs.setdefault(*attr)

    return user_attrs
