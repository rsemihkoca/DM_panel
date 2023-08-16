from fastapi import APIRouter, UploadFile, File, Form, Query, Depends
from starlette.requests import Request
from database.schemas.responses import
from database.schemas.parameters import
from .responses import DatasetsResponse, SuccessCreateResponse, DatasetResponse
from api_models.parameters import DatasetCreate, DatasetUpdate

from platml.utils.responses import success_data_response, handle_exception
from platml.utils.constants import ErrorMessages, ErrorCodes, VisualizationTypes, Constants
from platml.utils.helpers import process_params_to_be_logged

router = APIRouter()

@router.post("", summary="Used for saving dataset metadata", response_model=SuccessCreateResponse)
def save_dataset_metadata(request: Request, dataset: DatasetCreate):
    operation_log = request.app.logger.start_service_operation("save_dataset_metadata", request)\
        .add_field(Constants.USERNAME, dataset.created_by)
    try:
        operation_log.add_field(Constants.PARAMS, process_params_to_be_logged(dataset, request.app.logger))
        dataset_id, _ = request.app.controller.save_dataset_metadata(dataset.name, dataset.path, dataset.created_by,
                                                                     dataset.size, dataset.row, dataset.column,
                                                                     dataset.data_source_id, dataset.sql_query,
                                                                     dataset.ingest_flow_id, dataset.status)
        operation_log.succeed()
        return SuccessCreateResponse(data=dataset_id)
    except Exception as e:
        return handle_exception(operation_log, e)