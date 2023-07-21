#!/Users/hiba/Documents/python/python apis/Crave_delivery/env/bin/python
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.routes.customer_routes import router as customer_router

app = FastAPI()


@app.get("/")
def index():

    """
    DEFAULT ROUTE
    This method will
    1. Provide usage instructions formatted as JSON
    """
    response = {"usage" : "Crave Delivery"}
    return JSONResponse(response.dict(),indent=4)

app.include_router(customer_router)