"""User controller for handling HTTP requests"""

from http import HTTPStatus
from chalice import Blueprint, Response
from chalice import CORSConfig
from .service import UserService
from ..common.enums.response_type_enum import ResponseTypeEnum
from ..common.exceptions.exception import UserException
from ..common.helpers.error_middleware import exception_handler
from ..common.helpers.filters import Filters
from ..common.helpers.message_response_helper import MessageResponseHelper
from .messages import Messages
from .model import UserModel, UserPatchModel

cors_config = CORSConfig(
    allow_origin='*',
    allow_headers=['Content-Type', 'Authorization'],
    max_age=600,
    expose_headers=['Content-Length'],
    allow_credentials=True
)

service = UserService()
api = Blueprint(__name__)
USER_URL = '/users'


@api.route(USER_URL, methods=['POST'], cors=cors_config)
@exception_handler
def add():
    """Create a new user"""
    request = api.current_request
    payload = request.json_body
    model = UserModel.model_validate(payload)
    inserted_model = service.add_model(model)
    return Response(body=inserted_model.model_dump_json(exclude_none=True), status_code=HTTPStatus.CREATED)


@api.route(USER_URL, methods=['GET'], cors=cors_config)
@exception_handler
def get_all_with_criteria():
    """Get all users with filtering and pagination"""
    query_params = api.current_request.query_params or {}
    criteria = Filters(**query_params)
    models = service.get_all_models(filters=criteria)
    return Response(body=models.model_dump_json(exclude_none=True))


@api.route(USER_URL + '/{_id}', methods=['GET'], cors=cors_config)
@exception_handler
def get_by_id(_id):
    """Get user by ID"""
    if not _id:
        message_response = MessageResponseHelper.build(
            ResponseTypeEnum.ERROR,
            Messages.REQUIRED_ID)
        return Response(message_response, status_code=HTTPStatus.BAD_REQUEST)
    model = service.get_model(_id)
    if model:
        return Response(body=model.model_dump_json(exclude_none=True))
    else:
        message_response = MessageResponseHelper.build(
            ResponseTypeEnum.ERROR,
            Messages.ERROR_NOT_FOUND)
        return Response(message_response, status_code=HTTPStatus.NOT_FOUND)


@api.route(USER_URL + '/email/{email}', methods=['GET'], cors=cors_config)
@exception_handler
def get_by_email(email):
    """Get user by email"""
    if not email:
        message_response = MessageResponseHelper.build(
            ResponseTypeEnum.ERROR,
            Messages.REQUIRED_EMAIL)
        return Response(message_response, status_code=HTTPStatus.BAD_REQUEST)
    model = service.get_by_email(email)
    if model:
        return Response(body=model.model_dump_json(exclude_none=True))
    else:
        message_response = MessageResponseHelper.build(
            ResponseTypeEnum.ERROR,
            Messages.ERROR_NOT_FOUND)
        return Response(message_response, status_code=HTTPStatus.NOT_FOUND)


@api.route(USER_URL + '/{_id}', methods=['PATCH'], cors=cors_config)
@exception_handler
def patch(_id):
    """Partially update a user"""
    if not _id:
        raise UserException(Messages.REQUIRED_ID)
    
    existing_user = service.get_model(_id)
    if not existing_user:
        message_response = MessageResponseHelper.build(
            ResponseTypeEnum.ERROR,
            Messages.ERROR_NOT_FOUND
        )
        return Response(message_response, status_code=HTTPStatus.NOT_FOUND)
    
    request = api.current_request
    user_patch_model = UserPatchModel.model_validate(request.json_body)

    if not any(user_patch_model.model_dump(exclude_none=True).keys()):
        user_patch_model_keys = list(user_patch_model.model_fields.keys())
        message = Messages.UNAUTHORIZED_FIELDS.format(allowed_fields=user_patch_model_keys)
        raise UserException(message)

    if not service.check_changes(existing_user, user_patch_model):
        return Response(body="", status_code=HTTPStatus.NO_CONTENT)

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

    return Response(body=patched_model.model_dump_json(exclude_none=True))


@api.route(USER_URL + '/{_id}', methods=['DELETE'], cors=cors_config)
@exception_handler
def delete_by_id(_id):
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
    return Response(message_response, status_code=status_code)


@api.route(USER_URL + '/{_id}/suspend', methods=['PATCH'], cors=cors_config)
@exception_handler
def suspend(_id):
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
        return Response(body=model.model_dump_json(exclude_none=True))
    else:
        message_response = MessageResponseHelper.build(
            ResponseTypeEnum.ERROR,
            Messages.ERROR_NOT_FOUND
        )
        return Response(message_response, status_code=HTTPStatus.NOT_FOUND)


@api.route(USER_URL + '/{_id}/activate', methods=['PATCH'], cors=cors_config)
@exception_handler
def activate(_id):
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
        return Response(body=model.model_dump_json(exclude_none=True))
    else:
        message_response = MessageResponseHelper.build(
            ResponseTypeEnum.ERROR,
            Messages.ERROR_NOT_FOUND
        )
        return Response(message_response, status_code=HTTPStatus.NOT_FOUND)
