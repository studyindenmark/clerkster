from datetime import datetime
from datetime import timedelta
from google.appengine.api import mail


FROM = 'per@youtify.com' # <-- chanage


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
  body = 'email body is coming...'

  print body

  mail.send_mail(
    sender="Clerkster <%s>" % FROM,
    to="%s <%s>" % (user.name, user.email),
    subject=subject,
    body=body
  )
