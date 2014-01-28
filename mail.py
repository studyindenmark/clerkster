from datetime import datetime
from datetime import timedelta
from google.appengine.api import mail
from search import search_posts
from config import EMAIL_SENDER
from config import EMAIL_DOMAIN


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

    link = EMAIL_DOMAIN + '/pages/%s?from=%s&to=%s' % (
      page.key.id(),
      from_date,
      to_date,
    )

    results = search_posts(
      page,
      'created_time >= %s AND created_time <= %s' % (from_date, to_date)
    )

    body += '%s\n' % page.name
    body += 'Posts: %s\n' % results['nr_of_posts']
    body += 'Comments: %s\n' % results['nr_of_comments']
    body += '%s\n\n' % link

  print body

  mail.send_mail(
    sender=EMAIL_SENDER,
    to="%s <%s>" % (user.name, user.email),
    subject=subject,
    body=body
  )
