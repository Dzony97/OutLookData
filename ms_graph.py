import os
import webbrowser
import msal
from dotenv import load_dotenv

MS_GRAPH_BASE_URL = 'https://graph.microsoft.com/v1.0/'


def get_access_token(application_id: str, client_secret: str, scopes: list[str], email: str) -> str:
    client = msal.ConfidentialClientApplication(
        client_id=application_id,
        client_credential=client_secret,
        authority='https://login.microsoftonline.com/consumers/'
    )

    refresh_token_file = f'refresh_token_{email}.txt'

    refresh_token = None
    if os.path.exists(refresh_token_file):
        with open(refresh_token_file, 'r') as file:
            refresh_token = file.read().strip()

    if refresh_token:
        token_response = client.acquire_token_by_refresh_token(refresh_token, scopes=scopes)
    else:
        auth_request_url = client.get_authorization_request_url(scopes)
        webbrowser.open(auth_request_url)
        authorization_code = input('Enter authorization code: ')

        if not authorization_code:
            raise ValueError('Authorization code is empty')

        token_response = client.acquire_token_by_authorization_code(
            code=authorization_code,
            scopes=scopes
        )

    if 'access_token' in token_response:
        if 'refresh_token' in token_response:
            with open(refresh_token_file, 'w') as file:
                file.write(token_response['refresh_token'])

        return token_response['access_token']
    else:
        raise Exception('Failed to acquire token' + str(token_response))


def main() -> None:
    load_dotenv()
    APPLICATION_ID = os.getenv('APPLICATION_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')
    SCOPES = ['User.Read', 'Mail.ReadWrite']
    EMAIL = os.getenv('EMAIL')

    try:
        access_token = get_access_token(application_id=APPLICATION_ID, client_secret=CLIENT_SECRET, scopes=SCOPES,
                                        email=EMAIL)
        headers = {
            'Authorization': 'Bearer ' + access_token
        }
        print(headers)
    except Exception as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    main()