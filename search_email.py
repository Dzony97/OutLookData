import os
from dotenv import load_dotenv
import httpx
from ms_graph import get_access_token

import os
from dotenv import load_dotenv
import httpx
from ms_graph import get_access_token
from outlook import search_messages
from extract_data import (
    extract_email_addresses,
    extract_phone_numbers,
    extract_date,
    extract_amount_of_money
)
from openpyxl import Workbook


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

        search_query = ['Temat', 'Czesc', 'Patryk']

        wb = Workbook()
        ws = wb.active

        ws.append([
            "Subject",
            "From Name",
            "From Email",
            "Received DateTime",
            "Extracted Emails",
            "Extracted Phones",
            "Extracted Dates",
            "Extracted Amounts"
        ])

        for query in search_query:
            messages = search_messages(headers, query)

            for mail_message in messages:
                subject = mail_message['subject']
                from_name = mail_message['from']['emailAddress']['name']
                from_email = mail_message['from']['emailAddress']['address']
                received_datetime = mail_message['receivedDateTime']
                body_preview = mail_message['bodyPreview']

                emails = extract_email_addresses(body_preview)
                phones = extract_phone_numbers(body_preview)
                dates = extract_date(body_preview)
                amounts = extract_amount_of_money(body_preview)

                # Zamieniamy listy na łańcuchy tekstowe (dla czytelności w Excelu)
                emails_str = ", ".join(emails) if emails else ""
                phones_str = ", ".join(phones) if phones else ""
                dates_str = ", ".join(dates) if dates else ""
                amounts_str = ", ".join(amounts) if amounts else ""

                # Wpisujemy dane do nowego wiersza w arkuszu
                ws.append([
                    subject,
                    from_name,
                    from_email,
                    received_datetime,
                    emails_str,
                    phones_str,
                    dates_str,
                    amounts_str
                ])

        excel_filename = "extracted_data.xlsx"
        wb.save(excel_filename)

    except httpx.HTTPStatusError as e:
        print(f'HTTP Error: {e}')
    except Exception as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    main()