import collections
import enum
import grpc

from venus912_dashboard.protobuf import venus912_pb2_grpc, venus912_pb2
from venus912_dashboard.core import venus912DashboardClient


@enum.unique
class Scenario(enum.Enum):
    SERVICE_INFO = 'service_info'
    UPLOAD_MODEL = 'upload_model'
    SWITCH_MODEL = 'switch_model'
    UPLOAD_EVALUATION_DATA = 'upload_evaluation_data'
    EVALUATE_MODEL = 'evaluate_model'
    EVALUATION_RESULT = 'evaluation_result'


class Outcome(collections.namedtuple('Outcome', ('kind', 'code', 'details'))):
    """Outcome of a client application scenario.
    Attributes:
      kind: A Kind value describing the overall kind of scenario execution.
      code: A grpc.StatusCode value. Only valid if kind is Kind.RPC_ERROR.
      details: A status details string. Only valid if kind is Kind.RPC_ERROR.
    """

    @enum.unique
    class Kind(enum.Enum):
        SATISFACTORY = 'satisfactory'
        UNSATISFACTORY = 'unsatisfactory'
        RPC_ERROR = 'rpc error'


_SATISFACTORY_OUTCOME = Outcome(Outcome.Kind.SATISFACTORY, None, None)
_UNSATISFACTORY_OUTCOME = Outcome(Outcome.Kind.UNSATISFACTORY, None, None)


@enum.unique
class Request(enum.Enum):
    UPLOAD_MODEL_REQUEST = ('my_path', b'data')
    SWITCH_MODEL_REQUEST = ('new_path',)
    UPLOAD_EVALUATION_DATA_REQUEST = (b'data', 'my_path')
    EVALUATE_MODEL_REQUEST = (b'data', 'my_path1', 'my_path2')
    EVALUATION_RESULT_REQUEST = ('my_path1', 'my_path2')


@enum.unique
class Response(enum.Enum):
    SERVICE_INFO_RESPONSE = venus912_pb2.ServiceInfoResponse(
        application_name="sample", service_name="service", service_level="development")
    MODEL_RESPONSE = venus912_pb2.ModelResponse(status=1, message="Success.")
    UPLOAD_EVALUATION_DATA_RESPONSE = venus912_pb2.UploadEvaluationDataResponse(status=1, message="Success.")
    METRICS = venus912_pb2.EvaluationMetrics(
        num=1, accuracy=1.0, precision=[1.0], recall=[1.0], fvalue=[1.0], option=dict(),
        label=[venus912_pb2.IO(str=venus912_pb2.ArrString(val=["label"]))])
    EVALUATE_MODEL_RESPONSE = venus912_pb2.EvaluateModelResponse(metrics=METRICS)
    EVALUATION_RESULT_RESPONSE = venus912_pb2.EvaluationResultResponse(
        metrics=METRICS,
        detail=[venus912_pb2.EvaluationResultResponse.Detail(
            input=venus912_pb2.IO(str=venus912_pb2.ArrString(val=["input"])),
            label=venus912_pb2.IO(str=venus912_pb2.ArrString(val=["label"])),
            output=venus912_pb2.IO(str=venus912_pb2.ArrString(val=["output"])),
            score=[1.0],
            is_correct=True)])


def _assertServiceInfoResponse(response):
    if Response.SERVICE_INFO_RESPONSE.value.application_name == response["application_name"] and \
            Response.SERVICE_INFO_RESPONSE.value.service_name == response["service_name"] and \
            Response.SERVICE_INFO_RESPONSE.value.service_level == response["service_level"]:
        return True
    return False


def _assertModelResponse(response):
    if Response.MODEL_RESPONSE.value.status == response["status"] and \
            Response.MODEL_RESPONSE.value.message == response["message"]:
        return True
    return False


def _assertEvaluationResultResponse(response_iterator):
    try:
        next(response_iterator)
    except StopIteration:
        return True
    else:
        return False


def _run_service_info(client: venus912DashboardClient):
    response = client.run_service_info()
    if _assertServiceInfoResponse(response):
        return _SATISFACTORY_OUTCOME
    else:
        return _UNSATISFACTORY_OUTCOME


def _run_upload_model(client: venus912DashboardClient):
    response, call = client.stub.UploadModel.with_call(
        iter((Request.UPLOAD_MODEL_REQUEST.value,) * 3))
    if Response.MODEL_RESPONSE.value == response and call.code() is grpc.StatusCode.OK:
        return _SATISFACTORY_OUTCOME
    else:
        return _UNSATISFACTORY_OUTCOME


def _run_switch_service_model_assignment(client: venus912DashboardClient):
    response = client.run_switch_service_model_assignment(*Request.SWITCH_MODEL_REQUEST.value)
    if _assertModelResponse(response):
        return _SATISFACTORY_OUTCOME
    else:
        return _UNSATISFACTORY_OUTCOME


def _run_upload_evaluation_data(client: venus912DashboardClient):
    response, call = client.stub.UploadEvaluationData.with_call(
        iter((Request.UPLOAD_EVALUATION_DATA_REQUEST.value,) * 3))
    if Response.UPLOAD_EVALUATION_DATA_RESPONSE.value == response and call.code() is grpc.StatusCode.OK:
        return _SATISFACTORY_OUTCOME
    else:
        return _UNSATISFACTORY_OUTCOME


def _run_evaluate_model(client: venus912DashboardClient):
    response, call = client.stub.EvaluateModel.with_call(
        iter((Request.EVALUATE_MODEL_REQUEST.value,) * 3))
    if Response.EVALUATE_MODEL_RESPONSE.value == response and call.code() is grpc.StatusCode.OK:
        return _SATISFACTORY_OUTCOME
    else:
        return _UNSATISFACTORY_OUTCOME


def _run_evaluation_data(client: venus912DashboardClient):
    response_iterator = client.run_evaluation_data(*Request.EVALUATION_RESULT_REQUEST.value)
    if _assertEvaluationResultResponse(response_iterator):
        return _SATISFACTORY_OUTCOME
    else:
        return _UNSATISFACTORY_OUTCOME


_IMPLEMENTATIONS = {
    Scenario.SERVICE_INFO: _run_service_info,
    Scenario.UPLOAD_MODEL: _run_upload_model,
    Scenario.SWITCH_MODEL: _run_switch_service_model_assignment,
    Scenario.UPLOAD_EVALUATION_DATA: _run_upload_evaluation_data,
    Scenario.EVALUATE_MODEL: _run_evaluate_model,
    Scenario.EVALUATION_RESULT: _run_evaluation_data,
}


def run(scenario, channel):
    stub = venus912_pb2_grpc.venus912DashboardStub(channel)
    client = venus912DashboardClient(
        host="example.com", port=80, application_name="venus912-sample",
        service_level="development", venus912_grpc_version='v2')
    client.stub = stub
    try:
        return _IMPLEMENTATIONS[scenario](client)
    except grpc.RpcError as rpc_error:
        return Outcome(Outcome.Kind.RPC_ERROR, rpc_error.code(),
                       rpc_error.details())
