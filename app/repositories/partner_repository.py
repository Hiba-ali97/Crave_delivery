
from app.core.config import get_db
from app.core.exceptions import DatabaseConnectionError,UserNotFoundError,DatabaseInsertionError, UserValidationError
from app.models.partner import PartnerCreate
import bcrypt
from app.utils.jwt_utils import generate_jwt
import mysql.connector
from mysql.connector import errorcode

mydb=get_db()

def get_partner_id(phone_number:str)->int:
    if mydb is not None:
        db=mydb.cursor()
        # Execute a SQL query to retrieve the partner ID based on the phone number
        sql_query="SELECT id_partner FROM partner WHERE phone_number = %s"
        db.execute(sql_query, (phone_number,))
        row=db.fetchone()
        db.close()
        if row is not None:
            id_partner=row[0]
            return id_partner
        else:
            raise UserNotFoundError()
    else:
        raise DatabaseConnectionError()

def add_partner(partner:PartnerCreate)->str:
    if mydb is not None:
        db=mydb.cursor()
        sql_query="INSERT INTO partner(name, password, phone_number, email) VALUES (%s, %s, %s, %s)"
        name=partner.name
        password=partner.password
        phone_number=partner.phone_number
        email=partner.email
        hashed_password=bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        values=(name,hashed_password,phone_number,email)
        try:
            db.execute(sql_query,values)
            if db.rowcount==0:
                raise DatabaseInsertionError()
            mydb.commit()
            # Get the last customer ID
            id_partner = db.lastrowid
            db.close()
            return generate_jwt(id_partner)
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

        
