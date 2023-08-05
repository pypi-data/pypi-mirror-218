"""
Type annotations for braket service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_braket/type_defs/)

Usage::

    ```python
    from mypy_boto3_braket.type_defs import ContainerImageTypeDef

    data: ContainerImageTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    CancellationStatusType,
    CompressionTypeType,
    DeviceStatusType,
    DeviceTypeType,
    InstanceTypeType,
    JobEventTypeType,
    JobPrimaryStatusType,
    QuantumTaskStatusType,
    SearchJobsFilterOperatorType,
    SearchQuantumTasksFilterOperatorType,
)

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "ContainerImageTypeDef",
    "ScriptModeConfigTypeDef",
    "CancelJobRequestRequestTypeDef",
    "CancelJobResponseTypeDef",
    "CancelQuantumTaskRequestRequestTypeDef",
    "CancelQuantumTaskResponseTypeDef",
    "DeviceConfigTypeDef",
    "InstanceConfigTypeDef",
    "JobCheckpointConfigTypeDef",
    "JobOutputDataConfigTypeDef",
    "JobStoppingConditionTypeDef",
    "CreateJobResponseTypeDef",
    "CreateQuantumTaskRequestRequestTypeDef",
    "CreateQuantumTaskResponseTypeDef",
    "S3DataSourceTypeDef",
    "DeviceSummaryTypeDef",
    "GetDeviceRequestRequestTypeDef",
    "GetDeviceResponseTypeDef",
    "GetJobRequestRequestTypeDef",
    "JobEventDetailsTypeDef",
    "GetQuantumTaskRequestRequestTypeDef",
    "GetQuantumTaskResponseTypeDef",
    "JobSummaryTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PaginatorConfigTypeDef",
    "QuantumTaskSummaryTypeDef",
    "ResponseMetadataTypeDef",
    "SearchDevicesFilterTypeDef",
    "SearchJobsFilterTypeDef",
    "SearchQuantumTasksFilterTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "AlgorithmSpecificationTypeDef",
    "DataSourceTypeDef",
    "SearchDevicesResponseTypeDef",
    "SearchJobsResponseTypeDef",
    "SearchQuantumTasksResponseTypeDef",
    "SearchDevicesRequestRequestTypeDef",
    "SearchDevicesRequestSearchDevicesPaginateTypeDef",
    "SearchJobsRequestRequestTypeDef",
    "SearchJobsRequestSearchJobsPaginateTypeDef",
    "SearchQuantumTasksRequestRequestTypeDef",
    "SearchQuantumTasksRequestSearchQuantumTasksPaginateTypeDef",
    "InputFileConfigTypeDef",
    "CreateJobRequestRequestTypeDef",
    "GetJobResponseTypeDef",
)

ContainerImageTypeDef = TypedDict(
    "ContainerImageTypeDef",
    {
        "uri": str,
    },
)

_RequiredScriptModeConfigTypeDef = TypedDict(
    "_RequiredScriptModeConfigTypeDef",
    {
        "entryPoint": str,
        "s3Uri": str,
    },
)
_OptionalScriptModeConfigTypeDef = TypedDict(
    "_OptionalScriptModeConfigTypeDef",
    {
        "compressionType": CompressionTypeType,
    },
    total=False,
)

class ScriptModeConfigTypeDef(_RequiredScriptModeConfigTypeDef, _OptionalScriptModeConfigTypeDef):
    pass

CancelJobRequestRequestTypeDef = TypedDict(
    "CancelJobRequestRequestTypeDef",
    {
        "jobArn": str,
    },
)

CancelJobResponseTypeDef = TypedDict(
    "CancelJobResponseTypeDef",
    {
        "cancellationStatus": CancellationStatusType,
        "jobArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CancelQuantumTaskRequestRequestTypeDef = TypedDict(
    "CancelQuantumTaskRequestRequestTypeDef",
    {
        "clientToken": str,
        "quantumTaskArn": str,
    },
)

CancelQuantumTaskResponseTypeDef = TypedDict(
    "CancelQuantumTaskResponseTypeDef",
    {
        "cancellationStatus": CancellationStatusType,
        "quantumTaskArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeviceConfigTypeDef = TypedDict(
    "DeviceConfigTypeDef",
    {
        "device": str,
    },
)

_RequiredInstanceConfigTypeDef = TypedDict(
    "_RequiredInstanceConfigTypeDef",
    {
        "instanceType": InstanceTypeType,
        "volumeSizeInGb": int,
    },
)
_OptionalInstanceConfigTypeDef = TypedDict(
    "_OptionalInstanceConfigTypeDef",
    {
        "instanceCount": int,
    },
    total=False,
)

class InstanceConfigTypeDef(_RequiredInstanceConfigTypeDef, _OptionalInstanceConfigTypeDef):
    pass

_RequiredJobCheckpointConfigTypeDef = TypedDict(
    "_RequiredJobCheckpointConfigTypeDef",
    {
        "s3Uri": str,
    },
)
_OptionalJobCheckpointConfigTypeDef = TypedDict(
    "_OptionalJobCheckpointConfigTypeDef",
    {
        "localPath": str,
    },
    total=False,
)

class JobCheckpointConfigTypeDef(
    _RequiredJobCheckpointConfigTypeDef, _OptionalJobCheckpointConfigTypeDef
):
    pass

_RequiredJobOutputDataConfigTypeDef = TypedDict(
    "_RequiredJobOutputDataConfigTypeDef",
    {
        "s3Path": str,
    },
)
_OptionalJobOutputDataConfigTypeDef = TypedDict(
    "_OptionalJobOutputDataConfigTypeDef",
    {
        "kmsKeyId": str,
    },
    total=False,
)

class JobOutputDataConfigTypeDef(
    _RequiredJobOutputDataConfigTypeDef, _OptionalJobOutputDataConfigTypeDef
):
    pass

JobStoppingConditionTypeDef = TypedDict(
    "JobStoppingConditionTypeDef",
    {
        "maxRuntimeInSeconds": int,
    },
    total=False,
)

CreateJobResponseTypeDef = TypedDict(
    "CreateJobResponseTypeDef",
    {
        "jobArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateQuantumTaskRequestRequestTypeDef = TypedDict(
    "_RequiredCreateQuantumTaskRequestRequestTypeDef",
    {
        "action": str,
        "clientToken": str,
        "deviceArn": str,
        "outputS3Bucket": str,
        "outputS3KeyPrefix": str,
        "shots": int,
    },
)
_OptionalCreateQuantumTaskRequestRequestTypeDef = TypedDict(
    "_OptionalCreateQuantumTaskRequestRequestTypeDef",
    {
        "deviceParameters": str,
        "jobToken": str,
        "tags": Mapping[str, str],
    },
    total=False,
)

class CreateQuantumTaskRequestRequestTypeDef(
    _RequiredCreateQuantumTaskRequestRequestTypeDef, _OptionalCreateQuantumTaskRequestRequestTypeDef
):
    pass

CreateQuantumTaskResponseTypeDef = TypedDict(
    "CreateQuantumTaskResponseTypeDef",
    {
        "quantumTaskArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

S3DataSourceTypeDef = TypedDict(
    "S3DataSourceTypeDef",
    {
        "s3Uri": str,
    },
)

DeviceSummaryTypeDef = TypedDict(
    "DeviceSummaryTypeDef",
    {
        "deviceArn": str,
        "deviceName": str,
        "deviceStatus": DeviceStatusType,
        "deviceType": DeviceTypeType,
        "providerName": str,
    },
)

GetDeviceRequestRequestTypeDef = TypedDict(
    "GetDeviceRequestRequestTypeDef",
    {
        "deviceArn": str,
    },
)

GetDeviceResponseTypeDef = TypedDict(
    "GetDeviceResponseTypeDef",
    {
        "deviceArn": str,
        "deviceCapabilities": str,
        "deviceName": str,
        "deviceStatus": DeviceStatusType,
        "deviceType": DeviceTypeType,
        "providerName": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetJobRequestRequestTypeDef = TypedDict(
    "GetJobRequestRequestTypeDef",
    {
        "jobArn": str,
    },
)

JobEventDetailsTypeDef = TypedDict(
    "JobEventDetailsTypeDef",
    {
        "eventType": JobEventTypeType,
        "message": str,
        "timeOfEvent": datetime,
    },
    total=False,
)

GetQuantumTaskRequestRequestTypeDef = TypedDict(
    "GetQuantumTaskRequestRequestTypeDef",
    {
        "quantumTaskArn": str,
    },
)

GetQuantumTaskResponseTypeDef = TypedDict(
    "GetQuantumTaskResponseTypeDef",
    {
        "createdAt": datetime,
        "deviceArn": str,
        "deviceParameters": str,
        "endedAt": datetime,
        "failureReason": str,
        "jobArn": str,
        "outputS3Bucket": str,
        "outputS3Directory": str,
        "quantumTaskArn": str,
        "shots": int,
        "status": QuantumTaskStatusType,
        "tags": Dict[str, str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredJobSummaryTypeDef = TypedDict(
    "_RequiredJobSummaryTypeDef",
    {
        "createdAt": datetime,
        "device": str,
        "jobArn": str,
        "jobName": str,
        "status": JobPrimaryStatusType,
    },
)
_OptionalJobSummaryTypeDef = TypedDict(
    "_OptionalJobSummaryTypeDef",
    {
        "endedAt": datetime,
        "startedAt": datetime,
        "tags": Dict[str, str],
    },
    total=False,
)

class JobSummaryTypeDef(_RequiredJobSummaryTypeDef, _OptionalJobSummaryTypeDef):
    pass

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "tags": Dict[str, str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

_RequiredQuantumTaskSummaryTypeDef = TypedDict(
    "_RequiredQuantumTaskSummaryTypeDef",
    {
        "createdAt": datetime,
        "deviceArn": str,
        "outputS3Bucket": str,
        "outputS3Directory": str,
        "quantumTaskArn": str,
        "shots": int,
        "status": QuantumTaskStatusType,
    },
)
_OptionalQuantumTaskSummaryTypeDef = TypedDict(
    "_OptionalQuantumTaskSummaryTypeDef",
    {
        "endedAt": datetime,
        "tags": Dict[str, str],
    },
    total=False,
)

class QuantumTaskSummaryTypeDef(
    _RequiredQuantumTaskSummaryTypeDef, _OptionalQuantumTaskSummaryTypeDef
):
    pass

ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HostId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
    },
)

SearchDevicesFilterTypeDef = TypedDict(
    "SearchDevicesFilterTypeDef",
    {
        "name": str,
        "values": Sequence[str],
    },
)

SearchJobsFilterTypeDef = TypedDict(
    "SearchJobsFilterTypeDef",
    {
        "name": str,
        "operator": SearchJobsFilterOperatorType,
        "values": Sequence[str],
    },
)

SearchQuantumTasksFilterTypeDef = TypedDict(
    "SearchQuantumTasksFilterTypeDef",
    {
        "name": str,
        "operator": SearchQuantumTasksFilterOperatorType,
        "values": Sequence[str],
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Mapping[str, str],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)

AlgorithmSpecificationTypeDef = TypedDict(
    "AlgorithmSpecificationTypeDef",
    {
        "containerImage": ContainerImageTypeDef,
        "scriptModeConfig": ScriptModeConfigTypeDef,
    },
    total=False,
)

DataSourceTypeDef = TypedDict(
    "DataSourceTypeDef",
    {
        "s3DataSource": S3DataSourceTypeDef,
    },
)

SearchDevicesResponseTypeDef = TypedDict(
    "SearchDevicesResponseTypeDef",
    {
        "devices": List[DeviceSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

SearchJobsResponseTypeDef = TypedDict(
    "SearchJobsResponseTypeDef",
    {
        "jobs": List[JobSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

SearchQuantumTasksResponseTypeDef = TypedDict(
    "SearchQuantumTasksResponseTypeDef",
    {
        "nextToken": str,
        "quantumTasks": List[QuantumTaskSummaryTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredSearchDevicesRequestRequestTypeDef = TypedDict(
    "_RequiredSearchDevicesRequestRequestTypeDef",
    {
        "filters": Sequence[SearchDevicesFilterTypeDef],
    },
)
_OptionalSearchDevicesRequestRequestTypeDef = TypedDict(
    "_OptionalSearchDevicesRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

class SearchDevicesRequestRequestTypeDef(
    _RequiredSearchDevicesRequestRequestTypeDef, _OptionalSearchDevicesRequestRequestTypeDef
):
    pass

_RequiredSearchDevicesRequestSearchDevicesPaginateTypeDef = TypedDict(
    "_RequiredSearchDevicesRequestSearchDevicesPaginateTypeDef",
    {
        "filters": Sequence[SearchDevicesFilterTypeDef],
    },
)
_OptionalSearchDevicesRequestSearchDevicesPaginateTypeDef = TypedDict(
    "_OptionalSearchDevicesRequestSearchDevicesPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

class SearchDevicesRequestSearchDevicesPaginateTypeDef(
    _RequiredSearchDevicesRequestSearchDevicesPaginateTypeDef,
    _OptionalSearchDevicesRequestSearchDevicesPaginateTypeDef,
):
    pass

_RequiredSearchJobsRequestRequestTypeDef = TypedDict(
    "_RequiredSearchJobsRequestRequestTypeDef",
    {
        "filters": Sequence[SearchJobsFilterTypeDef],
    },
)
_OptionalSearchJobsRequestRequestTypeDef = TypedDict(
    "_OptionalSearchJobsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

class SearchJobsRequestRequestTypeDef(
    _RequiredSearchJobsRequestRequestTypeDef, _OptionalSearchJobsRequestRequestTypeDef
):
    pass

_RequiredSearchJobsRequestSearchJobsPaginateTypeDef = TypedDict(
    "_RequiredSearchJobsRequestSearchJobsPaginateTypeDef",
    {
        "filters": Sequence[SearchJobsFilterTypeDef],
    },
)
_OptionalSearchJobsRequestSearchJobsPaginateTypeDef = TypedDict(
    "_OptionalSearchJobsRequestSearchJobsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

class SearchJobsRequestSearchJobsPaginateTypeDef(
    _RequiredSearchJobsRequestSearchJobsPaginateTypeDef,
    _OptionalSearchJobsRequestSearchJobsPaginateTypeDef,
):
    pass

_RequiredSearchQuantumTasksRequestRequestTypeDef = TypedDict(
    "_RequiredSearchQuantumTasksRequestRequestTypeDef",
    {
        "filters": Sequence[SearchQuantumTasksFilterTypeDef],
    },
)
_OptionalSearchQuantumTasksRequestRequestTypeDef = TypedDict(
    "_OptionalSearchQuantumTasksRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

class SearchQuantumTasksRequestRequestTypeDef(
    _RequiredSearchQuantumTasksRequestRequestTypeDef,
    _OptionalSearchQuantumTasksRequestRequestTypeDef,
):
    pass

_RequiredSearchQuantumTasksRequestSearchQuantumTasksPaginateTypeDef = TypedDict(
    "_RequiredSearchQuantumTasksRequestSearchQuantumTasksPaginateTypeDef",
    {
        "filters": Sequence[SearchQuantumTasksFilterTypeDef],
    },
)
_OptionalSearchQuantumTasksRequestSearchQuantumTasksPaginateTypeDef = TypedDict(
    "_OptionalSearchQuantumTasksRequestSearchQuantumTasksPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

class SearchQuantumTasksRequestSearchQuantumTasksPaginateTypeDef(
    _RequiredSearchQuantumTasksRequestSearchQuantumTasksPaginateTypeDef,
    _OptionalSearchQuantumTasksRequestSearchQuantumTasksPaginateTypeDef,
):
    pass

_RequiredInputFileConfigTypeDef = TypedDict(
    "_RequiredInputFileConfigTypeDef",
    {
        "channelName": str,
        "dataSource": DataSourceTypeDef,
    },
)
_OptionalInputFileConfigTypeDef = TypedDict(
    "_OptionalInputFileConfigTypeDef",
    {
        "contentType": str,
    },
    total=False,
)

class InputFileConfigTypeDef(_RequiredInputFileConfigTypeDef, _OptionalInputFileConfigTypeDef):
    pass

_RequiredCreateJobRequestRequestTypeDef = TypedDict(
    "_RequiredCreateJobRequestRequestTypeDef",
    {
        "algorithmSpecification": AlgorithmSpecificationTypeDef,
        "clientToken": str,
        "deviceConfig": DeviceConfigTypeDef,
        "instanceConfig": InstanceConfigTypeDef,
        "jobName": str,
        "outputDataConfig": JobOutputDataConfigTypeDef,
        "roleArn": str,
    },
)
_OptionalCreateJobRequestRequestTypeDef = TypedDict(
    "_OptionalCreateJobRequestRequestTypeDef",
    {
        "checkpointConfig": JobCheckpointConfigTypeDef,
        "hyperParameters": Mapping[str, str],
        "inputDataConfig": Sequence[InputFileConfigTypeDef],
        "stoppingCondition": JobStoppingConditionTypeDef,
        "tags": Mapping[str, str],
    },
    total=False,
)

class CreateJobRequestRequestTypeDef(
    _RequiredCreateJobRequestRequestTypeDef, _OptionalCreateJobRequestRequestTypeDef
):
    pass

GetJobResponseTypeDef = TypedDict(
    "GetJobResponseTypeDef",
    {
        "algorithmSpecification": AlgorithmSpecificationTypeDef,
        "billableDuration": int,
        "checkpointConfig": JobCheckpointConfigTypeDef,
        "createdAt": datetime,
        "deviceConfig": DeviceConfigTypeDef,
        "endedAt": datetime,
        "events": List[JobEventDetailsTypeDef],
        "failureReason": str,
        "hyperParameters": Dict[str, str],
        "inputDataConfig": List[InputFileConfigTypeDef],
        "instanceConfig": InstanceConfigTypeDef,
        "jobArn": str,
        "jobName": str,
        "outputDataConfig": JobOutputDataConfigTypeDef,
        "roleArn": str,
        "startedAt": datetime,
        "status": JobPrimaryStatusType,
        "stoppingCondition": JobStoppingConditionTypeDef,
        "tags": Dict[str, str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)
