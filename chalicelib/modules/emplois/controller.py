from http import HTTPStatus
from fastapi import APIRouter, Query, Path, Body, status
from fastapi.responses import JSONResponse, Response
from .service import EmploiService
from ...common.enums.response_type_enum import ResponseTypeEnum
from ...common.exceptions.exception import EmploiException
from ...common.helpers.error_middleware import exception_handler
from ...common.helpers.filters import Filters
from ...common.helpers.message_response_helper import MessageResponseHelper
from .messages import Messages
from .model import EmploiModel, EmploiPatchModel

service = EmploiService()
router = APIRouter(prefix='/emplois', tags=['emplois'])


@router.post('', status_code=status.HTTP_201_CREATED)
@exception_handler
def add(payload: EmploiModel):
    """Create a new emploi"""
    inserted_model = service.add_model(payload)
    return JSONResponse(
        content=inserted_model.model_dump(exclude_none=True, mode='json'),
        status_code=HTTPStatus.CREATED
    )


@router.get('')
@exception_handler
def get_all_with_criteria(
    userId: str = Query(None),
    entrepriseId: str = Query(None),
    role: str = Query(None),
    status: str = Query(None),
    email: str = Query(None),
    skip: int = Query(0),
    limit: int = Query(100)
):
    """Get all emplois with filtering and pagination"""
    # If both userId and entrepriseId are provided, get specific emploi
    if userId and entrepriseId:
        model = service.get_by_user_and_entreprise(userId, entrepriseId)
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
    """Get emploi by ID"""
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
def patch(_id: str = Path(...), emploi_patch_model: EmploiPatchModel = Body(...)):
    """Partially update an emploi"""
    if not _id:
        raise EmploiException(Messages.REQUIRED_ID)
    
    existing_emploi = service.get_model(_id)
    if not existing_emploi:
        message_response = MessageResponseHelper.build(
            ResponseTypeEnum.ERROR,
            Messages.ERROR_NOT_FOUND
        )
        return JSONResponse(content=message_response, status_code=HTTPStatus.NOT_FOUND)
    
    if not any(emploi_patch_model.model_dump(exclude_none=True).keys()):
        emploi_patch_model_keys = list(emploi_patch_model.model_fields.keys())
        message = Messages.UNAUTHORIZED_FIELDS.format(allowed_fields=emploi_patch_model_keys)
        raise EmploiException(message)
    
    if not service.check_changes(existing_emploi, emploi_patch_model):
        return Response(content="", status_code=HTTPStatus.NO_CONTENT)
    
    # Update fields
    service.update_position(_id, emploi_patch_model.position)
    
    patched_model = service.get_model(_id)
    
    return JSONResponse(content=patched_model.model_dump(exclude_none=True, mode='json'))


@router.delete('/{_id}')
@exception_handler
def delete_by_id(_id: str = Path(...)):
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
    return JSONResponse(content=message_response, status_code=status_code)
