from app.utils.jwt_utils import generate_jwt
from ..models.customer import CustomerCreate
from ..core.config import get_db
from ..core.exceptions import CustomerNotFoundError, DatabaseConnectionError, DatabaseInsertionError,CustomerValidationError
from geopy.geocoders import Nominatim
import bcrypt
import mysql.connector
from mysql.connector import errorcode
def get_customers()-> list[dict]:

    mydb=get_db()
    if mydb is not None:
        print("mydb is not None")
        dp = mydb.cursor()
        sql_query="SELECT * FROM customer"
        dp.execute(sql_query)
        customers = dp.fetchall()
        dp.close()
        # Convert the fetched data to a list of dictionaries
        customer_dicts = []
        for customer in customers:
            customer_dict = {
                # "id_customer": customer[0],
                "id_credit": customer[1],
                "name": customer[2],
                "password": customer[3],
                "phone_number": customer[4],
                "vip": customer[5],
                "location_lat": float(customer[6]),
                "location_lng": float(customer[7]),
                "location_address": customer[8]
            }
            customer_dicts.append(customer_dict)
            print(f"{customer[0]} , ")


        return customer_dicts

    else:
        print("Database connection is not established")
        return[]



def add_customer(customer: CustomerCreate):

    mydb=get_db()
    if mydb is not None:
        dp = mydb.cursor()
        id_credit = customer.id_credit
        name = customer.name
        password = customer.password
        phone_number = customer.phone_number
        vip = customer.vip
        location_lat = customer.location_lat
        location_lng = customer.location_lng
        location_address = customer.location_address

        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        sql_query="INSERT INTO Customer (id_credit, name, password, phone_number, vip, location_lat,location_lng,location_address) VALUES (%s, %s, %s,%s, %s, %s,%s, %s)"
        values =  (id_credit, name, hashed_password, phone_number, vip, location_lat,location_lng,location_address)
        try:
            dp.execute(sql_query, values)
            if dp.rowcount == 0:
                raise DatabaseInsertionError("Failed to add the customer to the database due to a specific error.")
            mydb.commit()
            # Get the last customer ID
            id_customer = dp.lastrowid
            dp.close()
            return generate_jwt(id_customer)
        except mysql.connector.Error as e:
            # Handle duplicate entry error
            if e.errno == errorcode.ER_DUP_ENTRY:
                raise CustomerValidationError(detail="The phone number is already registered.")
            else:
                raise DatabaseInsertionError(f"An error occurred: {str(e)}")
        except Exception as e:
            raise DatabaseInsertionError(f"An error occurred: {str(e)}")


    else:
        raise DatabaseConnectionError()


def get_customer_id(username: str) -> int:
    mydb = get_db()
    if mydb is not None:
        dp = mydb.cursor()

        # Execute a SQL query to retrieve the customer ID based on the phone number
        sql_query = "SELECT id_customer FROM Customer WHERE phone_number = %s"
        dp.execute(sql_query, (username,))
        
        # Fetch the first row from the result set
        row = dp.fetchone()
        dp.close()
        
        if row is not None:
            # Extract the customer ID from the row
            customer_id = row[0]
            return customer_id
        else:
            # Handle the case when the customer does not exist
            raise CustomerNotFoundError()
    
    else:
        # Handle the case when the database connection is not established
        raise DatabaseConnectionError()


def get_hashed_password(username: str) -> bytes:
    # Replace this code with your database retrieval logic
    mydb = get_db()
    if mydb is not None:
        dp = mydb.cursor()
        sql_query = "SELECT password FROM Customer WHERE phone_number = %s"
        dp.execute(sql_query, (username,))
        
        # Fetch the first row from the result set
        row = dp.fetchone()
        dp.close()
        # assert row, 'The customer is not found'
        if row is not None:
            # Extract the hashed password from the row
            hashed_password = row[0]
            return hashed_password
        
        else:
            # the username is not found
            raise CustomerNotFoundError()
    
    else:
        #the database connection is not established
        raise DatabaseConnectionError("Database connection is not established")


    

def verify_customer_info(customer_info: CustomerCreate) -> bool:
    
    # Verify customer information
    # - Name must be at least 3 characters long
    # - Phone number must be a 10-digit number
    # - Password must have at least 8 characters
    # - VIP must be either 0 or 1
    # - Location latitude must be between -90 and 90
    # - Location longitude must be between -180 and 180
    # - Location should be in the UAE
    massages=[]
    if (
        len(customer_info.name) >= 3
        and len(str(customer_info.phone_number)) == 10
        and len(customer_info.password) >= 8
        and -90 <= customer_info.location_lat <= 90
        and -180 <= customer_info.location_lng <= 180
        # and verify_location_country(customer_info.location_lat, customer_info.location_lng, "AE")
    ):
        return True

    else:
        if len(customer_info.name) < 3:
            massages.append("Name must be at least 3 characters long")
        if len(str(customer_info.phone_number)) != 10:
            massages.append("Phone number must be a 10-digit number")
        if len(customer_info.password) < 8:
            massages.append("Password must have at least 8 characters")
        # if not verify_location_country(customer_info.location_lat, customer_info.location_lng, "AE"):
        #     massage.append("Location should be in the UAE")

        if massages:
         raise CustomerValidationError(
            detail= massages
         )

        return True


def verify_location_country(lat: float, lng: float, country_code: str) -> bool:
    """
    Verify if the location is in the specified country
    """
    geolocator = Nominatim(user_agent="YourApp")
    location = geolocator.reverse((lat, lng), exactly_one=True)

    if location and location.raw.get("address", {}).get("country_code") == country_code:
        return True
    else:
        return False

def validate_credentials(username: str, password: str) -> bool:
    # Retrieve the hashed password from the database based on the username
    hashed_password = get_hashed_password(username)  
    encoded_password = password.encode()
    # Ensure that hashed_password is encoded as bytes-like object
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode()

    # Verify the provided password against the hashed password
    return bcrypt.checkpw(encoded_password, hashed_password)