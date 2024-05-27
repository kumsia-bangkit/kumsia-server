import jwt

from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from .database import create_connection
from .utility import show_responses
from .environment import ALGORITHM, ACCESS_TOKEN_EXPIRE_DAYS, SECRET_KEY

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

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
            "id": temp_data[0],
            "username": temp_data[1],
            "roles": temp_data[6],
            "gender": temp_data[7],
        }
        db_username = temp_data[1]
        if username != db_username:
            return False
        if not verify_password(password, temp_data[2]):
            return show_responses("Incorrect Password", 401)
        return user_data
    except Exception as err:
        return show_responses("Failed when finding users", 401, error=err)
    
def create_access_token(user_data: dict):
    encode_data = user_data.copy()
    expire = datetime.now() + timedelta(days=int(ACCESS_TOKEN_EXPIRE_DAYS))
    encode_data.update({"exp": expire})
    jwt_token = jwt.encode(encode_data, SECRET_KEY, algorithm=ALGORITHM)
    return jwt_token