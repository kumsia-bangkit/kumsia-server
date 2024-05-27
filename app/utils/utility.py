from fastapi.responses import JSONResponse

def show_responses(message, status_code, data=None, error=None):
    response_content = {"message": message}
    if data is not None:
        response_content["data"] = data
    if error is not None:
        response_content["error"] = error
    return JSONResponse(response_content, status_code=status_code)
