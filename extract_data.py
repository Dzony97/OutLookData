import re


def extract_phone_numbers(email_body: str) -> list[...]:
    phone_pattern = re.compile(
        r'(?:\+48\s?)?\d{3}(?:[\s-]?\d{3}){2}'
    )
    phone_numbers = re.findall(phone_pattern, email_body)
    return phone_numbers


def extract_email_addresses(email_body: str) -> list[...]:
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    email_addresses = re.findall(email_pattern, email_body)
    return email_addresses


def extract_amount_of_money(email_body: str) -> list[...]:
    money_pattern = re.compile(
        r'\b'
        r'(?:'
        r'(?:USD|EUR|PLN|GBP|JPY|CHF|CZK|EURO)\s?\d{1,3}(?:[ ,.]\d{3})*(?:[.,]\d{1,2})?'
        r'|'
        r'\d{1,3}(?:[ ,.]\d{3})*(?:[.,]\d{1,2})?\s?(?:USD|EUR|PLN|GBP|JPY|CHF|CZK|EURO)'
        r')'
        r'\b',
        re.IGNORECASE
    )
    amount_of_money = money_pattern.findall(email_body)
    return amount_of_money


def extract_date(email_body: str) -> list[...]:
    date_pattern = r'\b\d{2}[./-]\d{2}[./-]\d{4}\b'
    date = re.findall(date_pattern, email_body)
    return date
