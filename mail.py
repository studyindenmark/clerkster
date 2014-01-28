from datetime import datetime
from datetime import timedelta
from google.appengine.api import mail
from search import search_posts


FROM = 'per@youtify.com' # <-- chanage
DOMAIN = 'http://studyindenmark-clerkster.appspot.com'


def send_report(user):
  now = datetime.now()
  first_day_this_month = datetime(now.year, now.month, 1)
  last_day_last_month = first_day_this_month - timedelta(days=1)
  first_day_last_month = datetime(
    last_day_last_month.year,
    last_day_last_month.month,
    1
  )

  subject = 'Your Clerkster report, %s' % last_day_last_month.strftime('%b %Y') # e.g. 'Jan 2014'
  body = ''

  for page in user.pages:
    from_date = first_day_last_month.strftime('%Y-%m-%d')
    to_date = last_day_last_month.strftime('%Y-%m-%d')

    link = DOMAIN + '/pages/%s?from=%s&to=%s' % (
      page.key.id(),
      from_date,
      to_date,
    )

    results = search_posts(
      page,
      'created_time >= %s AND created_time <= %s' % (from_date, to_date)
    )

    body += '%s: %s\n' % (page.name, link)
    body += 'Posts: %s\n' % results['nr_of_posts']
    body += 'Comments: %s\n' % results['nr_of_comments']
    body += '\n\n'

  print body

  mail.send_mail(
    sender="Clerkster <%s>" % FROM,
    to="%s <%s>" % (user.name, user.email),
    subject=subject,
    body=body
  )
