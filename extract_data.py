import re


def extract_phone_numbers_from_email(email_body: str) -> str:
    phone_numbers = re.findall(r'\+?\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}', email_body)
    return f'phone_numbers: {phone_numbers}'


def extract_email_addresses_from_email(email_body: str) -> str:
    email_addresses = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', email_body)
    return f'email: {email_addresses}'