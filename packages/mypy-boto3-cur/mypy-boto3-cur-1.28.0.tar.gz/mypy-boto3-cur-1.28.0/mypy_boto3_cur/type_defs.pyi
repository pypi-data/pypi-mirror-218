"""
Type annotations for cur service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cur/type_defs/)

Usage::

    ```python
    from mypy_boto3_cur.type_defs import DeleteReportDefinitionRequestRequestTypeDef

    data: DeleteReportDefinitionRequestRequestTypeDef = {...}
    ```
"""
import sys
from typing import Dict, List

from .literals import (
    AdditionalArtifactType,
    AWSRegionType,
    CompressionFormatType,
    ReportFormatType,
    ReportVersioningType,
    SchemaElementType,
    TimeUnitType,
)

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "DeleteReportDefinitionRequestRequestTypeDef",
    "DeleteReportDefinitionResponseTypeDef",
    "DescribeReportDefinitionsRequestDescribeReportDefinitionsPaginateTypeDef",
    "DescribeReportDefinitionsRequestRequestTypeDef",
    "ReportDefinitionTypeDef",
    "PaginatorConfigTypeDef",
    "ResponseMetadataTypeDef",
    "DescribeReportDefinitionsResponseTypeDef",
    "ModifyReportDefinitionRequestRequestTypeDef",
    "PutReportDefinitionRequestRequestTypeDef",
)

DeleteReportDefinitionRequestRequestTypeDef = TypedDict(
    "DeleteReportDefinitionRequestRequestTypeDef",
    {
        "ReportName": str,
    },
    total=False,
)

DeleteReportDefinitionResponseTypeDef = TypedDict(
    "DeleteReportDefinitionResponseTypeDef",
    {
        "ResponseMessage": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeReportDefinitionsRequestDescribeReportDefinitionsPaginateTypeDef = TypedDict(
    "DescribeReportDefinitionsRequestDescribeReportDefinitionsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

DescribeReportDefinitionsRequestRequestTypeDef = TypedDict(
    "DescribeReportDefinitionsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

_RequiredReportDefinitionTypeDef = TypedDict(
    "_RequiredReportDefinitionTypeDef",
    {
        "ReportName": str,
        "TimeUnit": TimeUnitType,
        "Format": ReportFormatType,
        "Compression": CompressionFormatType,
        "AdditionalSchemaElements": List[SchemaElementType],
        "S3Bucket": str,
        "S3Prefix": str,
        "S3Region": AWSRegionType,
    },
)
_OptionalReportDefinitionTypeDef = TypedDict(
    "_OptionalReportDefinitionTypeDef",
    {
        "AdditionalArtifacts": List[AdditionalArtifactType],
        "RefreshClosedReports": bool,
        "ReportVersioning": ReportVersioningType,
        "BillingViewArn": str,
    },
    total=False,
)

class ReportDefinitionTypeDef(_RequiredReportDefinitionTypeDef, _OptionalReportDefinitionTypeDef):
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

DescribeReportDefinitionsResponseTypeDef = TypedDict(
    "DescribeReportDefinitionsResponseTypeDef",
    {
        "ReportDefinitions": List[ReportDefinitionTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ModifyReportDefinitionRequestRequestTypeDef = TypedDict(
    "ModifyReportDefinitionRequestRequestTypeDef",
    {
        "ReportName": str,
        "ReportDefinition": ReportDefinitionTypeDef,
    },
)

PutReportDefinitionRequestRequestTypeDef = TypedDict(
    "PutReportDefinitionRequestRequestTypeDef",
    {
        "ReportDefinition": ReportDefinitionTypeDef,
    },
)
