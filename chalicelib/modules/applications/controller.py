from http import HTTPStatus
from chalice import Blueprint, Response
from chalice import CORSConfig
from .service import ApplicationService
from ...common.enums.response_type_enum import ResponseTypeEnum
from ...common.exceptions.exception import ApplicationException
from ...common.helpers.error_middleware import exception_handler
from ...common.helpers.filters import Filters
from ...common.helpers.message_response_helper import MessageResponseHelper
from .messages import Messages
from .model import ApplicationModel, ApplicationPatchModel

cors_config = CORSConfig(
    allow_origin='*',
    allow_headers=['Content-Type', 'Authorization'],
    max_age=600,
    expose_headers=['Content-Length'],
    allow_credentials=True
)

service = ApplicationService()
api = Blueprint(__name__)
APPLICATION_URL = '/applications'


@api.route(APPLICATION_URL, methods=['POST'], cors=cors_config)
@exception_handler
def add():
    """Create a new application"""
    request = api.current_request
    payload = request.json_body
    model = ApplicationModel.model_validate(payload)
    inserted_model = service.add_model(model)
    return Response(body=inserted_model.model_dump_json(exclude_none=True), status_code=HTTPStatus.CREATED)


@api.route(APPLICATION_URL, methods=['GET'], cors=cors_config)
@exception_handler
def get_all_with_criteria():
    """Get all applications with filtering and pagination"""
    query_params = api.current_request.query_params or {}
    criteria = Filters(**query_params)
    models = service.get_all_models(filters=criteria)
    return Response(body=models.model_dump_json(exclude_none=True))


@api.route(APPLICATION_URL + '/{_id}', methods=['GET'], cors=cors_config)
@exception_handler
def get_by_id(_id):
    """Get application by ID"""
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


@api.route(APPLICATION_URL + '/job/{job_id}', methods=['GET'], cors=cors_config)
@exception_handler
def get_by_job(job_id):
    """Get applications by job ID"""
    if not job_id:
        message_response = MessageResponseHelper.build(
            ResponseTypeEnum.ERROR,
            Messages.REQUIRED_JOB_ID)
        return Response(message_response, status_code=HTTPStatus.BAD_REQUEST)
    models = service.get_by_job(job_id)
    return Response(body=models.model_dump_json(exclude_none=True))


@api.route(APPLICATION_URL + '/candidat/{candidat_id}', methods=['GET'], cors=cors_config)
@exception_handler
def get_by_candidat(candidat_id):
    """Get applications by candidate ID"""
    if not candidat_id:
        message_response = MessageResponseHelper.build(
            ResponseTypeEnum.ERROR,
            Messages.REQUIRED_CANDIDAT_ID)
        return Response(message_response, status_code=HTTPStatus.BAD_REQUEST)
    models = service.get_by_candidat(candidat_id)
    return Response(body=models.model_dump_json(exclude_none=True))


@api.route(APPLICATION_URL + '/{_id}', methods=['PATCH'], cors=cors_config)
@exception_handler
def patch(_id):
    """Partially update an application"""
    if not _id:
        raise ApplicationException(Messages.REQUIRED_ID)
    
    existing_application = service.get_model(_id)
    if not existing_application:
        message_response = MessageResponseHelper.build(
            ResponseTypeEnum.ERROR,
            Messages.ERROR_NOT_FOUND
        )
        return Response(message_response, status_code=HTTPStatus.NOT_FOUND)
    
    request = api.current_request
    application_patch_model = ApplicationPatchModel.model_validate(request.json_body)
    
    if not any(application_patch_model.model_dump(exclude_none=True).keys()):
        application_patch_model_keys = list(application_patch_model.model_fields.keys())
        message = Messages.UNAUTHORIZED_FIELDS.format(allowed_fields=application_patch_model_keys)
        raise ApplicationException(message)
    
    if not service.check_changes(existing_application, application_patch_model):
        return Response(body="", status_code=HTTPStatus.NO_CONTENT)
    
    # Update fields
    service.update_application(_id, application_patch_model)
    
    patched_model = service.get_model(_id)
    
    return Response(body=patched_model.model_dump_json(exclude_none=True))


@api.route(APPLICATION_URL + '/{_id}', methods=['DELETE'], cors=cors_config)
@exception_handler
def delete_by_id(_id):
    """Delete an application (soft delete)"""
    if not _id:
        raise ApplicationException(Messages.REQUIRED_ID)
    
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
