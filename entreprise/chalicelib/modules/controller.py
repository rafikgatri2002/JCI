from http import HTTPStatus
from chalice import Blueprint, Response
from chalice import CORSConfig
from .service import EntrepriseService
from ..common.enums.response_type_enum import ResponseTypeEnum
from ..common.exceptions.exception import EntrepriseException
from ..common.helpers.error_middleware import exception_handler
from ..common.helpers.filters import Filters
from ..common.helpers.message_response_helper import MessageResponseHelper
from .messages import Messages
from .model import EntrepriseModel, EntreprisePatchModel

cors_config = CORSConfig(
    allow_origin='*',
    allow_headers=['Content-Type', 'Authorization'],
    max_age=600,
    expose_headers=['Content-Length'],
    allow_credentials=True
)

service = EntrepriseService()
api = Blueprint(__name__)
ENTREPRISE_URL = '/entreprises'


@api.route(ENTREPRISE_URL, methods=['POST'], cors=cors_config)
@exception_handler
def add():
    """Create a new entreprise"""
    request = api.current_request
    payload = request.json_body
    model = EntrepriseModel.model_validate(payload)
    inserted_model = service.add_model(model)
    return Response(body=inserted_model.model_dump_json(exclude_none=True), status_code=HTTPStatus.CREATED)


@api.route(ENTREPRISE_URL, methods=['GET'], cors=cors_config)
@exception_handler
def get_all_with_criteria():
    """Get all entreprises with filtering and pagination"""
    query_params = api.current_request.query_params or {}
    criteria = Filters(**query_params)
    models = service.get_all_models(filters=criteria)
    return Response(body=models.model_dump_json(exclude_none=True))


@api.route(ENTREPRISE_URL + '/{_id}', methods=['GET'], cors=cors_config)
@exception_handler
def get_by_id(_id):
    """Get entreprise by ID"""
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


@api.route(ENTREPRISE_URL + '/name/{name}', methods=['GET'], cors=cors_config)
@exception_handler
def get_by_name(name):
    """Get entreprise by name"""
    if not name:
        message_response = MessageResponseHelper.build(
            ResponseTypeEnum.ERROR,
            Messages.REQUIRED_NAME)
        return Response(message_response, status_code=HTTPStatus.BAD_REQUEST)
    model = service.get_by_name(name)
    if model:
        return Response(body=model.model_dump_json(exclude_none=True))
    else:
        message_response = MessageResponseHelper.build(
            ResponseTypeEnum.ERROR,
            Messages.ERROR_NOT_FOUND)
        return Response(message_response, status_code=HTTPStatus.NOT_FOUND)


@api.route(ENTREPRISE_URL + '/{_id}', methods=['PATCH'], cors=cors_config)
@exception_handler
def patch(_id):
    """Partially update an entreprise"""
    if not _id:
        raise EntrepriseException(Messages.REQUIRED_ID)
    
    existing_entreprise = service.get_model(_id)
    if not existing_entreprise:
        message_response = MessageResponseHelper.build(
            ResponseTypeEnum.ERROR,
            Messages.ERROR_NOT_FOUND
        )
        return Response(message_response, status_code=HTTPStatus.NOT_FOUND)
    
    request = api.current_request
    entreprise_patch_model = EntreprisePatchModel.model_validate(request.json_body)

    if not any(entreprise_patch_model.model_dump(exclude_none=True).keys()):
        entreprise_patch_model_keys = list(entreprise_patch_model.model_fields.keys())
        message = Messages.UNAUTHORIZED_FIELDS.format(allowed_fields=entreprise_patch_model_keys)
        raise EntrepriseException(message)

    if not service.check_changes(existing_entreprise, entreprise_patch_model):
        return Response(body="", status_code=HTTPStatus.NO_CONTENT)

    # Update fields
    service.update_name(_id, entreprise_patch_model.name)
    service.update_description(_id, entreprise_patch_model.description)
    service.update_logo(_id, entreprise_patch_model.logo)
    service.update_website(_id, entreprise_patch_model.website)
    service.update_location(_id, entreprise_patch_model.location)

    patched_model = service.get_model(_id)

    return Response(body=patched_model.model_dump_json(exclude_none=True))


@api.route(ENTREPRISE_URL + '/{_id}', methods=['DELETE'], cors=cors_config)
@exception_handler
def delete_by_id(_id):
    """Delete an entreprise"""
    if not _id:
        raise EntrepriseException(Messages.REQUIRED_ID)
    
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
