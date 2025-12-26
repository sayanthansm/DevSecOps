import random
import string

def generate_aws_like_key():
    """
    Generates a fake AWS-style access key (AKIA + 16 chars)
    Used for HIGH-risk test cases
    """
    return "AKIA" + "".join(
        random.choices(string.ascii_uppercase + string.digits, k=16)
    )

def generate_generic_api_key(length=24):
    """
    Generates a generic API key
    Used for MEDIUM-risk test cases
    """
    return "".join(
        random.choices(string.ascii_letters + string.digits, k=length)
    )

if __name__ == "__main__":
    print("AWS-like Key     :", generate_aws_like_key())
    print("Generic API Key :", generate_generic_api_key())
