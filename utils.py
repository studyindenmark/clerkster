import re


def scan_for_author(message):
  """Scan messages for trailing /MyName"""
  if not message:
    return

  message = message.strip()
  matches = re.findall(r'^.*?\s+\/(.*)\Z', message, re.MULTILINE)

  if matches:
    return matches[-1]
