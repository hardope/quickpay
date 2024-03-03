from rest_framework_simplejwt.tokens import AccessToken
from datetime import datetime
from jwt import decode, ExpiredSignatureError
from django.conf import settings

def parse_token(token):

    secret_key = settings.SECRET_KEY

    return {
        'access': {
            'token': token['access'],
            'expiration_date': get_token_expiration_seconds(token['access'], secret_key)
        },
        'refresh': {
            'token': token['refresh'],
            'expiration_date': get_token_expiration_seconds(token['refresh'], secret_key)
        }
    }

    
def get_token_expiration_seconds(token, secret_key):
    try:
        # Decode the token
        decoded_token = decode(token, secret_key, algorithms=['HS256'])

        # Extract expiration timestamp from the decoded token
        expiration_timestamp = decoded_token['exp']

        # Calculate the time remaining in seconds
        current_timestamp = datetime.utcnow().timestamp()
        seconds_remaining = int(expiration_timestamp - current_timestamp)

        return seconds_remaining

    except ExpiredSignatureError:
        print("Token has already expired.")
        return 0

    except Exception as e:
        print(f"Error decoding token: {e}")
        return None
