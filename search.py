from google.appengine.api import search 

def create_document(post):
  parent = None

  if post.is_reply:
    parent = post.key.parent().urlsafe()

  return search.Document(doc_id=post.key.urlsafe(), fields=[
    search.TextField(name='author', value=post.author),
    search.TextField(name='from_name', value=post.from_name),
    search.TextField(name='message', value=post.message),
    search.TextField(name='parent', value=parent),
    search.DateField(name='created_time', value=post.created_time),
  ])

def index(page, docs):
  index = search.Index(page.key.urlsafe())

  # Can only index 200 docs at a time.
  start = 0
  while start < len(docs):
    index.put(docs[start:start+200])
    start += 200

def doc_to_json(doc):
  d = {}
  for field in doc.fields:
    d[field.name] = field.value
  return d


def search_posts(page, query_string):
  ret = []
  parents = {}
  index = search.Index(page.key.urlsafe())

  expr_list = [
    search.SortExpression(
      expression="created_time",
      direction=search.SortExpression.DESCENDING
    )
  ]

  sort_options = search.SortOptions(expressions=expr_list)
  query_options = search.QueryOptions(sort_options=sort_options)

  query = search.Query(query_string=query_string, options=query_options)
  result = index.search(query)

  for doc in result:
    parent_key = doc.field('parent').value

    if parent_key:
      parent = None
      if parent_key in parents:
        parent = parents[parent_key]
      else:
        parent_doc = index.get(parent_key)
        parent = doc_to_json(parent_doc)
        parent['replies'] = []
        parents[parent_key] = parent
        ret.append(parent)
      parent['replies'].append(doc_to_json(doc))
    else:
      d = doc_to_json(doc)
      ret.append(d)

  return ret