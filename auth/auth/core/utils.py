import string
from secrets import choice as secrets_choice


def generate_random_string():
    alphabet = string.ascii_letters + string.digits
    result = "".join(secrets_choice(alphabet) for _ in range(16))
    return result
