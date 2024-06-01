from fastapi.responses import JSONResponse
from .database import create_connection

def show_responses(message: str, status_code: int, data=None, error=None):
    response_content = {"message": message}
    if data is not None:
        response_content["data"] = data
    if error is not None:
        response_content["error"] = error
    return JSONResponse(response_content, status_code=status_code)

def find_duplicate_data(table: str, column: str, data):
    conn = create_connection()
    cursor = conn.cursor()
    try: 
        query = f"""
            SELECT COUNT(*)
            FROM {table}
            WHERE {column} = %s
        """
        cursor.execute(query, (data,))
        result = cursor.fetchone()
        conn.close()
        return result[0] > 0
    except Exception as err:
        return JSONResponse({"message": "Failed find data", "error": err}, status_code=500)