import jwt
from datetime import datetime, timedelta
import secrets

# Secret key for JWT signing and verification
SECRET_KEY = secrets.token_hex(32)


def generate_jwt(user_id: int) -> str:
    # Define the payload containing the data you want to include in the JWT
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=24)  # Set the expiration time
    }

    # Generate the JWT
    jwt_token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    return jwt_token


def is_valid_token(jwt_token: str) -> bool:
    try:
        decoded_token = jwt.decode(jwt_token, SECRET_KEY, algorithms=["HS256"])
        
        # Get the expiration time from the decoded token
        expiration_time = datetime.fromtimestamp(decoded_token["exp"])
        
        # Check if the token has expired
        if expiration_time < datetime.utcnow():
            return False
                
        return True
    
    except jwt.ExpiredSignatureError:
        # Handle the case when the token has expired
        return False
    
    except (jwt.InvalidTokenError, jwt.DecodeError):
        # Handle the case when the token is invalid or cannot be decoded
        return False

