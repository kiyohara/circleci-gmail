from __future__ import print_function
import lib
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def main():
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server()

    creds_string = lib.get_google_api_credentials_string(creds)

    print ("--> success\n\n" + creds_string + "\n")

if __name__ == '__main__':
    main()
