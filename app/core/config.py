from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .exceptions import DatabaseConnectionError
import mysql.connector
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:@localhost/crave_delivery"

# Create the database engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the base model for SQLAlchemy models
Base = declarative_base()


def get_db():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="crave_delivery",
            # pool_size=10 
        )
        return mydb
    except mysql.connector.Error as error:
        raise DatabaseConnectionError()

