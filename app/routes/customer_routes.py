from fastapi import APIRouter,status,HTTPException,Depends
from sqlalchemy.orm import Session
from app.core.exceptions import InvalidLoginError,CustomerNotFoundError,DatabaseInsertionError,CustomerValidationError
from app.core.security import login
from app.models.customer import LoginCredentials, CustomerCreate
from fastapi.encoders import jsonable_encoder
from app.repositories.customer_repository import add_customer, get_customers,verify_customer_info
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/customers")
def show_customers():
    """
    This method will:
    return all customers
    """
    customers=get_customers()
    customer_models = [CustomerCreate(**customer) for customer in customers]
    if customers:
        response={"status":"success","data":customer_models}
        return jsonable_encoder(response) 
    else:
        response={"status":"success","data":" "}
        return jsonable_encoder(response, indent=4)



@router.post("/customers/register",response_model=dict)
def register_customer(customer: CustomerCreate):
    """
    This method will:
    Register a new customer
    """
    try:
        verify_customer_info(customer)
        try:
            add_customer(customer)
            response= {"status":"success","data": "Customer created successfully"}
            return jsonable_encoder(response)
        except DatabaseInsertionError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e),
            )
        except CustomerValidationError as e:
            raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=e.detail,
                )
    except CustomerValidationError as e:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=e.detail,
            )


@router.post("/customers/login")
def login_customer(customer: LoginCredentials):
    """
    This method will:
    -Retrieve the login credentials from the customer object
    -Validate the login credentials
    -Return the generate JWT token
    """
    try:
        jwt_token = login(customer)
        response = {
            "status": "success",
            "data": {
                "jwt_token": jwt_token
            }
        }
        return JSONResponse(content=response, status_code=status.HTTP_200_OK)
    except InvalidLoginError:
        response = {
            "status": "error",
            "message": "Invalid login credentials"
        }
        return JSONResponse(content=response, status_code=status.HTTP_401_UNAUTHORIZED)
    except CustomerNotFoundError:
        response = {
            "status": "error",
            "message": "Customer not found"
        }
        return JSONResponse(content=response, status_code=status.HTTP_404_NOT_FOUND)






