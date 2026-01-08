from http import HTTPStatus
from chalice import Blueprint, Response
from chalice import CORSConfig
from .service import EmploiService
from ...common.enums.response_type_enum import ResponseTypeEnum
from ...common.exceptions.exception import EmploiException
from ...common.helpers.error_middleware import exception_handler
from ...common.helpers.filters import Filters
from ...common.helpers.message_response_helper import MessageResponseHelper
from .messages import Messages
from .model import EmploiModel, EmploiPatchModel

cors_config = CORSConfig(
    allow_origin='*',
    allow_headers=['Content-Type', 'Authorization'],
    max_age=600,
    expose_headers=['Content-Length'],
    allow_credentials=True
)

service = EmploiService()
api = Blueprint(__name__)
EMPLOI_URL = '/emplois'


@api.route(EMPLOI_URL, methods=['POST'], cors=cors_config)
@exception_handler
def add():
    """Create a new emploi"""
    request = api.current_request
    payload = request.json_body
    model = EmploiModel.model_validate(payload)
    inserted_model = service.add_model(model)
    return Response(body=inserted_model.model_dump_json(exclude_none=True), status_code=HTTPStatus.CREATED)


@api.route(EMPLOI_URL, methods=['GET'], cors=cors_config)
@exception_handler
def get_all_with_criteria():
    """Get all emplois with filtering and pagination"""
    query_params = api.current_request.query_params or {}
    criteria = Filters(**query_params)
    models = service.get_all_models(filters=criteria)
    return Response(body=models.model_dump_json(exclude_none=True))


@api.route(EMPLOI_URL + '/{_id}', methods=['GET'], cors=cors_config)
@exception_handler
def get_by_id(_id):
    """Get emploi by ID"""
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


@api.route(EMPLOI_URL + '/user/{user_id}/entreprise/{entreprise_id}', methods=['GET'], cors=cors_config)
@exception_handler
def get_by_user_and_entreprise(user_id, entreprise_id):
    """Get emploi by user ID and entreprise ID"""
    if not user_id:
        message_response = MessageResponseHelper.build(
            ResponseTypeEnum.ERROR,
            Messages.REQUIRED_USER_ID)
        return Response(message_response, status_code=HTTPStatus.BAD_REQUEST)
    if not entreprise_id:
        message_response = MessageResponseHelper.build(
            ResponseTypeEnum.ERROR,
            Messages.REQUIRED_ENTREPRISE_ID)
        return Response(message_response, status_code=HTTPStatus.BAD_REQUEST)
    model = service.get_by_user_and_entreprise(user_id, entreprise_id)
    if model:
        return Response(body=model.model_dump_json(exclude_none=True))
    else:
        message_response = MessageResponseHelper.build(
            ResponseTypeEnum.ERROR,
            Messages.ERROR_NOT_FOUND)
        return Response(message_response, status_code=HTTPStatus.NOT_FOUND)


@api.route(EMPLOI_URL + '/{_id}', methods=['PATCH'], cors=cors_config)
@exception_handler
def patch(_id):
    """Partially update an emploi"""
    if not _id:
        raise EmploiException(Messages.REQUIRED_ID)
    
    existing_emploi = service.get_model(_id)
    if not existing_emploi:
        message_response = MessageResponseHelper.build(
            ResponseTypeEnum.ERROR,
            Messages.ERROR_NOT_FOUND
        )
        return Response(message_response, status_code=HTTPStatus.NOT_FOUND)
    
    request = api.current_request
    emploi_patch_model = EmploiPatchModel.model_validate(request.json_body)
    
    if not any(emploi_patch_model.model_dump(exclude_none=True).keys()):
        emploi_patch_model_keys = list(emploi_patch_model.model_fields.keys())
        message = Messages.UNAUTHORIZED_FIELDS.format(allowed_fields=emploi_patch_model_keys)
        raise EmploiException(message)
    
    if not service.check_changes(existing_emploi, emploi_patch_model):
        return Response(body="", status_code=HTTPStatus.NO_CONTENT)
    
    # Update fields
    service.update_position(_id, emploi_patch_model.position)
    
    patched_model = service.get_model(_id)
    
    return Response(body=patched_model.model_dump_json(exclude_none=True))


@api.route(EMPLOI_URL + '/{_id}', methods=['DELETE'], cors=cors_config)
@exception_handler
def delete_by_id(_id):
    """Delete an emploi (soft delete)"""
    if not _id:
        raise EmploiException(Messages.REQUIRED_ID)
    
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
