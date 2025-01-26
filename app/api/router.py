from fastapi.routing import APIRouter

from api.system.book_controller import router as book_router
from api.system.patron_controller import router as patron_router
from api.system.checkout_controller import router as checkout_router

api_router = APIRouter()
api_router.include_router(book_router, prefix="/v1", tags=["book"])
api_router.include_router(patron_router, prefix="/v1", tags=["patron"])
api_router.include_router(checkout_router, prefix="/v1", tags=["checkout"])
