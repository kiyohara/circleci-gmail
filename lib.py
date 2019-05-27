import os
import sys
import base64
import pickle

from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
import mimetypes
from apiclient import errors

def get_google_api_credentials_string(creds):
    creds_pickle = pickle.dumps(creds)
    creds_b64 = base64.b64encode(creds_pickle)
    creds_string = creds_b64.decode('ascii')

    return creds_string

def load_google_api_credentials_by_string(creds_string):
    try:
        creds_pickle = base64.b64decode(creds_string)
    except Exception as err:
        print("ERROR: invalid env value - base64 decode error(" + str(err) + ")", file=sys.stderr)
        sys.exit(1)

    try:
        creds = pickle.loads(creds_pickle)
    except Exception as err:
        print("ERROR: invalid env value - pickle load error(" + str(err) + ")", file=sys.stderr)
        sys.exit(1)

    return creds

def load_google_api_credentials_by_environment():
    creds_string = os.getenv("GOOGLE_API_CREDENTIALS")
    if not creds_string:
        print("ERROR: GOOGLE_API_CREDENTIALS env required", file=sys.stderr)
        sys.exit(1)

    return load_google_api_credentials_by_string(creds_string)

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
