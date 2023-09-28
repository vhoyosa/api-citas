from django.utils.crypto import get_random_string


def generate_token(token_prefix):
    return '{}-{}'.format(
        token_prefix,
        get_random_string(
            length=32 - len(token_prefix) - 1,
            allowed_chars='abcdefghijklmnopqrstuvwxyz0123456789',
        ),
    )