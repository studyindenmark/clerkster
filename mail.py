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

    link = EMAIL_DOMAIN + '/pages/%s?from=%s&to=%s&author=%s' % (
      page.key.id(),
      from_date,
      to_date,
      user.first_name,
    )

    results = search_posts(
      page,
      'created_time >= %s AND created_time <= %s AND author: %s' % (from_date, to_date, user.first_name)
    )

    body += '%s\nYou (%s) have been involved in %s post(s) and %s comment(s).\n%s\n\n' % (
      page.name,
      user.first_name,
      results['nr_of_posts'],
      results['nr_of_comments'],
      link
    )

  body += 'Not interested in receiving these emails anymore? You can delete your account here: %s' % (
    EMAIL_DOMAIN + '/settings'
  )

  print body

  mail.send_mail(
    sender=EMAIL_SENDER,
    to="%s <%s>" % (user.name, user.email),
    subject=subject,
    body=body
  )
