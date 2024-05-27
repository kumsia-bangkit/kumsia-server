from passlib.context import CryptContext
from jwt.exceptions import InvalidTokenError
from .database import create_connection
from .utility import show_responses

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
            return False
        return user_data
    except Exception as err:
        return show_responses("Failed when finding users", 401, error=err)