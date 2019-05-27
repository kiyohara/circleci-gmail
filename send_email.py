from __future__ import print_function
import os
import sys
import pickle
import base64
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
import mimetypes
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from apiclient import errors

# https://developers.google.com/gmail/api/guides/sending
def create_message(sender, to, subject, message_text, cset='utf-8'):
    """Create a message for an email.

    Args:
        sender: Email address of the sender.
        to: Email address of the receiver.
        subject: The subject of the email message.
        message_text: The text of the email message.

    Returns:
        An object containing a base64url encoded email object.
    """
    message = MIMEText(message_text, 'plain', cset)
    message['to'] = to
    message['from'] = sender
    message['subject'] = Header(subject, cset)

    # https://thinkami.hatenablog.com/entry/2016/06/10/065731
    message_bytes = message.as_string().encode(encoding=cset)
    message_b64 = base64.urlsafe_b64encode(message_bytes)
    message_b64_str = message_b64.decode(encoding=cset)

    return {'raw': message_b64_str}

# https://developers.google.com/gmail/api/guides/sending
def create_message_with_attachment(sender, to, subject, message_text, file, cset='utf-8'):
    """Create a message for an email.

    Args:
        sender: Email address of the sender.
        to: Email address of the receiver.
        subject: The subject of the email message.
        message_text: The text of the email message.
        file: The path to the file to be attached.

    Returns:
        An object containing a base64url encoded email object.
    """
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = Header(subject, cset)

    msg = MIMEText(message_text)
    message.attach(msg)

    content_type, encoding = mimetypes.guess_type(file)

    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'
    main_type, sub_type = content_type.split('/', 1)
    if main_type == 'text':
        fp = open(file, 'rb')
        content = fp.read()
        msg = MIMEText(content, _subtype=sub_type, _charset=cset)
        fp.close()
    elif main_type == 'image':
        fp = open(file, 'rb')
        msg = MIMEImage(fp.read(), _subtype=sub_type)
        fp.close()
    elif main_type == 'audio':
        fp = open(file, 'rb')
        msg = MIMEAudio(fp.read(), _subtype=sub_type)
        fp.close()
    else:
        fp = open(file, 'rb')
        msg = MIMEBase(main_type, sub_type)
        msg.set_payload(fp.read())
        fp.close()
    filename = os.path.basename(file)
    msg.add_header('Content-Disposition', 'attachment', filename=filename)
    message.attach(msg)

    # https://thinkami.hatenablog.com/entry/2016/06/10/065731
    message_bytes = message.as_string().encode(encoding=cset)
    message_b64 = base64.urlsafe_b64encode(message_bytes)
    message_b64_str = message_b64.decode(encoding=cset)

    return {'raw': message_b64_str}

# https://developers.google.com/gmail/api/guides/sending
def send_message(service, user_id, message):
    """Send an email message.

    Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        message: Message to be sent.

    Returns:
        Sent Message.
    """
    try:
        message = (service.users().messages().send(userId=user_id, body=message)
                .execute())
        print('Message Id: %s' % message['id'])
        return message
    except errors.HttpError as error:
        print('An error occurred: %s' % error)
            
def main():
    from_addr = os.environ.get('GOOGLE_API_MAIL_FROM')
    to_addr   = os.environ.get('GOOGLE_API_MAIL_TO')

    creds_b64 = os.getenv("GOOGLE_API_CREDENTIALS")
    if not creds_b64:
        print("ERROR: GOOGLE_API_CREDENTIALS env required", file=sys.stderr)
        sys.exit(1)

    try:
        creds_pickle = base64.b64decode(creds_b64)
    except Exception as err:
        print("ERROR: invalid env value - base64 decode error(" + str(err) + ")", file=sys.stderr)
        sys.exit(1)

    try:
        creds = pickle.loads(creds_pickle)
    except Exception as err:
        print("ERROR: invalid env value - pickle load error(" + str(err) + ")", file=sys.stderr)
        sys.exit(1)

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())

        creds_pickle = pickle.dumps(creds)
        creds_b64 = base64.b64encode(creds_pickle)
        print ("WARN: credentials token refreshed\n\n" + creds_b64.decode('ascii') + "\n")

    if not creds.valid:
        print("ERROR: creds validation error", file=sys.stderr)
        sys.exit(1)

    service = build('gmail', 'v1', credentials=creds)

    # message = create_message(from_addr, to_addr, u'GOOGLE API mail send test テストサブジェクト', u'GOOGLE API mail send test テスト本文')
    message = create_message_with_attachment(from_addr, to_addr, u'GOOGLE API mail send test テストサブジェクト', u'GOOGLE API mail send test テスト本文', 'attached-file.txt')
    send_message(service, 'me', message)

if __name__ == '__main__':
    main()
