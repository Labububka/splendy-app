from fastapi import APIRouter
from dtos.auth_dto import RegisterRequest, LoginRequest
import services.auth_service as auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
def register(body: RegisterRequest):
    return auth_service.register(body.email, body.password, body.name)


@router.post("/login")
def login(body: LoginRequest):
    return auth_service.login(body.email, body.password)


@router.post("/logout")
def logout():
    return {"message": "Logged out"}
