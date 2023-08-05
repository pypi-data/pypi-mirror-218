"""
Type annotations for sagemaker-a2i-runtime service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_a2i_runtime/type_defs/)

Usage::

    ```python
    from mypy_boto3_sagemaker_a2i_runtime.type_defs import DeleteHumanLoopRequestRequestTypeDef

    data: DeleteHumanLoopRequestRequestTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence, Union

from .literals import ContentClassifierType, HumanLoopStatusType, SortOrderType

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "DeleteHumanLoopRequestRequestTypeDef",
    "DescribeHumanLoopRequestRequestTypeDef",
    "HumanLoopOutputTypeDef",
    "HumanLoopDataAttributesTypeDef",
    "HumanLoopInputTypeDef",
    "HumanLoopSummaryTypeDef",
    "ListHumanLoopsRequestListHumanLoopsPaginateTypeDef",
    "ListHumanLoopsRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "ResponseMetadataTypeDef",
    "StartHumanLoopResponseTypeDef",
    "StopHumanLoopRequestRequestTypeDef",
    "DescribeHumanLoopResponseTypeDef",
    "StartHumanLoopRequestRequestTypeDef",
    "ListHumanLoopsResponseTypeDef",
)

DeleteHumanLoopRequestRequestTypeDef = TypedDict(
    "DeleteHumanLoopRequestRequestTypeDef",
    {
        "HumanLoopName": str,
    },
)

DescribeHumanLoopRequestRequestTypeDef = TypedDict(
    "DescribeHumanLoopRequestRequestTypeDef",
    {
        "HumanLoopName": str,
    },
)

HumanLoopOutputTypeDef = TypedDict(
    "HumanLoopOutputTypeDef",
    {
        "OutputS3Uri": str,
    },
)

HumanLoopDataAttributesTypeDef = TypedDict(
    "HumanLoopDataAttributesTypeDef",
    {
        "ContentClassifiers": Sequence[ContentClassifierType],
    },
)

HumanLoopInputTypeDef = TypedDict(
    "HumanLoopInputTypeDef",
    {
        "InputContent": str,
    },
)

HumanLoopSummaryTypeDef = TypedDict(
    "HumanLoopSummaryTypeDef",
    {
        "HumanLoopName": str,
        "HumanLoopStatus": HumanLoopStatusType,
        "CreationTime": datetime,
        "FailureReason": str,
        "FlowDefinitionArn": str,
    },
    total=False,
)

_RequiredListHumanLoopsRequestListHumanLoopsPaginateTypeDef = TypedDict(
    "_RequiredListHumanLoopsRequestListHumanLoopsPaginateTypeDef",
    {
        "FlowDefinitionArn": str,
    },
)
_OptionalListHumanLoopsRequestListHumanLoopsPaginateTypeDef = TypedDict(
    "_OptionalListHumanLoopsRequestListHumanLoopsPaginateTypeDef",
    {
        "CreationTimeAfter": Union[datetime, str],
        "CreationTimeBefore": Union[datetime, str],
        "SortOrder": SortOrderType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

class ListHumanLoopsRequestListHumanLoopsPaginateTypeDef(
    _RequiredListHumanLoopsRequestListHumanLoopsPaginateTypeDef,
    _OptionalListHumanLoopsRequestListHumanLoopsPaginateTypeDef,
):
    pass

_RequiredListHumanLoopsRequestRequestTypeDef = TypedDict(
    "_RequiredListHumanLoopsRequestRequestTypeDef",
    {
        "FlowDefinitionArn": str,
    },
)
_OptionalListHumanLoopsRequestRequestTypeDef = TypedDict(
    "_OptionalListHumanLoopsRequestRequestTypeDef",
    {
        "CreationTimeAfter": Union[datetime, str],
        "CreationTimeBefore": Union[datetime, str],
        "SortOrder": SortOrderType,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListHumanLoopsRequestRequestTypeDef(
    _RequiredListHumanLoopsRequestRequestTypeDef, _OptionalListHumanLoopsRequestRequestTypeDef
):
    pass

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

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

StartHumanLoopResponseTypeDef = TypedDict(
    "StartHumanLoopResponseTypeDef",
    {
        "HumanLoopArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StopHumanLoopRequestRequestTypeDef = TypedDict(
    "StopHumanLoopRequestRequestTypeDef",
    {
        "HumanLoopName": str,
    },
)

DescribeHumanLoopResponseTypeDef = TypedDict(
    "DescribeHumanLoopResponseTypeDef",
    {
        "CreationTime": datetime,
        "FailureReason": str,
        "FailureCode": str,
        "HumanLoopStatus": HumanLoopStatusType,
        "HumanLoopName": str,
        "HumanLoopArn": str,
        "FlowDefinitionArn": str,
        "HumanLoopOutput": HumanLoopOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredStartHumanLoopRequestRequestTypeDef = TypedDict(
    "_RequiredStartHumanLoopRequestRequestTypeDef",
    {
        "HumanLoopName": str,
        "FlowDefinitionArn": str,
        "HumanLoopInput": HumanLoopInputTypeDef,
    },
)
_OptionalStartHumanLoopRequestRequestTypeDef = TypedDict(
    "_OptionalStartHumanLoopRequestRequestTypeDef",
    {
        "DataAttributes": HumanLoopDataAttributesTypeDef,
    },
    total=False,
)

class StartHumanLoopRequestRequestTypeDef(
    _RequiredStartHumanLoopRequestRequestTypeDef, _OptionalStartHumanLoopRequestRequestTypeDef
):
    pass

ListHumanLoopsResponseTypeDef = TypedDict(
    "ListHumanLoopsResponseTypeDef",
    {
        "HumanLoopSummaries": List[HumanLoopSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)
