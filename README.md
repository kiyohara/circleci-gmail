1. Open Google APIs Console
    - [https://console.developers.google.com/apis/dashboard](https://console.developers.google.com/apis/dashboard)

2. Create project

3. Open credentials view via side menu

4. Create "OAuth client ID"
    - web application

5. Download credentials JSON file by ID list
    - save as `credentials.json`

6. Put `credentials.json` this directory

7. `$ pipenv install`

8. `$ pipenv run python get_creds_base64.py`

9. Save printed base64 string to `GOOGLE_API_CREDENTIALS` environment

10. Set environment below
    - `GOOGLE_API_MAIL_TO`
    - `GOOGLE_API_MAIL_FROM`

11. Test run `$ pipenv run python send_mail.py`

12. Set environments to CircleCI env

13. Push branch to Github (-> CircleCI do nothing)

14. Push TAG to Github (-> CircleCI exec `send_mail.py`)

