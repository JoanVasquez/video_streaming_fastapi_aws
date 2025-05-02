import base64
import hashlib
import hmac


# Function to generate a secret hash for AWS Cognito authentication 🔑
# Takes username, client ID and client secret as input parameters
def get_secret_hash(username: str, client_id: str, client_secret: str):
    # Concatenate username and client_id to create message
    message = username + client_id

    # Create HMAC SHA256 hash of the message using client_secret as key
    # Encode strings to utf-8 bytes before hashing
    digest = hmac.new(
        client_secret.encode("utf-8"),
        msg=message.encode("utf-8"),
        digestmod=hashlib.sha256,
    ).digest()

    # Decode the base64 hash and return as string
    return base64.b64encode(digest).decode()
