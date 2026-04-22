import string
import random


def generate_code(n: int = 8) -> str:
    return "".join(
        random.choices(
            string.ascii_uppercase + string.ascii_lowercase + string.digits, k=n
        )
    )
