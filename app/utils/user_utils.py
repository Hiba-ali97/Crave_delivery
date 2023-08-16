from app.core.config import get_db
from app.core.exceptions import DatabaseConnectionError, UserNotFoundError,UserValidationError,InvalidUserTypeError
from app.models.customer import Customer
from app.models.partner import Partner
import bcrypt
from geopy.geocoders import Nominatim
import re
# Dictionary to store user types and their corresponding classes
USER_TYPES = {
    "customer": Customer,
    "partner": Partner,
    # Add more user types and classes as needed
}

def check_user_type(user_type:str)->str:
    user_class = USER_TYPES.get(user_type)
    if not user_class:
        raise InvalidUserTypeError()
    table_name = user_class.__name__
    return table_name
    
def register(user_type, user_data):
    """
    Register a user of the given user_type with the provided user_data.
    
    Parameters:
        user_type (str): The type of user (e.g., "customer", "partner").
        user_data (dict): A dictionary containing user data specific to the user type.
        
    Returns:
        instance of the registered user (Customer or Partner).
    """
    user_class = USER_TYPES.get(user_type)
    if not user_class:
        raise InvalidUserTypeError()
    
    # Create an instance of the appropriate user class and validate the user_data
    user_instance = user_class(**user_data)
    return user_instance



def validate_credentials(phone_number: str, password: str,user_type:str) ->bool:
    # Retrieve the hashed password from the database based on the username
    try:
        hashed_password = get_hashed_password(phone_number,user_type)  
        encoded_password = password.encode()
        # Ensure that hashed_password is encoded as bytes-like object
        if isinstance(hashed_password, str):
            hashed_password = hashed_password.encode()
        # Verify the provided password against the hashed password
        return bcrypt.checkpw(encoded_password, hashed_password)
    except UserNotFoundError:
        # Handle the case when the user is not found
        raise UserNotFoundError()
    except DatabaseConnectionError:
        # Handle the case when the database connection is not established
        raise DatabaseConnectionError()
    except InvalidUserTypeError :
        # Handle other exceptions gracefully (optional)
        raise InvalidUserTypeError()

   


def get_hashed_password(phone_number: str,user_type:str) -> bytes:

        table_name = check_user_type(user_type)
        if table_name is None:
            raise Exception
        print(table_name)
        mydb = get_db()
        if mydb is not None:
            db = mydb.cursor()
            sql_query = f"SELECT password FROM {table_name} WHERE phone_number = %s"
            db.execute(sql_query, (phone_number,))
            
            # Fetch the first row from the result set
            row = db.fetchone()
            db.close()
            # assert row, 'The customer is not found'
            if row is not None:
                # Extract the hashed password from the row
                hashed_password = row[0]
                return hashed_password
            
            else:
                # the username is not found
                raise UserNotFoundError()
        
        else:
            #the database connection is not established
            raise DatabaseConnectionError()

def get_user_id(phone_number: str,user_type:str) -> int:
    try:
        table_name = check_user_type(user_type)
        if table_name is None:
            raise ValueError(f"Invalid user_type '{user_type}'")
        mydb = get_db()
        if mydb is not None:
            db = mydb.cursor()
            # Get the ID column name based on the user type
            id_column_name = f"id_{table_name}"
            # Execute a SQL query to retrieve the customer ID based on the phone number
            sql_query =f"SELECT {id_column_name} FROM {table_name} WHERE phone_number = %s"
            db.execute(sql_query, (phone_number,))
            
            # Fetch the first row from the result set
            row = db.fetchone()
            db.close()
            
            if row is not None:
                # Extract the customer ID from the row
                customer_id = row[0]
                return customer_id
            else:
                # Handle the case when the customer does not exist
                raise UserNotFoundError()
        
        else:
            # Handle the case when the database connection is not established
            raise DatabaseConnectionError()
    except ValueError:
        raise ValueError

def verify_location_country(lat: float, lng: float, country_code: str) -> bool:
    #Verify if the location is in the specified country
    geolocator = Nominatim(user_agent="YourApp")
    location = geolocator.reverse((lat, lng), exactly_one=True)

    if location and location.raw.get("address", {}).get("country_code") == country_code:
        return True
    raise UserValidationError(detail="This sevice is not available in your country")


def verify_user_name(name:str)->bool:
    # - Name must be at least 3 characters long
    if len(name) >= 3:
        return True
    raise UserValidationError(detail="Name must be at least 3 characters long")


def verify_phone_number(phone_number:str)-> bool:
    # - Phone number must be a 10-digit number
    if len(str(phone_number)) == 10 :
        number_pattern=r"^[0-9]+$"
        if re.match(number_pattern,phone_number):
            return True
    raise UserValidationError(detail="Phone number must be a 10-digit number")

def verify_email(email: str) -> bool:
    # Use regular expression to validate email format
    email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if re.match(email_pattern, email):
        return True
    raise UserValidationError(detail="Invalid email format")
 

def verify_password(password:str)->bool:
    # - Password must have at least 8 characters
    if len(password) >= 8:
        return True
    raise UserValidationError(detail="Password must have at least 8 characters")

def verify_location(location_lat:float,location_lng:float)->bool:
    # - Location latitude must be between -90 and 90
    # - Location longitude must be between -180 and 180
    if ( -90 <= location_lat <= 90
        and -180 <= location_lng <= 180):
        return True
    return UserValidationError(detail="Location is not correct")




        # if len(customer_info.name) < 3:
        #     massages.append("Name must be at least 3 characters long")
        # if len(str(customer_info.phone_number)) != 10:
        #     massages.append("Phone number must be a 10-digit number")
        # if len(customer_info.password) < 8:
        #     massages.append("Password must have at least 8 characters")
        # if not verify_location_country(customer_info.location_lat, customer_info.location_lng, "AE"):
        #     massage.append("Location should be in the UAE")
