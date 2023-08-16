from app.core.exceptions import InvalidLoginError,UserNotFoundError,DatabaseConnectionError,InvalidUserTypeError
from app.models.user import LoginCredentials
from app.utils.jwt_utils import generate_jwt
from app.utils.user_utils import validate_credentials,get_user_id

def login(user: LoginCredentials,user_type:str)->str:
    # Retrieve the login credentials from the customer object
    username = user.phone_number
    password = user.password
    try:
        if validate_credentials(username, password,user_type) is True:
            user_id = get_user_id(username,user_type)
            jwt_token = generate_jwt(user_id)         
            return jwt_token
        elif validate_credentials(username, password,user_type) is False:
            raise InvalidLoginError()
    except UserNotFoundError:
        raise UserNotFoundError()
    except DatabaseConnectionError:
        raise DatabaseConnectionError()
    except InvalidUserTypeError :
        raise InvalidUserTypeError()

