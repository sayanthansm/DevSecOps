from key_generator import generate_aws_like_key, generate_generic_api_key

# Toggle test case here
TEST_CASE = "HIGH"   # change to "MEDIUM"

if TEST_CASE == "HIGH":
    API_KEY = generate_aws_like_key()
else:
    API_KEY = generate_generic_api_key()

def main():
    print("Demo app running")
    print("Using API Key:", API_KEY)

if __name__ == "__main__":
    main()
