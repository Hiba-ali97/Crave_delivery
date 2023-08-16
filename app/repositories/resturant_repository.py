from app.core.config import get_db
from app.core.exceptions import DatabaseConnectionError,DatabaseInsertionError,UserNotFoundError
from app.models.resturant import RestaurantCreate
from app.repositories.partner_repository import get_partner_id
import mysql.connector

mydb=get_db()

def get_all_restaurants()->list[dict]:
    

    if(mydb is not None):
        db=mydb.cursor()
        sql_query="SELECT * FROM resturant"

        db.execute(sql_query)
        restaurants=db.fetchall()
        db.close()
        # Convert the fetched data to a list of dictionaries
        restaurant_dicts=[]
        for restaurant in restaurants:
            restaurant_dict={
                "name":restaurant[1],
                "info":restaurant[2],
                "id_partner":restaurant[3]
            }
            restaurant_dicts.append(restaurant_dict)
        return restaurant_dicts


    else:
        raise DatabaseConnectionError()


def add_restaurant(restaurant:RestaurantCreate, phone_number:str):
    if mydb is not None:
        db=mydb.cursor()
        name=restaurant.name
        info=restaurant.info
        print(restaurant.id_partner)
        if restaurant.id_partner == 0:
            try:
                id_partner=get_partner_id(phone_number)
            except UserNotFoundError :
                raise UserNotFoundError()
        else:
            id_partner=restaurant.id_partner
        sql_query="INSERT INTO Resturant(name, info, id_partner) VALUES (%s, %s, %s)"
        values=(name, info, id_partner)
        try:
            db.execute(sql_query,values)
            if db.rowcount == 0:
                raise DatabaseInsertionError()
            mydb.commit()
            db.close()
            return 
        except mysql.connector.Error :
            raise DatabaseInsertionError()
    else:
        raise DatabaseConnectionError()