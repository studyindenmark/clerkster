# -*- coding: utf-8 -*-
import logging
import secrets
import json

import webapp2
from webapp2_extras import auth, sessions, jinja2
from jinja2.runtime import TemplateNotFound

from simpleauth import SimpleAuthHandler

from facebook import GraphAPI

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
  def jinja2(self):
    """Returns a Jinja2 renderer cached in the app registry"""
    return jinja2.get_jinja2(app=self.app)
    
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
  
      
  def render(self, template_name, template_vars={}):
    # Preset values for the template
    values = {
      'url_for': self.uri_for,
      'logged_in': self.logged_in,
      'flashes': self.session.get_flashes()
    }
    
    # Add manually supplied template values
    values.update(template_vars)
    
    # read the template or 404.html
    try:
      self.response.write(self.jinja2.render_template(template_name, **values))
    except TemplateNotFound:
      self.abort(404)

  def head(self, *args):
    """Head is used by Twitter. If not there the tweet button shows 0"""
    pass
    
    
class RootHandler(BaseRequestHandler):
  def get(self):
    """Handles default landing page"""
    self.render('home.html')
    

class ProfileHandler(BaseRequestHandler):
  def get(self):
    """Handles GET /profile"""    
    if self.logged_in:
      self.render('profile.html', {
        'user': self.current_user, 
        'session': self.auth.get_user_by_session()
      })
    else:
      self.redirect('/')


class AddAccountPageHandler(BaseRequestHandler):
  def get(self):
    """Handles GET /add"""    
    if self.logged_in:
      self.render('add.html', {
        'user': self.current_user, 
        'session': self.auth.get_user_by_session()
      })
    else:
      self.redirect('/')


class FacebookHandler(BaseRequestHandler):

  def __init__(self, request, response):
    self.initialize(request, response)
    self.graph = GraphAPI(
      access_token=self.current_user.facebook_access_token
    )

  def get_listing(self):
    """Handles GET /facebook/pages"""    
    if not self.logged_in:
      self.redirect('/')
      return

    pages = self.graph.get_connections("me", "accounts")

    self.render('facebook_pages.html', {
      'user': self.current_user,
      'pages': pages,
      'session': self.auth.get_user_by_session()
    })

  def post_page(self, page_id):
    pages = self.graph.get_connections("me", "accounts")
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
    m = models.FacebookPage.get_by_id(page_id)
    self.graph.access_token = m.access_token

    page = self.graph.get_object(page_id)
    posts = self.graph.get_connections(page_id, "posts")
    threads = self.graph.get_connections(page_id, "threads")

    # self.response.headers['Content-Type'] = 'application/json'
    # self.response.write(json.dumps(threads))
    # return

    self.render('facebook_page.html', {
      'user': self.current_user,
      'page': page,
      'posts': posts,
      'threads': threads,
      'session': self.auth.get_user_by_session()
    })


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
        'http://graph.facebook.com/{0}/picture?type=large'.format(id)),
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
    _attrs[provider + '_access_token'] = auth_info['access_token']

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

    # Go to the profile page
    self.redirect('/profile')

  def logout(self):
    self.auth.unset_session()
    self.redirect('/')

  def handle_exception(self, exception, debug):
    logging.error(exception)
    self.render('error.html', {'exception': exception})
    
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
