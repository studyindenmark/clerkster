from google.appengine.api import search 

def create_document(post):
  return search.Document(doc_id=post.key.urlsafe(), fields=[
    search.TextField(name='author', value=post.author),
    search.TextField(name='from_name', value=post.from_name),
    search.TextField(name='message', value=post.message),
    search.DateField(name='created_time', value=post.created_time),
  ])

def index(page, docs):
  index = search.Index(page.key.urlsafe())

  # Can only index 200 docs at a time.
  start = 0
  while start < len(docs):
    index.put(docs[start:start+200])
    start += 200


def find(page, q):
  return []
