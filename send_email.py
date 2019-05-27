from __future__ import print_function
import os
import sys
import lib

from googleapiclient.discovery import build
from google.auth.transport.requests import Request

def main():
    from_addr = os.environ.get('GOOGLE_API_MAIL_FROM')
    to_addr   = os.environ.get('GOOGLE_API_MAIL_TO')
    git_tag   = os.environ.get('CIRCLE_TAG')

    creds = lib.load_google_api_credentials_by_environment()

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        creds_string = lib.get_google_api_credentials_string(creds)
        print ("WARN: credentials token refreshed\n\n" + creds_string + "\n")

    if not creds.valid:
        print("ERROR: creds validation error", file=sys.stderr)
        sys.exit(1)

    service = build('gmail', 'v1', credentials=creds)

    subject = u'GOOGLE API mail send test テストサブジェクト (%s)' % git_tag
    content = u'''
GOOGLE API mail send test テスト本文
GOOGLE API mail send test テスト本文
GOOGLE API mail send test テスト本文
'''

    attached_file_path = 'attached-file.txt'
    if os.path.exists(attached_file_path):
        message = lib.create_message_with_attachment(from_addr, to_addr, subject, content, attached_file_path)
    else:
        message = lib.create_message(from_addr, to_addr, subject, content)

    lib.send_message(service, 'me', message)

if __name__ == '__main__':
    main()
