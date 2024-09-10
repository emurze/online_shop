from fastapi import APIRouter
from .models import User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
async def register():
    """Part of BPMN diagram"""


@router.post("/login")
async def login():
    """Part of BPMN diagram"""
