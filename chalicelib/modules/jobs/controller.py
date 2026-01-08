from http import HTTPStatus
from fastapi import APIRouter, Query, Path, Body, status
from fastapi.responses import JSONResponse, Response
from .service import JobService
from ...common.enums.response_type_enum import ResponseTypeEnum
from ...common.exceptions.exception import JobException
from ...common.helpers.error_middleware import exception_handler
from ...common.helpers.filters import Filters
from ...common.helpers.message_response_helper import MessageResponseHelper
from .messages import Messages
from .model import JobModel, JobPatchModel

service = JobService()
router = APIRouter(prefix='/jobs', tags=['jobs'])


@router.post('', status_code=status.HTTP_201_CREATED)
@exception_handler
def add(payload: JobModel):
    """Create a new job"""
    inserted_model = service.add_model(payload)
    return JSONResponse(
        content=inserted_model.model_dump(exclude_none=True, mode='json'),
        status_code=HTTPStatus.CREATED
    )


@router.get('')
@exception_handler
def get_all_with_criteria(
    entrepriseId: str = Query(None),
    status: str = Query(None),
    role: str = Query(None),
    email: str = Query(None),
    skip: int = Query(0),
    limit: int = Query(100)
):
    """Get all jobs with filtering and pagination"""
    criteria = Filters(role=role, status=status, email=email, skip=skip, limit=limit)
    
    # If entrepriseId is provided, filter by entreprise
    if entrepriseId:
        models = service.get_by_entreprise(entrepriseId, criteria)
        return JSONResponse(content=models.model_dump(exclude_none=True, mode='json'))
    
    # If status is provided (and no entrepriseId), filter by status
    if status:
        models = service.get_by_status(status, criteria)
        return JSONResponse(content=models.model_dump(exclude_none=True, mode='json'))
    
    # Otherwise get all jobs
    models = service.get_all_models(filters=criteria)
    return JSONResponse(content=models.model_dump(exclude_none=True, mode='json'))


@router.get('/{_id}')
@exception_handler
def get_by_id(_id: str = Path(...)):
    """Get job by ID"""
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
def patch(_id: str = Path(...), job_patch_model: JobPatchModel = Body(...)):
    """Partially update a job"""
    if not _id:
        raise JobException(Messages.REQUIRED_ID)

    existing_job = service.get_model(_id)
    if not existing_job:
        message_response = MessageResponseHelper.build(
            ResponseTypeEnum.ERROR,
            Messages.ERROR_NOT_FOUND
        )
        return JSONResponse(content=message_response, status_code=HTTPStatus.NOT_FOUND)

    if not any(job_patch_model.model_dump(exclude_none=True).keys()):
        job_patch_model_keys = list(job_patch_model.model_fields.keys())
        message = Messages.UNAUTHORIZED_FIELDS.format(allowed_fields=job_patch_model_keys)
        raise JobException(message)

    if not service.check_changes(existing_job, job_patch_model):
        return Response(content="", status_code=HTTPStatus.NO_CONTENT)

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

    return JSONResponse(content=patched_model.model_dump(exclude_none=True, mode='json'))


@router.delete('/{_id}')
@exception_handler
def delete_by_id(_id: str = Path(...)):
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
    return JSONResponse(content=message_response, status_code=status_code)
