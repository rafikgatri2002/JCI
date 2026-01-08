from http import HTTPStatus
from chalice import Blueprint, Response
from chalice import CORSConfig
from .service import JobService
from ...common.enums.response_type_enum import ResponseTypeEnum
from ...common.exceptions.exception import JobException
from ...common.helpers.error_middleware import exception_handler
from ...common.helpers.filters import Filters
from ...common.helpers.message_response_helper import MessageResponseHelper
from .messages import Messages
from .model import JobModel, JobPatchModel

cors_config = CORSConfig(
    allow_origin='*',
    allow_headers=['Content-Type', 'Authorization'],
    max_age=600,
    expose_headers=['Content-Length'],
    allow_credentials=True
)

service = JobService()
api = Blueprint(__name__)
JOB_URL = '/jobs'


@api.route(JOB_URL, methods=['POST'], cors=cors_config)
@exception_handler
def add():
    """Create a new job"""
    request = api.current_request
    payload = request.json_body
    model = JobModel.model_validate(payload)
    inserted_model = service.add_model(model)
    return Response(body=inserted_model.model_dump_json(exclude_none=True), status_code=HTTPStatus.CREATED)


@api.route(JOB_URL, methods=['GET'], cors=cors_config)
@exception_handler
def get_all_with_criteria():
    """Get all jobs with filtering and pagination"""
    query_params = api.current_request.query_params or {}
    criteria = Filters(**query_params)
    models = service.get_all_models(filters=criteria)
    return Response(body=models.model_dump_json(exclude_none=True))


@api.route(JOB_URL + '/{_id}', methods=['GET'], cors=cors_config)
@exception_handler
def get_by_id(_id):
    """Get job by ID"""
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


@api.route(JOB_URL + '/entreprise/{entreprise_id}', methods=['GET'], cors=cors_config)
@exception_handler
def get_by_entreprise(entreprise_id):
    """Get all jobs for a specific entreprise"""
    if not entreprise_id:
        message_response = MessageResponseHelper.build(
            ResponseTypeEnum.ERROR,
            Messages.REQUIRED_ENTREPRISE_ID)
        return Response(message_response, status_code=HTTPStatus.BAD_REQUEST)
    
    query_params = api.current_request.query_params or {}
    criteria = Filters(**query_params)
    models = service.get_by_entreprise(entreprise_id, criteria)
    return Response(body=models.model_dump_json(exclude_none=True))


@api.route(JOB_URL + '/status/{status}', methods=['GET'], cors=cors_config)
@exception_handler
def get_by_status(status):
    """Get all jobs with a specific status"""
    if not status:
        message_response = MessageResponseHelper.build(
            ResponseTypeEnum.ERROR,
            Messages.REQUIRED_STATUS)
        return Response(message_response, status_code=HTTPStatus.BAD_REQUEST)
    
    query_params = api.current_request.query_params or {}
    criteria = Filters(**query_params)
    models = service.get_by_status(status, criteria)
    return Response(body=models.model_dump_json(exclude_none=True))


@api.route(JOB_URL + '/{_id}', methods=['PATCH'], cors=cors_config)
@exception_handler
def patch(_id):
    """Partially update a job"""
    if not _id:
        raise JobException(Messages.REQUIRED_ID)

    existing_job = service.get_model(_id)
    if not existing_job:
        message_response = MessageResponseHelper.build(
            ResponseTypeEnum.ERROR,
            Messages.ERROR_NOT_FOUND
        )
        return Response(message_response, status_code=HTTPStatus.NOT_FOUND)

    request = api.current_request
    job_patch_model = JobPatchModel.model_validate(request.json_body)

    if not any(job_patch_model.model_dump(exclude_none=True).keys()):
        job_patch_model_keys = list(job_patch_model.model_fields.keys())
        message = Messages.UNAUTHORIZED_FIELDS.format(allowed_fields=job_patch_model_keys)
        raise JobException(message)

    if not service.check_changes(existing_job, job_patch_model):
        return Response(body="", status_code=HTTPStatus.NO_CONTENT)

    # Update fields
    service.update_title(_id, job_patch_model.title)
    service.update_description(_id, job_patch_model.description)
    service.update_location(_id, job_patch_model.location)
    service.update_contract_type(_id, job_patch_model.contractType)
    service.update_remote(_id, job_patch_model.remote)
    service.update_salary_range(_id, job_patch_model.salaryRange)
    service.update_entreprise_id(_id, job_patch_model.entrepriseId)
    service.update_status(_id, job_patch_model.status)
    service.update_expires_at(_id, job_patch_model.expiresAt)

    patched_model = service.get_model(_id)

    return Response(body=patched_model.model_dump_json(exclude_none=True))


@api.route(JOB_URL + '/{_id}', methods=['DELETE'], cors=cors_config)
@exception_handler
def delete_by_id(_id):
    """Delete a job"""
    if not _id:
        raise JobException(Messages.REQUIRED_ID)

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
