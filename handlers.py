# -*- coding: utf-8 -*-
import logging
import secrets
import json
import os.path

import webapp2
from webapp2_extras import auth, sessions

from simpleauth import SimpleAuthHandler

from facebook import FacebookAPI
from twitter import TwitterAPI

import models


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

  def head(self, *args):
    """Head is used by Twitter. If not there the tweet button shows 0"""
    pass
    
    
class RootHandler(BaseRequestHandler):
  def get(self):
    """Handles default landing page"""
    if self.logged_in:
      self.render('index.html')
    else:
      self.render('login.html')
    

class FacebookHandler(BaseRequestHandler):

  def __init__(self, request, response):
    self.initialize(request, response)
    self.api = FacebookAPI(self.current_user.facebook_access_token)

  def get_pages(self):
    """Handles GET /facebook/pages"""    
    data = self.api.fetch("me/accounts")
    self.response.headers['Content-Type'] = 'application/json'
    self.response.write(json.dumps(data))

  def _set_access_token_from_page(self, page_id):
    m = models.FacebookPage.get_by_id(page_id)
    self.api.access_token = m.access_token

  def post_page(self, page_id):
    pages = self.api.fetch("me/accounts")
    m = None
    for page in pages['data']:
      if page['id'] == page_id:
        m = models.FacebookPage(
          id=page_id,
          access_token=page['access_token'],
          name=page['name'],
        )
        m.put()
        break
    assert m is not None
    self.redirect('/facebook/pages/%s' % page_id)

  def get_page(self, page_id):
    self._set_access_token_from_page(page_id)
    data = self.api.fetch(page_id)
    self.response.headers['Content-Type'] = 'application/json'
    self.response.write(json.dumps(data))

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


class UserHandler(BaseRequestHandler):

  def get_info(self):
    data = {
      'avatar_url': self.current_user.avatar_url,
      'name': self.current_user.name,
    }
    self.response.headers['Content-Type'] = 'application/json'
    self.response.write(json.dumps(data))


class TwitterHandler(BaseRequestHandler):

  def __init__(self, request, response):
    self.initialize(request, response)

    assert self.current_user.twitter_oauth_token
    assert self.current_user.twitter_oauth_token_secret

    self.api = TwitterAPI(
      secrets.TWITTER_CONSUMER_KEY,
      secrets.TWITTER_CONSUMER_SECRET,
      self.current_user.twitter_oauth_token,
      self.current_user.twitter_oauth_token_secret,
    )

  def get_tweets(self):
    data = self.api.get_tweets(screen_name='youtify')
    self.response.headers['Content-Type'] = 'application/json'
    self.response.write(json.dumps(data))


class AuthHandler(BaseRequestHandler, SimpleAuthHandler):
  """Authentication handler for OAuth 2.0, 1.0(a) and OpenID."""

  # Enable optional OAuth 2.0 CSRF guard
  OAUTH2_CSRF_STATE = True
  
  USER_ATTRS = {
    'twitter'  : {
      'profile_image_url': 'avatar_url',
      'screen_name'      : 'name',
      'link'             : 'link'
    },
    'facebook' : {
      'id'     : lambda id: ('avatar_url', 
        'http://graph.facebook.com/{0}/picture?type=square'.format(id)),
      'name'   : 'name',
      'link'   : 'link'
    },
  }
  
  def _on_signin(self, data, auth_info, provider):
    """Callback whenever a new or existing user is logging in.
     data is a user info dictionary.
     auth_info contains access token or oauth token and secret.
    """
    auth_id = '%s:%s' % (provider, data['id'])
    logging.info('Looking for a user with id %s', auth_id)
    
    user = self.auth.store.user_model.get_by_auth_id(auth_id)
    _attrs = self._to_user_model_attrs(data, self.USER_ATTRS[provider])

    if provider == 'facebook':
      _attrs['facebook_access_token'] = auth_info['access_token']
    elif provider == 'twitter':
      _attrs['twitter_oauth_token'] = auth_info['oauth_token']
      _attrs['twitter_oauth_token_secret'] = auth_info['oauth_token_secret']

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
