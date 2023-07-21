from app.core.exceptions import InvalidLoginError
from app.repositories.customer_repository import get_customer_id,validate_credentials
from app.models.customer import LoginCredentials
from app.utils.jwt_utils import generate_jwt

def login(customer: LoginCredentials):
    # Retrieve the login credentials from the customer object
    username = customer.phone_number
    password = customer.password
    
    # Validate the login credentials
    if validate_credentials(username, password):
        # Perform login logic and generate JWT token
        customer_id = get_customer_id(username)
        jwt_token = generate_jwt(customer_id)
        
        return jwt_token
    else:
        # Handle invalid login credentials
        raise InvalidLoginError()
