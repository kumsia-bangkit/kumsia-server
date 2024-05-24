from fastapi.responses import JSONResponse

def get_test():
    return JSONResponse({"message": "Halo"}, status_code=200)