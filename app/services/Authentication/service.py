import uuid

from . import response_schema as Response
from fastapi.responses import JSONResponse
from app.utils.database import create_connection
from app.utils.authentication import get_password_hash
from app.utils.utility import find_duplicate_data

def register(request):
    conn = create_connection()
    cursor = conn.cursor()
    username = request.username
    isDuplicate = find_duplicate_data("users", "username", username.lower())
    if isDuplicate:
        return JSONResponse({"messagge": f"{request.username} username has been taken"}, status_code=406)
    try:
        cursor.execute(
            """
            INSERT INTO users (user_id, username, email, password, name, dob, gender)
            VALUES(%s, %s, %s, %s, %s, %s, %s)
            """, (str(uuid.uuid4()), username.lower(), request.email, get_password_hash(request.password), request.name, request.dob, request.gender)
        )
        conn.commit()
        conn.close()
        return JSONResponse({"message": "Account has beed created"}, status_code=201)
    except Exception as err:
        return JSONResponse({"message": "Failed creating an account", "err": err}, status_code=500)
