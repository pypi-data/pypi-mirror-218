"""
Type annotations for s3outposts service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3outposts/type_defs/)

Usage::

    ```python
    from mypy_boto3_s3outposts.type_defs import CreateEndpointRequestRequestTypeDef

    data: CreateEndpointRequestRequestTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List

from .literals import EndpointAccessTypeType, EndpointStatusType

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "CreateEndpointRequestRequestTypeDef",
    "CreateEndpointResultTypeDef",
    "DeleteEndpointRequestRequestTypeDef",
    "EmptyResponseMetadataTypeDef",
    "FailedReasonTypeDef",
    "NetworkInterfaceTypeDef",
    "ListEndpointsRequestListEndpointsPaginateTypeDef",
    "ListEndpointsRequestRequestTypeDef",
    "ListOutpostsWithS3RequestListOutpostsWithS3PaginateTypeDef",
    "ListOutpostsWithS3RequestRequestTypeDef",
    "OutpostTypeDef",
    "ListSharedEndpointsRequestListSharedEndpointsPaginateTypeDef",
    "ListSharedEndpointsRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "ResponseMetadataTypeDef",
    "EndpointTypeDef",
    "ListOutpostsWithS3ResultTypeDef",
    "ListEndpointsResultTypeDef",
    "ListSharedEndpointsResultTypeDef",
)

_RequiredCreateEndpointRequestRequestTypeDef = TypedDict(
    "_RequiredCreateEndpointRequestRequestTypeDef",
    {
        "OutpostId": str,
        "SubnetId": str,
        "SecurityGroupId": str,
    },
)
_OptionalCreateEndpointRequestRequestTypeDef = TypedDict(
    "_OptionalCreateEndpointRequestRequestTypeDef",
    {
        "AccessType": EndpointAccessTypeType,
        "CustomerOwnedIpv4Pool": str,
    },
    total=False,
)


class CreateEndpointRequestRequestTypeDef(
    _RequiredCreateEndpointRequestRequestTypeDef, _OptionalCreateEndpointRequestRequestTypeDef
):
    pass


CreateEndpointResultTypeDef = TypedDict(
    "CreateEndpointResultTypeDef",
    {
        "EndpointArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteEndpointRequestRequestTypeDef = TypedDict(
    "DeleteEndpointRequestRequestTypeDef",
    {
        "EndpointId": str,
        "OutpostId": str,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

FailedReasonTypeDef = TypedDict(
    "FailedReasonTypeDef",
    {
        "ErrorCode": str,
        "Message": str,
    },
    total=False,
)

NetworkInterfaceTypeDef = TypedDict(
    "NetworkInterfaceTypeDef",
    {
        "NetworkInterfaceId": str,
    },
    total=False,
)

ListEndpointsRequestListEndpointsPaginateTypeDef = TypedDict(
    "ListEndpointsRequestListEndpointsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListEndpointsRequestRequestTypeDef = TypedDict(
    "ListEndpointsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListOutpostsWithS3RequestListOutpostsWithS3PaginateTypeDef = TypedDict(
    "ListOutpostsWithS3RequestListOutpostsWithS3PaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListOutpostsWithS3RequestRequestTypeDef = TypedDict(
    "ListOutpostsWithS3RequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

OutpostTypeDef = TypedDict(
    "OutpostTypeDef",
    {
        "OutpostArn": str,
        "OutpostId": str,
        "OwnerId": str,
        "CapacityInBytes": int,
    },
    total=False,
)

_RequiredListSharedEndpointsRequestListSharedEndpointsPaginateTypeDef = TypedDict(
    "_RequiredListSharedEndpointsRequestListSharedEndpointsPaginateTypeDef",
    {
        "OutpostId": str,
    },
)
_OptionalListSharedEndpointsRequestListSharedEndpointsPaginateTypeDef = TypedDict(
    "_OptionalListSharedEndpointsRequestListSharedEndpointsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListSharedEndpointsRequestListSharedEndpointsPaginateTypeDef(
    _RequiredListSharedEndpointsRequestListSharedEndpointsPaginateTypeDef,
    _OptionalListSharedEndpointsRequestListSharedEndpointsPaginateTypeDef,
):
    pass


_RequiredListSharedEndpointsRequestRequestTypeDef = TypedDict(
    "_RequiredListSharedEndpointsRequestRequestTypeDef",
    {
        "OutpostId": str,
    },
)
_OptionalListSharedEndpointsRequestRequestTypeDef = TypedDict(
    "_OptionalListSharedEndpointsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListSharedEndpointsRequestRequestTypeDef(
    _RequiredListSharedEndpointsRequestRequestTypeDef,
    _OptionalListSharedEndpointsRequestRequestTypeDef,
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

EndpointTypeDef = TypedDict(
    "EndpointTypeDef",
    {
        "EndpointArn": str,
        "OutpostsId": str,
        "CidrBlock": str,
        "Status": EndpointStatusType,
        "CreationTime": datetime,
        "NetworkInterfaces": List[NetworkInterfaceTypeDef],
        "VpcId": str,
        "SubnetId": str,
        "SecurityGroupId": str,
        "AccessType": EndpointAccessTypeType,
        "CustomerOwnedIpv4Pool": str,
        "FailedReason": FailedReasonTypeDef,
    },
    total=False,
)

ListOutpostsWithS3ResultTypeDef = TypedDict(
    "ListOutpostsWithS3ResultTypeDef",
    {
        "Outposts": List[OutpostTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListEndpointsResultTypeDef = TypedDict(
    "ListEndpointsResultTypeDef",
    {
        "Endpoints": List[EndpointTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListSharedEndpointsResultTypeDef = TypedDict(
    "ListSharedEndpointsResultTypeDef",
    {
        "Endpoints": List[EndpointTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)
