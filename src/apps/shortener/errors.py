from rest_framework.exceptions import APIException
from rest_framework import status


class CreateShortException(Exception):
    pass


class CreateShortAPIException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Cannot create short url. Try again later."
    default_code = "create_short_error"
