import os
from dotenv import load_dotenv
import httpx
from ms_graph import get_access_token
from outlook import search_messages
from extract_data import extract_email_addresses_from_email, extract_phone_numbers_from_email


def main():
    load_dotenv()
    APPLICATION_ID = os.getenv('APPLICATION_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')
    SCOPES = ['User.Read', 'Mail.ReadWrite']
    EMAIL = os.getenv('EMAIL')

    try:
        access_token = get_access_token(
            application_id=APPLICATION_ID,
            client_secret=CLIENT_SECRET,
            scopes=SCOPES,
            email=EMAIL
        )
        headers = {
            'Authorization': 'Bearer ' + access_token
        }
        search_query = 'Temat'
        messages = search_messages(headers, search_query)

        for index, mail_message in enumerate(messages):
            print('Subject:', mail_message['subject'])
            print('From:', mail_message['from']['emailAddress']['name'],
                  f"({mail_message['from']['emailAddress']['address']})")
            print('Received Data Time:', mail_message['receivedDateTime'])
            print('Body preview:', mail_message['bodyPreview'])

            print('===========================================')
            print(extract_email_addresses_from_email(mail_message['bodyPreview']))
            print(extract_phone_numbers_from_email(mail_message['bodyPreview']))
            print('===========================================')

    except httpx.HTTPStatusError as e:
        print(f'HTTP Error: {e}')
    except Exception as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    main()