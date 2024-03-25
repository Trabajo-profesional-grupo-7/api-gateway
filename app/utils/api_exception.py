from typing import Union

from fastapi import HTTPException, status

from app.utils.api_exception import *
from app.utils.constants import *


class APIException(Exception):
    def __init__(self, code: str, msg: str):
        super().__init__(msg)
        self.code = code

    def get_code(self) -> str:
        return self.code


class APIExceptionToHTTP:
    def __init__(self):
        self.error_dict = {
            INTERNAL_SERVICE_ERROR: status.HTTP_500_INTERNAL_SERVER_ERROR,
            FLIGTH_INFO_NOT_FOUND_ERROR: status.HTTP_404_NOT_FOUND,
            INVALID_CREDENTIALS_ERROR: status.HTTP_401_UNAUTHORIZED,
            USER_EXISTS_ERROR: status.HTTP_409_CONFLICT,
            LOGIN_ERROR: status.HTTP_400_BAD_REQUEST,
            USER_UNAUTHORIZED_ERROR: status.HTTP_401_UNAUTHORIZED,
            USER_DOES_NOT_EXISTS_ERROR: status.HTTP_404_NOT_FOUND,
        }

    def convert(
        self, err: APIException, headers: Union[dict, None] = None
    ) -> HTTPException:
        err_code = err.get_code()
        # Return 500 INTERNAL SERVER ERROR as default status
        err_http_status = self.error_dict.get(
            err_code, status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        err_detail = f"{err_code}: {str(err)}"
        return HTTPException(
            status_code=err_http_status, detail=err_detail, headers=headers
        )
