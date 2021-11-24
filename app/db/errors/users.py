from fastapi import HTTPException, status

from app.resources.strings import *


class WrongLoginError(HTTPException):
    """Raised when log in input is incorrect (login or/and password)"""

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST, detail=INCORRECT_LOGIN_INPUT
        )

class WrongUserIdError(HTTPException):
    """Raised when trying to get user with incorrect id """

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST, detail=USER_ID_DOESNT_EXISTS
        )
