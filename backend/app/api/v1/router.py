from fastapi import APIRouter
from app.api.v1.endpoints import auth, snippets, analysis

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(snippets.router, prefix="/snippets", tags=["Code Snippets"])
api_router.include_router(analysis.router, prefix="/analysis", tags=["Code Analysis"])