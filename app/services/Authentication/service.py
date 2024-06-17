import uuid
from fastapi.responses import JSONResponse
from app.utils.database import create_connection
from app.utils.authentication import get_password_hash
from app.utils.utility import find_duplicate_data

def register(request):
    conn = create_connection()
    cursor = conn.cursor()
    username = request.username
    user_exists = find_duplicate_data("users", "username", username.lower())
    org_exists = find_duplicate_data("organization", "username", username.lower())
    if user_exists or org_exists:
        return JSONResponse({"messagge": f"username {request.username} has been taken"}, status_code=406)
    try:
        preference_id = str(uuid.uuid4())
        try:
            cursor.execute(
                """
                INSERT INTO preference (preference_id) VALUES (%s)
                """, (preference_id,)
            )
        except Exception as err:
            return JSONResponse({"message": "Failed creating an user's preference", "err": err}, status_code=500)
        cursor.execute(
            """
            INSERT INTO users (user_id, preference_id, username, email, password, name, dob, gender)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
            """, (str(uuid.uuid4()), preference_id, username.lower(), request.email, get_password_hash(request.password), request.name, request.dob, request.gender)
        )
        conn.commit()
        conn.close()
        return JSONResponse({"message": "Account has beed created"}, status_code=201)
    except Exception as err:
        return JSONResponse({"message": "Failed creating an account", "err": err}, status_code=500)

def register_organization(request):
    conn = create_connection()
    cursor = conn.cursor()
    username = request.username
    user_exists = find_duplicate_data("users", "username", username.lower())
    org_exists = find_duplicate_data("organization", "username", username.lower())
    if user_exists or org_exists:
        return JSONResponse({"messagge": f"username {request.username} has been taken"}, status_code=406)
    try:
        cursor.execute(
            """
            INSERT INTO organization (organization_id, name, username, password, email)
            VALUES(%s, %s, %s, %s, %s)
            """, (str(uuid.uuid4()), request.name, username.lower(), get_password_hash(request.password), request.email)
        )
        conn.commit()
        conn.close()
        return JSONResponse({"message": "Account has beed created"}, status_code=201)
    except Exception as err:
        return JSONResponse({"message": "Failed creating an account", "err": err}, status_code=500)
