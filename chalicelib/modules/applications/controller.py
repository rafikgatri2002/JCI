from http import HTTPStatus
from fastapi import APIRouter, Query, Path, Body, status
from fastapi.responses import JSONResponse, Response
from .service import ApplicationService
from ...common.enums.response_type_enum import ResponseTypeEnum
from ...common.exceptions.exception import ApplicationException
from ...common.helpers.error_middleware import exception_handler
from ...common.helpers.filters import Filters
from ...common.helpers.message_response_helper import MessageResponseHelper
from .messages import Messages
from .model import ApplicationModel, ApplicationPatchModel

service = ApplicationService()
router = APIRouter(prefix='/applications', tags=['applications'])


@router.post('', status_code=status.HTTP_201_CREATED)
@exception_handler
def add(payload: ApplicationModel):
    """Create a new application"""
    inserted_model = service.add_model(payload)
    return JSONResponse(
        content=inserted_model.model_dump(exclude_none=True, mode='json'),
        status_code=HTTPStatus.CREATED
    )


@router.get('')
@exception_handler
def get_all_with_criteria(
    jobId: str = Query(None),
    candidatId: str = Query(None),
    role: str = Query(None),
    status: str = Query(None),
    email: str = Query(None),
    skip: int = Query(0),
    limit: int = Query(100)
):
    """Get all applications with filtering and pagination"""
    # If jobId is provided, get applications for that job
    if jobId:
        models = service.get_by_job(jobId)
        return JSONResponse(content=models.model_dump(exclude_none=True, mode='json'))
    
    # If candidatId is provided, get applications for that candidat
    if candidatId:
        models = service.get_by_candidat(candidatId)
        return JSONResponse(content=models.model_dump(exclude_none=True, mode='json'))
    
    criteria = Filters(role=role, status=status, email=email, skip=skip, limit=limit)
    models = service.get_all_models(filters=criteria)
    return JSONResponse(content=models.model_dump(exclude_none=True, mode='json'))


@router.get('/{_id}')
@exception_handler
def get_by_id(_id: str = Path(...)):
    """Get application by ID"""
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
def patch(_id: str = Path(...), application_patch_model: ApplicationPatchModel = Body(...)):
    """Partially update an application"""
    if not _id:
        raise ApplicationException(Messages.REQUIRED_ID)
    
    existing_application = service.get_model(_id)
    if not existing_application:
        message_response = MessageResponseHelper.build(
            ResponseTypeEnum.ERROR,
            Messages.ERROR_NOT_FOUND
        )
        return JSONResponse(content=message_response, status_code=HTTPStatus.NOT_FOUND)
    
    if not any(application_patch_model.model_dump(exclude_none=True).keys()):
        application_patch_model_keys = list(application_patch_model.model_fields.keys())
        message = Messages.UNAUTHORIZED_FIELDS.format(allowed_fields=application_patch_model_keys)
        raise ApplicationException(message)
    
    if not service.check_changes(existing_application, application_patch_model):
        return Response(content="", status_code=HTTPStatus.NO_CONTENT)
    
    # Update fields
    service.update_application(_id, application_patch_model)
    
    patched_model = service.get_model(_id)
    
    return JSONResponse(content=patched_model.model_dump(exclude_none=True, mode='json'))


@router.delete('/{_id}')
@exception_handler
def delete_by_id(_id: str = Path(...)):
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
    return JSONResponse(content=message_response, status_code=status_code)
