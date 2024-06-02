import jwt

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from .database import create_connection
from .utility import show_responses
from .environment import ALGORITHM, ACCESS_TOKEN_EXPIRE_DAYS, SECRET_KEY
from typing import Annotated
from jwt.exceptions import InvalidTokenError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# Authenticate user from db
def authenticate_user(username: str, password: str):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT * 
            FROM users
            WHERE username=%s   
            """, (username,)
        )
        temp_data = cursor.fetchone()
        if not temp_data:
            return show_responses("User not found", 404)

        user_data = {
            "user_id": temp_data[0],
            "username": temp_data[2],
            "gender": temp_data[10],
        }
        db_username = temp_data[2]
        if username != db_username:
            return False
        if not verify_password(password, temp_data[4]):
            return show_responses("Incorrect Password", 401)
        conn.close()
        return user_data
    except Exception as err:
        return show_responses("Failed when finding users", 401, error=err)
    
def create_access_token(user_data: dict):
    encode_data = user_data.copy()
    expire = datetime.now() + timedelta(days=int(ACCESS_TOKEN_EXPIRE_DAYS))
    encode_data.update({"exp": expire})
    jwt_token = jwt.encode(encode_data, SECRET_KEY, algorithm=ALGORITHM)
    return jwt_token

def handle_token_error(message: str):
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=message,
        headers={"WWW-Authenticate": "<Token>"},
    )

def get_user_from_id(user_id: str):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT * FROM users WHERE user_id=%s", (user_id,)
        )
        temp_data = cursor.fetchone()
        user_data = {
            "id": temp_data[0],
            "username": temp_data[2],
            "gender": temp_data[10],
        }
        return user_data
    except Exception as err:
        show_responses("User Not Found", 404, error=err)

def validate_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise handle_token_error('User id not provided')
        return payload
    except InvalidTokenError:
        raise handle_token_error('Token Expired or Invalid')

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    payload = validate_token(token)
    user_id: str = payload.get('user_id')
    user_data = get_user_from_id(user_id)
    return user_data