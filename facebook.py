"""Thin Facebook API wrapper"""
import json
from urllib import urlencode
from google.appengine.api import urlfetch

class FacebookAPI(object):

  def __init__(self, access_token):
    self.access_token = access_token

  def fetch(self, path, params={}):
    params['access_token'] = self.access_token
    url = "https://graph.facebook.com/%s?%s" % (path, urlencode(params))
    r = urlfetch.fetch(url)
    if r.status_code != 200:
        raise Exception("%s returned %s - %s" % (url, r.status_code, r.content))
    return json.loads(r.content)
