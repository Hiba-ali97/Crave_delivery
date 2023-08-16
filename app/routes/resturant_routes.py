from fastapi import APIRouter,status,HTTPException
from app.models.resturant import RestaurantCreate
from fastapi.responses import JSONResponse
from app.repositories.resturant_repository import get_all_restaurants,add_restaurant
from app.core.exceptions import DatabaseConnectionError,DatabaseInsertionError,UserNotFoundError
router=APIRouter()
@router.get("/restaurants")
def show_restaurants():
    """
    This method will:
    return all restaurants
    """
    try:
        resturents=get_all_restaurants()
        # restaurant_models=[RestaurantCreate(**restaurant) for restaurant in resturents]
        if len(resturents)>0:
            response={"status":"success","data":resturents} 
            return JSONResponse(content=response,status_code=status.HTTP_200_OK)
        else:
            response={"status":"success","data":"No restaurants avilable"} 
            return JSONResponse(content=response,status_code=status.HTTP_200_OK)
    except DatabaseConnectionError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/restaurant/create")
def create_restaurant(restaurant:RestaurantCreate,partner_number:int):
    """
    This method will:
    1-Retrieve the resturant information:name , info ,id_partner(optional) and the partner phone number
    2-Add the resturant to database 
    """
    try:
        add_restaurant(restaurant,partner_number)
        response= {"status":"success","data": "Restaurant created successfully"}
        return JSONResponse(content=response,status_code=status.HTTP_200_OK)
    except DatabaseInsertionError as e :
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except DatabaseConnectionError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )