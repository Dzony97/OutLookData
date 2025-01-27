import os
from dotenv import load_dotenv
import httpx
from ms_graph import get_access_token
from outlook import search_folders, get_sub_folders, get_messages


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

        folder_name = 'TEST'
        target_folder = search_folders(headers, folder_name)
        folder_id = target_folder['id']

        messages = get_messages(headers, folder_id)

        for message in messages:
            print('Subject:', message['subject'])
            print('-' * 50)

        sub_folders = get_sub_folders(headers, folder_id)
        for sub_folder in sub_folders:
            if sub_folder['displayName'].lower() == 'sub folder':
                sub_folder_id = sub_folder['id']
                messages = get_messages(headers, sub_folder_id)
                for message in messages:
                    print('Subject:', message['subject'])
                    print('-' * 50)


    except httpx.HTTPStatusError as e:
        print(f'HTTP Error: {e}')
    except Exception as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    main()
