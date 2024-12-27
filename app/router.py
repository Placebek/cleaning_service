from fastapi import APIRouter

from app.api.auth.auth_user import router as auth_user_router
from app.api.auth.auth_admin import router as auth_admin_router


route = APIRouter()

route.include_router(auth_user_router, prefix="", tags=["UserAuthentication"])
route.include_router(auth_admin_router, prefix="/admin", tags=["AdminAuthentication"])

# route.include_router(docs_router, prefix="/docs", tags=["Docs"])
