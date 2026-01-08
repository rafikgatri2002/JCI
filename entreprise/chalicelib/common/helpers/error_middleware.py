"""Error handling middleware"""
from functools import wraps
from http import HTTPStatus
from chalice import Response
from ..enums.response_type_enum import ResponseTypeEnum
from ..exceptions.exception import (
    UserException, UserAlreadyExistsException, UserNotFoundException,
    EntrepriseException, EntrepriseAlreadyExistsException, EntrepriseNotFoundException
)
from ..helpers.message_response_helper import MessageResponseHelper


def exception_handler(func):
    """Decorator to handle exceptions in route handlers"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except UserAlreadyExistsException as e:
            message_response = MessageResponseHelper.build(
                ResponseTypeEnum.ERROR,
                str(e)
            )
            return Response(message_response, status_code=HTTPStatus.CONFLICT)
        except UserNotFoundException as e:
            message_response = MessageResponseHelper.build(
                ResponseTypeEnum.ERROR,
                str(e)
            )
            return Response(message_response, status_code=HTTPStatus.NOT_FOUND)
        except UserException as e:
            message_response = MessageResponseHelper.build(
                ResponseTypeEnum.ERROR,
                str(e)
            )
            return Response(message_response, status_code=HTTPStatus.BAD_REQUEST)
        except EntrepriseAlreadyExistsException as e:
            message_response = MessageResponseHelper.build(
                ResponseTypeEnum.ERROR,
                str(e)
            )
            return Response(message_response, status_code=HTTPStatus.CONFLICT)
        except EntrepriseNotFoundException as e:
            message_response = MessageResponseHelper.build(
                ResponseTypeEnum.ERROR,
                str(e)
            )
            return Response(message_response, status_code=HTTPStatus.NOT_FOUND)
        except EntrepriseException as e:
            message_response = MessageResponseHelper.build(
                ResponseTypeEnum.ERROR,
                str(e)
            )
            return Response(message_response, status_code=HTTPStatus.BAD_REQUEST)
        except ValueError as e:
            message_response = MessageResponseHelper.build(
                ResponseTypeEnum.ERROR,
                str(e)
            )
            return Response(message_response, status_code=HTTPStatus.BAD_REQUEST)
        except Exception as e:
            message_response = MessageResponseHelper.build(
                ResponseTypeEnum.ERROR,
                f"Internal server error: {str(e)}"
            )
            return Response(message_response, status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
    return wrapper
