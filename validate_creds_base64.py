from __future__ import print_function
import os
import sys
import pickle
import base64
from googleapiclient.discovery import build

def main():
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

    if creds.expired:
        print("ERROR: creds token expired", file=sys.stderr)
        sys.exit(1)

    if not creds.valid:
        print("ERROR: creds validation error", file=sys.stderr)
        sys.exit(1)

    print("OK: valid credentials", file=sys.stderr)
    sys.exit(0)

if __name__ == '__main__':
    main()

