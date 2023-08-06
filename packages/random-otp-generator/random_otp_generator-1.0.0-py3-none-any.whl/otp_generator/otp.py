import secrets
import string

def generate_otp(length):
    if not isinstance(length, int) or length <= 0:
        raise ValueError("Length must be a positive integer.")

    characters = string.ascii_letters + string.digits
    try:
        otp = ''.join(secrets.choice(characters) for _ in range(length))
    except IndexError:
        raise ValueError("Insufficient characters for OTP generation.")

    return otp
