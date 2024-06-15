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
        user_data = cursor.fetchone()

        cursor.execute(
            """
            SELECT * 
            FROM organization
            WHERE username=%s   
            """, (username,)
        )
        org_data = cursor.fetchone()

        if not user_data and not org_data:
            return show_responses("User not found", 404)

        if user_data:
            temp_data = user_data
            data = [{
                "sub": user_data['user_id'],
                "name": user_data['name'],
                "username": user_data['username'],
                "is_new_user": user_data['is_new_user']
            }, "user"]

        elif org_data:
            temp_data = org_data
            data = [{
            "sub": org_data['organization_id'],
            "name": org_data['name'],
            "username": org_data['username'],
            "is_new_user": org_data['is_new_user']
            }, "organization"]

        if not verify_password(password, temp_data['password']):
            return show_responses("Incorrect Password", 401)
        
        conn.close()
        return data
    except Exception as err:
        return show_responses("Failed when finding users", 401, error=err)
    
def create_access_token(user_data: dict, role: str):
    encode_data = user_data.copy()
    expire = datetime.now() + timedelta(days=int(ACCESS_TOKEN_EXPIRE_DAYS))
    encode_data.update({"exp": expire, "role": role})
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
            """SELECT 
                u.user_id,
                u.preference_id,
                u.username,
                u.name,
                u.email,
                u.contact,
                u.guardian_contact,
                u.profile_picture,
                u.religion,
                u.gender,
                u.dob,
                u.city,
                u.last_activity,
                u.is_new_user,
                p.hobby AS preference_hobby,
                p.religion AS preference_religion,
                p.city AS preference_city,
                p.gender AS preference_gender
                FROM users u
                LEFT JOIN preference p ON u.preference_id = p.preference_id
                WHERE u.user_id = %s;
            """,
            (user_id,)
        )
        user_data = cursor.fetchone()
        return user_data
    except Exception as err:
        show_responses("User Not Found", 404, error=err)

def get_org_from_id(org_id: str):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """SELECT
                organization_id, name, username,
                email, profile_picture, contact,
                description, is_new_user
                FROM organization
                WHERE organization_id = %s;
            """,
            (org_id,)
        )
        org_data = cursor.fetchone()
        return org_data
    except Exception as err:
        show_responses("Organization Not Found", 404, error=err)

def validate_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise handle_token_error('User id not provided')
        return payload
    except InvalidTokenError:
        raise handle_token_error('Token Expired or Invalid')

def validate_token_and_id(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise handle_token_error('User id not provided')
        return user_id
    except InvalidTokenError:
        raise handle_token_error('Token Expired or Invalid')

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    payload = validate_token(token)
    id: str = payload.get('sub')

    if payload.get('role') == "user":
        user_data = get_user_from_id(id)
        return user_data
    elif payload.get('role') == "organization":
        org_data = get_org_from_id(id)
        return org_data