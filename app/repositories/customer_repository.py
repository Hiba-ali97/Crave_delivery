from app.utils.jwt_utils import generate_jwt
from app.utils.user_utils import verify_user_name
from ..models.customer import CustomerCreate
from ..core.config import get_db
from ..core.exceptions import  DatabaseConnectionError, DatabaseInsertionError,UserValidationError
import bcrypt
import mysql.connector
from mysql.connector import errorcode

mydb=get_db()
massages=[]
def get_customers()-> list[dict]:

    if mydb is not None:
        print("mydb is not None")
        db = mydb.cursor()
        sql_query="SELECT * FROM customer"
        db.execute(sql_query)
        customers = db.fetchall()
        db.close()
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

        return customer_dicts

    else:
            raise DatabaseConnectionError()



def add_customer(customer: CustomerCreate)->str:
    verify_user_name(customer.name)
    if mydb is not None:
        db = mydb.cursor()
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
            db.execute(sql_query, values)
            if db.rowcount == 0:
                raise DatabaseInsertionError("Failed to add the customer to the database due to a specific error.")
            mydb.commit()
            # Get the last customer ID
            id_customer = db.lastrowid
            db.close()
            return generate_jwt(id_customer)
        except mysql.connector.Error as e:
            # Handle duplicate entry error
            if e.errno == errorcode.ER_DUP_ENTRY:
                raise UserValidationError(detail="The phone number is already registered.")
            else:
                raise DatabaseInsertionError(f"An error occurred: {str(e)}")
        except Exception as e:
            raise DatabaseInsertionError(f"An error occurred: {str(e)}")


    else:
        raise DatabaseConnectionError()

  
