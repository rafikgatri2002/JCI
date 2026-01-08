"""Error handling middleware"""
from functools import wraps
from http import HTTPStatus
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from ..enums.response_type_enum import ResponseTypeEnum
from ..exceptions.exception import (
    UserException, UserAlreadyExistsException, UserNotFoundException,
    JobException, EntrepriseException, EmploiException,
    CandidatException, ApplicationException
)
from ..helpers.message_response_helper import MessageResponseHelper


def exception_handler(func):
    """Decorator to handle exceptions in route handlers"""
    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except UserAlreadyExistsException as e:
            message_response = MessageResponseHelper.build(
                ResponseTypeEnum.ERROR,
                str(e)
            )
            return JSONResponse(content=message_response, status_code=HTTPStatus.CONFLICT)
        except UserNotFoundException as e:
            message_response = MessageResponseHelper.build(
                ResponseTypeEnum.ERROR,
                str(e)
            )
            return JSONResponse(content=message_response, status_code=HTTPStatus.NOT_FOUND)
        except (UserException, JobException, EntrepriseException, 
                EmploiException, CandidatException, ApplicationException) as e:
            message_response = MessageResponseHelper.build(
                ResponseTypeEnum.ERROR,
                str(e)
            )
            return JSONResponse(content=message_response, status_code=HTTPStatus.BAD_REQUEST)
        except ValueError as e:
            message_response = MessageResponseHelper.build(
                ResponseTypeEnum.ERROR,
                str(e)
            )
            return JSONResponse(content=message_response, status_code=HTTPStatus.BAD_REQUEST)
        except Exception as e:
            message_response = MessageResponseHelper.build(
                ResponseTypeEnum.ERROR,
                f"Internal server error: {str(e)}"
            )
            return JSONResponse(content=message_response, status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
    
    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except UserAlreadyExistsException as e:
            message_response = MessageResponseHelper.build(
                ResponseTypeEnum.ERROR,
                str(e)
            )
            return JSONResponse(content=message_response, status_code=HTTPStatus.CONFLICT)
        except UserNotFoundException as e:
            message_response = MessageResponseHelper.build(
                ResponseTypeEnum.ERROR,
                str(e)
            )
            return JSONResponse(content=message_response, status_code=HTTPStatus.NOT_FOUND)
        except (UserException, JobException, EntrepriseException, 
                EmploiException, CandidatException, ApplicationException) as e:
            message_response = MessageResponseHelper.build(
                ResponseTypeEnum.ERROR,
                str(e)
            )
            return JSONResponse(content=message_response, status_code=HTTPStatus.BAD_REQUEST)
        except ValueError as e:
            message_response = MessageResponseHelper.build(
                ResponseTypeEnum.ERROR,
                str(e)
            )
            return JSONResponse(content=message_response, status_code=HTTPStatus.BAD_REQUEST)
        except Exception as e:
            message_response = MessageResponseHelper.build(
                ResponseTypeEnum.ERROR,
                f"Internal server error: {str(e)}"
            )
            return JSONResponse(content=message_response, status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
    
    # Return appropriate wrapper based on whether the function is async or not
    import inspect
    if inspect.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper
