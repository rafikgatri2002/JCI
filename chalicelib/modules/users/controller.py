"""User controller for handling HTTP requests"""

from http import HTTPStatus
from fastapi import APIRouter, Query, Path, Body, status
from fastapi.responses import JSONResponse, Response
from .service import UserService
from ...common.enums.response_type_enum import ResponseTypeEnum
from ...common.exceptions.exception import UserException
from ...common.helpers.error_middleware import exception_handler
from ...common.helpers.filters import Filters
from ...common.helpers.message_response_helper import MessageResponseHelper
from .messages import Messages
from .model import UserModel, UserPatchModel

service = UserService()
router = APIRouter(prefix='/users', tags=['users'])


@router.post('', status_code=status.HTTP_201_CREATED)
@exception_handler
def add(payload: UserModel):
    """Create a new user"""
    inserted_model = service.add_model(payload)
    return JSONResponse(
        content=inserted_model.model_dump(exclude_none=True, mode='json'),
        status_code=HTTPStatus.CREATED
    )


@router.get('')
@exception_handler
def get_all_with_criteria(
    email: str = Query(None),
    role: str = Query(None),
    status: str = Query(None),
    skip: int = Query(0),
    limit: int = Query(100)
):
    """Get all users with filtering and pagination"""
    # If email is provided, get specific user
    if email:
        model = service.get_by_email(email)
        if model:
            return JSONResponse(content=model.model_dump(exclude_none=True, mode='json'))
        else:
            message_response = MessageResponseHelper.build(
                ResponseTypeEnum.ERROR,
                Messages.ERROR_NOT_FOUND)
            return JSONResponse(content=message_response, status_code=HTTPStatus.NOT_FOUND)
    
    criteria = Filters(role=role, status=status, email=email, skip=skip, limit=limit)
    models = service.get_all_models(filters=criteria)
    return JSONResponse(content=models.model_dump(exclude_none=True, mode='json'))


@router.get('/{_id}')
@exception_handler
def get_by_id(_id: str = Path(...)):
    """Get user by ID"""
    if not _id:
        message_response = MessageResponseHelper.build(
            ResponseTypeEnum.ERROR,
            Messages.REQUIRED_ID)
        return JSONResponse(content=message_response, status_code=HTTPStatus.BAD_REQUEST)
    model = service.get_model(_id)
    if model:
        return JSONResponse(content=model.model_dump(exclude_none=True, mode='json'))
    else:
        message_response = MessageResponseHelper.build(
            ResponseTypeEnum.ERROR,
            Messages.ERROR_NOT_FOUND)
        return JSONResponse(content=message_response, status_code=HTTPStatus.NOT_FOUND)


@router.patch('/{_id}')
@exception_handler
def patch(_id: str = Path(...), user_patch_model: UserPatchModel = Body(...)):
    """Partially update a user"""
    if not _id:
        raise UserException(Messages.REQUIRED_ID)
    
    existing_user = service.get_model(_id)
    if not existing_user:
        message_response = MessageResponseHelper.build(
            ResponseTypeEnum.ERROR,
            Messages.ERROR_NOT_FOUND
        )
        return JSONResponse(content=message_response, status_code=HTTPStatus.NOT_FOUND)
    
    if not any(user_patch_model.model_dump(exclude_none=True).keys()):
        user_patch_model_keys = list(user_patch_model.model_fields.keys())
        message = Messages.UNAUTHORIZED_FIELDS.format(allowed_fields=user_patch_model_keys)
        raise UserException(message)

    if not service.check_changes(existing_user, user_patch_model):
        return Response(content="", status_code=HTTPStatus.NO_CONTENT)

    # Update full name
    service.update_full_name(_id, user_patch_model.fullName)
    # Update email
    service.update_email(_id, user_patch_model.email)
    # Update phone
    service.update_phone(_id, user_patch_model.phone)
    # Update role
    service.update_role(_id, user_patch_model.role)
    # Update status
    service.update_status(_id, user_patch_model.status)

    patched_model = service.get_model(_id)

    return JSONResponse(content=patched_model.model_dump(exclude_none=True, mode='json'))


@router.delete('/{_id}')
@exception_handler
def delete_by_id(_id: str = Path(...)):
    """Soft delete a user"""
    if not _id:
        raise UserException(Messages.REQUIRED_ID)
    
    if service.delete_model(_id):
        message_response = MessageResponseHelper.build(
            ResponseTypeEnum.SUCCESS,
            Messages.SUCCESS_DELETED
        )
        status_code = HTTPStatus.OK
    else:
        message_response = MessageResponseHelper.build(
            ResponseTypeEnum.ERROR,
            Messages.ERROR_NOT_FOUND
        )
        status_code = HTTPStatus.NOT_FOUND
    return JSONResponse(content=message_response, status_code=status_code)


@router.patch('/{_id}/suspend')
@exception_handler
def suspend(_id: str = Path(...)):
    """Suspend a user"""
    if not _id:
        raise UserException(Messages.REQUIRED_ID)
    
    service.update_status(_id, "suspended")
    model = service.get_model(_id)
    
    if model:
        message_response = MessageResponseHelper.build(
            ResponseTypeEnum.SUCCESS,
            Messages.SUCCESS_SUSPENDED
        )
        return JSONResponse(content=model.model_dump(exclude_none=True, mode='json'))
    else:
        message_response = MessageResponseHelper.build(
            ResponseTypeEnum.ERROR,
            Messages.ERROR_NOT_FOUND
        )
        return JSONResponse(content=message_response, status_code=HTTPStatus.NOT_FOUND)


@router.patch('/{_id}/activate')
@exception_handler
def activate(_id: str = Path(...)):
    """Activate a user"""
    if not _id:
        raise UserException(Messages.REQUIRED_ID)
    
    service.update_status(_id, "active")
    model = service.get_model(_id)
    
    if model:
        message_response = MessageResponseHelper.build(
            ResponseTypeEnum.SUCCESS,
            Messages.SUCCESS_ACTIVATED
        )
        return JSONResponse(content=model.model_dump(exclude_none=True, mode='json'))
    else:
        message_response = MessageResponseHelper.build(
            ResponseTypeEnum.ERROR,
            Messages.ERROR_NOT_FOUND
        )
        return JSONResponse(content=message_response, status_code=HTTPStatus.NOT_FOUND)
