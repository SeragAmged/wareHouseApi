import re


def is_sesa_id_valid(sesa_id: int) -> bool:
    return len(str(sesa_id)) == 12


def is_valid_email(email: str) -> bool:
    # Define the regular expression pattern for a basic email validation
    pattern = r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$'

    # Use re.match to check if the email matches the pattern
    match = re.match(pattern, email)

    return match is not None
