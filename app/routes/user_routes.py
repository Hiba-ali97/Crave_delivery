from fastapi import APIRouter,status,HTTPException
from app.core.exceptions import InvalidLoginError,UserNotFoundError,DatabaseInsertionError,UserValidationError,DatabaseConnectionError,InvalidUserTypeError
from app.models.user import LoginCredentials
from app.core.security import login
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/user/login")
def login_customer(user: LoginCredentials,user_type:str):
    """
    This method will:
    -Retrieve the login credentials from the customer object
    -Validate the login credentials
    -Return the generate JWT token
    """
    try:
        jwt_token = login(user,user_type)
        response = {
            "status": "success",
            "data": {
                "message":"Logged in",
                "jwt_token": jwt_token
            }
        }
        return JSONResponse(content=response, status_code=status.HTTP_200_OK)
    except InvalidLoginError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except InvalidUserTypeError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
