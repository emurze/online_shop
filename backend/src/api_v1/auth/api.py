from fastapi import APIRouter
from api_v1.auth.models import User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
async def register():
    """Part of BPMN diagram"""


@router.post("/login")
async def login():
    """Part of BPMN diagram"""
