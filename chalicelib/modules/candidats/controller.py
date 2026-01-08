from http import HTTPStatus
from chalice import Blueprint, Response
from chalice import CORSConfig
from .service import CandidatService
from ...common.enums.response_type_enum import ResponseTypeEnum
from ...common.exceptions.exception import CandidatException
from ...common.helpers.error_middleware import exception_handler
from ...common.helpers.filters import Filters
from ...common.helpers.message_response_helper import MessageResponseHelper
from .messages import Messages
from .model import CandidatModel, CandidatPatchModel

cors_config = CORSConfig(
    allow_origin='*',
    allow_headers=['Content-Type', 'Authorization'],
    max_age=600,
    expose_headers=['Content-Length'],
    allow_credentials=True
)

service = CandidatService()
api = Blueprint(__name__)
CANDIDAT_URL = '/candidats'


@api.route(CANDIDAT_URL, methods=['POST'], cors=cors_config)
@exception_handler
def add():
    """Create a new candidat"""
    request = api.current_request
    payload = request.json_body
    model = CandidatModel.model_validate(payload)
    inserted_model = service.add_model(model)
    return Response(body=inserted_model.model_dump_json(exclude_none=True), status_code=HTTPStatus.CREATED)


@api.route(CANDIDAT_URL, methods=['GET'], cors=cors_config)
@exception_handler
def get_all_with_criteria():
    """Get all candidats with filtering and pagination"""
    query_params = api.current_request.query_params or {}
    criteria = Filters(**query_params)
    models = service.get_all_models(filters=criteria)
    return Response(body=models.model_dump_json(exclude_none=True))


@api.route(CANDIDAT_URL + '/{_id}', methods=['GET'], cors=cors_config)
@exception_handler
def get_by_id(_id):
    """Get candidat by ID"""
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


@api.route(CANDIDAT_URL + '/user/{user_id}', methods=['GET'], cors=cors_config)
@exception_handler
def get_by_user(user_id):
    """Get candidat by user ID"""
    if not user_id:
        message_response = MessageResponseHelper.build(
            ResponseTypeEnum.ERROR,
            Messages.REQUIRED_USER_ID)
        return Response(message_response, status_code=HTTPStatus.BAD_REQUEST)
    model = service.get_by_user(user_id)
    if model:
        return Response(body=model.model_dump_json(exclude_none=True))
    else:
        message_response = MessageResponseHelper.build(
            ResponseTypeEnum.ERROR,
            Messages.ERROR_NOT_FOUND)
        return Response(message_response, status_code=HTTPStatus.NOT_FOUND)


@api.route(CANDIDAT_URL + '/{_id}', methods=['PATCH'], cors=cors_config)
@exception_handler
def patch(_id):
    """Partially update a candidat"""
    if not _id:
        raise CandidatException(Messages.REQUIRED_ID)
    
    existing_candidat = service.get_model(_id)
    if not existing_candidat:
        message_response = MessageResponseHelper.build(
            ResponseTypeEnum.ERROR,
            Messages.ERROR_NOT_FOUND
        )
        return Response(message_response, status_code=HTTPStatus.NOT_FOUND)
    
    request = api.current_request
    candidat_patch_model = CandidatPatchModel.model_validate(request.json_body)
    
    if not any(candidat_patch_model.model_dump(exclude_none=True).keys()):
        candidat_patch_model_keys = list(candidat_patch_model.model_fields.keys())
        message = Messages.UNAUTHORIZED_FIELDS.format(allowed_fields=candidat_patch_model_keys)
        raise CandidatException(message)
    
    if not service.check_changes(existing_candidat, candidat_patch_model):
        return Response(body="", status_code=HTTPStatus.NO_CONTENT)
    
    # Update fields
    service.update_candidat(_id, candidat_patch_model)
    
    patched_model = service.get_model(_id)
    
    return Response(body=patched_model.model_dump_json(exclude_none=True))


@api.route(CANDIDAT_URL + '/{_id}', methods=['DELETE'], cors=cors_config)
@exception_handler
def delete_by_id(_id):
    """Delete a candidat (soft delete)"""
    if not _id:
        raise CandidatException(Messages.REQUIRED_ID)
    
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
