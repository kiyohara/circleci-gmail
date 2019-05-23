from __future__ import print_function
import pickle
import base64

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def main():
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server()
    creds_pickle = pickle.dumps(creds)
    creds_b64 = base64.b64encode(creds_pickle)

    print ("--> success\n\n" + creds_b64.decode('ascii') + "\n")

if __name__ == '__main__':
    main()

