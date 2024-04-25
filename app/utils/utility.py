import re


class Util:
    @classmethod
    def is_valid_email(cls, email:str) -> bool:
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return bool(re.match(email_regex, email))