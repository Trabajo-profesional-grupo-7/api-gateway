from fastapi import HTTPException


def handle_response_error(current_status_code, response):
    if response.status_code != current_status_code:
        raise HTTPException(status_code=response.status_code, detail=response.json())
