from fastapi import status,HTTPException


class DatabaseConnectionError(Exception):
    """Exception raised when a database connection cannot be established."""

    def __init__(self, message="Database connection is not established"):
        self.message = message
        super().__init__(self.message)


class DatabaseInsertionError(Exception):
    """Exception raised when an error occurs during database insertion."""

    def __init__(self, message="An error occurred while adding the customer to the database"):
        self.message = message
        super().__init__(self.message)


class CustomerValidationError(HTTPException):
    """HTTPException raised due to invalid information."""

    def __init__(
        self,
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="An error occurred due to invalid information.",
    ):
        self.status_code = status_code
        #Check if a custom detail message was provided
        print(detail)
        if detail:
            self.detail = {"errors": detail}
        else:
            self.detail = {"errors": "An error occurred due to invalid information."}
        
        super().__init__(status_code=self.status_code, detail=self.detail)

class CustomerNotFoundError(Exception):
    """Exception raised when the customer is not found"""
    def __init__(self, message="The customer is not found"):
        self.message = message
        super().__init__(self.message)
  
class InvalidLoginError(Exception):
    """Invalid login credentials"""
    def __init__(self, message="An error occurred while login due to Invalid username or password"):
        self.message = message
        super().__init__(self.message)
