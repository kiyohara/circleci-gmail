from __future__ import print_function
import sys
import lib

def main():
    creds = lib.load_google_api_credentials_by_environment()

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

