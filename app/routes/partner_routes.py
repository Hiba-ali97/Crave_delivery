from fastapi import APIRouter,status,HTTPException
from app.utils.user_utils import verify_user_name,verify_password,verify_phone_number,verify_email
from app.models.partner import PartnerCreate
from app.core.exceptions import UserValidationError,DatabaseInsertionError,DatabaseConnectionError
from app.repositories.partner_repository import add_partner
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/partner/register")
def register_partner(partner:PartnerCreate):
    """
    This method will:
    Register a new partner
    """
    try:
        verify_user_name(partner.name)
        verify_phone_number(partner.phone_number)
        verify_password(partner.password)
        verify_email(partner.email)
        try:
            add_partner(partner)
            response= {"status":"success","data": "Partner registered successfully"}
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
    except UserValidationError as e :
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=e.detail,
            )
    