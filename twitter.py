"""Thin Twitter API wrapper, uses same OAuth library as simpleauth"""
import json
from oauth2 import Client, Request, Consumer, Token, SignatureMethod_HMAC_SHA1
from urlparse import parse_qs

class TwitterAPI(object):

  def __init__(self, consumer_key, consumer_secret, oauth_token, oauth_token_secret):
    consumer = Consumer(consumer_key, consumer_secret)
    token = Token(oauth_token, oauth_token_secret)
    self.client = Client(consumer, token)
    self.client.set_signature_method(SignatureMethod_HMAC_SHA1())

  def get_tweets(self, screen_name):
    url = 'https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=%s' % screen_name
    resp, content = self.client.request(url, method='GET')
    return json.loads(content)
