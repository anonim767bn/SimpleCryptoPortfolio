from fastapi import FastAPI, Depends, status, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from db import get_session_factory, create_user
from dependencies import get_current_user
from fastapi.exceptions import HTTPException
from security import create_access_token, get_password_hash
from schemas import UserCreate
from pydantic import ValidationError


app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    return Response(content=exc.errors()[0]['msg'], status_code=status.HTTP_400_BAD_REQUEST)


@app.get('/')
def read_item():
    return '<Hello world>'


@app.post('/token')
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session_factory=Depends(get_session_factory)):
    user = get_current_user(
        form_data.username, form_data.password, session_factory)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Incorrect username or password')
    return {'token': create_access_token({"sub": user.id}), 'token_type': 'bearer'}


@app.post('/register')
async def register(form_data: UserCreate = Depends(), session_factory=Depends(get_session_factory)):
    user = get_current_user(
        form_data.username, form_data.password, session_factory)
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='User already exists')
    user = create_user(session_factory=session_factory, username=form_data.username,
                       password=get_password_hash(form_data.password))
    return Response(status_code=status.HTTP_201_CREATED, content='User created')
