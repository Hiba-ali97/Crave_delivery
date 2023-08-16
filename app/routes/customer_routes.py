from fastapi import APIRouter,status,HTTPException
from app.core.exceptions import DatabaseInsertionError,UserValidationError,DatabaseConnectionError
from app.models.customer import CustomerCreate
from app.repositories.customer_repository import add_customer, get_customers
from fastapi.responses import JSONResponse
from app.utils.user_utils import verify_user_name,verify_phone_number,verify_password,verify_location
router = APIRouter()

@router.get("/customers")
def show_customers():
    """
    This method will:
    return all customers
    """
    try:
        customers=get_customers()
        #customer_models = [CustomerCreate(**customer) for customer in customers]
        if customers:
            response={"status":"success","data":customers}
            return JSONResponse(content=response, status_code=status.HTTP_200_OK)
        else:
            response={"status":"success","data":"No Customers"}
            return JSONResponse(content=response,status_code=status.HTTP_200_OK)
    except DatabaseConnectionError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/customers/register",response_model=dict)
def register_customer(customer: CustomerCreate):
    """
    This method will:
    Register a new customer
    """
    try:
        verify_user_name(customer.name)
        verify_phone_number(customer.phone_number)
        verify_password(customer.password)
        verify_location(customer.location_lat,customer.location_lng)
        try:
            add_customer(customer)
            response= {"status":"success","data": "Customer registered successfully"}
            return JSONResponse(content=response,status_code=status.HTTP_200_OK)
        except DatabaseConnectionError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )
        except DatabaseInsertionError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e),
            )
        except UserValidationError as e:
            raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=e.detail,
                )
    except UserValidationError as e:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=e.detail,
            )






