"""Thin Facebook API wrapper"""
import json
from datetime import datetime
from urllib import urlencode
from google.appengine.api import urlfetch

class FacebookAPI(object):

  def __init__(self, access_token):
    self.access_token = access_token

  @classmethod
  def parse_date(cls, s):
  	"""Parses e.g. '2011-03-06T03:36:45+0000'

  	From http://stackoverflow.com/questions/7142618/parse-fb-graph-api-date-string-into-python-datetime
  	"""
  	return datetime.strptime(s, '%Y-%m-%dT%H:%M:%S+0000')

  def fetch(self, path, params={}):
    params['access_token'] = self.access_token
    url = "https://graph.facebook.com/%s?%s" % (path, urlencode(params))
    r = urlfetch.fetch(url)
    if r.status_code != 200:
        raise Exception("%s returned %s - %s" % (url, r.status_code, r.content))
    return json.loads(r.content)
