import uuid

from . import response_schema as Response
from utils.database import create_connection
from fastapi.responses import JSONResponse

def register(request):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO users (id, username, password, first_name, last_name, dob, roles, gender)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
            """, (str(uuid.uuid4()), request.username, request.password, request.first_name, request.last_name, request.dob, request.roles, request.gender)
        )
        conn.commit()
        conn.close()
        return JSONResponse({"message": "Account has beed created"}, status_code=201)
    except Exception as err:
        return JSONResponse({"message": "Failed creating an account", "err": err}, status_code=500)