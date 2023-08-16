#!/Users/hiba/Documents/python/python apis/Crave_delivery/env/bin/python
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.routes.customer_routes import router as customer_router
from app.routes.resturant_routes import router as restaurant_router
from app.routes.partner_routes import router as partner_router
from app.routes.user_routes import router as user_router
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
app.include_router(restaurant_router)
app.include_router(partner_router)
app.include_router(user_router)