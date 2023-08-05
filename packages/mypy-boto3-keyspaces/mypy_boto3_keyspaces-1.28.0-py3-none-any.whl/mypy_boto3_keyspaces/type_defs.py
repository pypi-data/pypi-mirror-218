"""
Type annotations for keyspaces service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_keyspaces/type_defs/)

Usage::

    ```python
    from mypy_boto3_keyspaces.type_defs import CapacitySpecificationSummaryTypeDef

    data: CapacitySpecificationSummaryTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence, Union

from .literals import (
    EncryptionTypeType,
    PointInTimeRecoveryStatusType,
    SortOrderType,
    TableStatusType,
    ThroughputModeType,
    rsType,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "CapacitySpecificationSummaryTypeDef",
    "CapacitySpecificationTypeDef",
    "ClientSideTimestampsTypeDef",
    "ClusteringKeyTypeDef",
    "ColumnDefinitionTypeDef",
    "CommentTypeDef",
    "ReplicationSpecificationTypeDef",
    "TagTypeDef",
    "CreateKeyspaceResponseTypeDef",
    "EncryptionSpecificationTypeDef",
    "PointInTimeRecoveryTypeDef",
    "TimeToLiveTypeDef",
    "CreateTableResponseTypeDef",
    "DeleteKeyspaceRequestRequestTypeDef",
    "DeleteTableRequestRequestTypeDef",
    "GetKeyspaceRequestRequestTypeDef",
    "GetKeyspaceResponseTypeDef",
    "GetTableRequestRequestTypeDef",
    "PointInTimeRecoverySummaryTypeDef",
    "KeyspaceSummaryTypeDef",
    "ListKeyspacesRequestListKeyspacesPaginateTypeDef",
    "ListKeyspacesRequestRequestTypeDef",
    "ListTablesRequestListTablesPaginateTypeDef",
    "ListTablesRequestRequestTypeDef",
    "TableSummaryTypeDef",
    "ListTagsForResourceRequestListTagsForResourcePaginateTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "PartitionKeyTypeDef",
    "ResponseMetadataTypeDef",
    "RestoreTableResponseTypeDef",
    "StaticColumnTypeDef",
    "UpdateTableResponseTypeDef",
    "CreateKeyspaceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "RestoreTableRequestRequestTypeDef",
    "UpdateTableRequestRequestTypeDef",
    "ListKeyspacesResponseTypeDef",
    "ListTablesResponseTypeDef",
    "SchemaDefinitionTypeDef",
    "CreateTableRequestRequestTypeDef",
    "GetTableResponseTypeDef",
)

_RequiredCapacitySpecificationSummaryTypeDef = TypedDict(
    "_RequiredCapacitySpecificationSummaryTypeDef",
    {
        "throughputMode": ThroughputModeType,
    },
)
_OptionalCapacitySpecificationSummaryTypeDef = TypedDict(
    "_OptionalCapacitySpecificationSummaryTypeDef",
    {
        "readCapacityUnits": int,
        "writeCapacityUnits": int,
        "lastUpdateToPayPerRequestTimestamp": datetime,
    },
    total=False,
)


class CapacitySpecificationSummaryTypeDef(
    _RequiredCapacitySpecificationSummaryTypeDef, _OptionalCapacitySpecificationSummaryTypeDef
):
    pass


_RequiredCapacitySpecificationTypeDef = TypedDict(
    "_RequiredCapacitySpecificationTypeDef",
    {
        "throughputMode": ThroughputModeType,
    },
)
_OptionalCapacitySpecificationTypeDef = TypedDict(
    "_OptionalCapacitySpecificationTypeDef",
    {
        "readCapacityUnits": int,
        "writeCapacityUnits": int,
    },
    total=False,
)


class CapacitySpecificationTypeDef(
    _RequiredCapacitySpecificationTypeDef, _OptionalCapacitySpecificationTypeDef
):
    pass


ClientSideTimestampsTypeDef = TypedDict(
    "ClientSideTimestampsTypeDef",
    {
        "status": Literal["ENABLED"],
    },
)

ClusteringKeyTypeDef = TypedDict(
    "ClusteringKeyTypeDef",
    {
        "name": str,
        "orderBy": SortOrderType,
    },
)

ColumnDefinitionTypeDef = TypedDict(
    "ColumnDefinitionTypeDef",
    {
        "name": str,
        "type": str,
    },
)

CommentTypeDef = TypedDict(
    "CommentTypeDef",
    {
        "message": str,
    },
)

_RequiredReplicationSpecificationTypeDef = TypedDict(
    "_RequiredReplicationSpecificationTypeDef",
    {
        "replicationStrategy": rsType,
    },
)
_OptionalReplicationSpecificationTypeDef = TypedDict(
    "_OptionalReplicationSpecificationTypeDef",
    {
        "regionList": Sequence[str],
    },
    total=False,
)


class ReplicationSpecificationTypeDef(
    _RequiredReplicationSpecificationTypeDef, _OptionalReplicationSpecificationTypeDef
):
    pass


TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "key": str,
        "value": str,
    },
)

CreateKeyspaceResponseTypeDef = TypedDict(
    "CreateKeyspaceResponseTypeDef",
    {
        "resourceArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredEncryptionSpecificationTypeDef = TypedDict(
    "_RequiredEncryptionSpecificationTypeDef",
    {
        "type": EncryptionTypeType,
    },
)
_OptionalEncryptionSpecificationTypeDef = TypedDict(
    "_OptionalEncryptionSpecificationTypeDef",
    {
        "kmsKeyIdentifier": str,
    },
    total=False,
)


class EncryptionSpecificationTypeDef(
    _RequiredEncryptionSpecificationTypeDef, _OptionalEncryptionSpecificationTypeDef
):
    pass


PointInTimeRecoveryTypeDef = TypedDict(
    "PointInTimeRecoveryTypeDef",
    {
        "status": PointInTimeRecoveryStatusType,
    },
)

TimeToLiveTypeDef = TypedDict(
    "TimeToLiveTypeDef",
    {
        "status": Literal["ENABLED"],
    },
)

CreateTableResponseTypeDef = TypedDict(
    "CreateTableResponseTypeDef",
    {
        "resourceArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteKeyspaceRequestRequestTypeDef = TypedDict(
    "DeleteKeyspaceRequestRequestTypeDef",
    {
        "keyspaceName": str,
    },
)

DeleteTableRequestRequestTypeDef = TypedDict(
    "DeleteTableRequestRequestTypeDef",
    {
        "keyspaceName": str,
        "tableName": str,
    },
)

GetKeyspaceRequestRequestTypeDef = TypedDict(
    "GetKeyspaceRequestRequestTypeDef",
    {
        "keyspaceName": str,
    },
)

GetKeyspaceResponseTypeDef = TypedDict(
    "GetKeyspaceResponseTypeDef",
    {
        "keyspaceName": str,
        "resourceArn": str,
        "replicationStrategy": rsType,
        "replicationRegions": List[str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetTableRequestRequestTypeDef = TypedDict(
    "GetTableRequestRequestTypeDef",
    {
        "keyspaceName": str,
        "tableName": str,
    },
)

_RequiredPointInTimeRecoverySummaryTypeDef = TypedDict(
    "_RequiredPointInTimeRecoverySummaryTypeDef",
    {
        "status": PointInTimeRecoveryStatusType,
    },
)
_OptionalPointInTimeRecoverySummaryTypeDef = TypedDict(
    "_OptionalPointInTimeRecoverySummaryTypeDef",
    {
        "earliestRestorableTimestamp": datetime,
    },
    total=False,
)


class PointInTimeRecoverySummaryTypeDef(
    _RequiredPointInTimeRecoverySummaryTypeDef, _OptionalPointInTimeRecoverySummaryTypeDef
):
    pass


_RequiredKeyspaceSummaryTypeDef = TypedDict(
    "_RequiredKeyspaceSummaryTypeDef",
    {
        "keyspaceName": str,
        "resourceArn": str,
        "replicationStrategy": rsType,
    },
)
_OptionalKeyspaceSummaryTypeDef = TypedDict(
    "_OptionalKeyspaceSummaryTypeDef",
    {
        "replicationRegions": List[str],
    },
    total=False,
)


class KeyspaceSummaryTypeDef(_RequiredKeyspaceSummaryTypeDef, _OptionalKeyspaceSummaryTypeDef):
    pass


ListKeyspacesRequestListKeyspacesPaginateTypeDef = TypedDict(
    "ListKeyspacesRequestListKeyspacesPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListKeyspacesRequestRequestTypeDef = TypedDict(
    "ListKeyspacesRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

_RequiredListTablesRequestListTablesPaginateTypeDef = TypedDict(
    "_RequiredListTablesRequestListTablesPaginateTypeDef",
    {
        "keyspaceName": str,
    },
)
_OptionalListTablesRequestListTablesPaginateTypeDef = TypedDict(
    "_OptionalListTablesRequestListTablesPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListTablesRequestListTablesPaginateTypeDef(
    _RequiredListTablesRequestListTablesPaginateTypeDef,
    _OptionalListTablesRequestListTablesPaginateTypeDef,
):
    pass


_RequiredListTablesRequestRequestTypeDef = TypedDict(
    "_RequiredListTablesRequestRequestTypeDef",
    {
        "keyspaceName": str,
    },
)
_OptionalListTablesRequestRequestTypeDef = TypedDict(
    "_OptionalListTablesRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class ListTablesRequestRequestTypeDef(
    _RequiredListTablesRequestRequestTypeDef, _OptionalListTablesRequestRequestTypeDef
):
    pass


TableSummaryTypeDef = TypedDict(
    "TableSummaryTypeDef",
    {
        "keyspaceName": str,
        "tableName": str,
        "resourceArn": str,
    },
)

_RequiredListTagsForResourceRequestListTagsForResourcePaginateTypeDef = TypedDict(
    "_RequiredListTagsForResourceRequestListTagsForResourcePaginateTypeDef",
    {
        "resourceArn": str,
    },
)
_OptionalListTagsForResourceRequestListTagsForResourcePaginateTypeDef = TypedDict(
    "_OptionalListTagsForResourceRequestListTagsForResourcePaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListTagsForResourceRequestListTagsForResourcePaginateTypeDef(
    _RequiredListTagsForResourceRequestListTagsForResourcePaginateTypeDef,
    _OptionalListTagsForResourceRequestListTagsForResourcePaginateTypeDef,
):
    pass


_RequiredListTagsForResourceRequestRequestTypeDef = TypedDict(
    "_RequiredListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)
_OptionalListTagsForResourceRequestRequestTypeDef = TypedDict(
    "_OptionalListTagsForResourceRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class ListTagsForResourceRequestRequestTypeDef(
    _RequiredListTagsForResourceRequestRequestTypeDef,
    _OptionalListTagsForResourceRequestRequestTypeDef,
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

PartitionKeyTypeDef = TypedDict(
    "PartitionKeyTypeDef",
    {
        "name": str,
    },
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

RestoreTableResponseTypeDef = TypedDict(
    "RestoreTableResponseTypeDef",
    {
        "restoredTableARN": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StaticColumnTypeDef = TypedDict(
    "StaticColumnTypeDef",
    {
        "name": str,
    },
)

UpdateTableResponseTypeDef = TypedDict(
    "UpdateTableResponseTypeDef",
    {
        "resourceArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateKeyspaceRequestRequestTypeDef = TypedDict(
    "_RequiredCreateKeyspaceRequestRequestTypeDef",
    {
        "keyspaceName": str,
    },
)
_OptionalCreateKeyspaceRequestRequestTypeDef = TypedDict(
    "_OptionalCreateKeyspaceRequestRequestTypeDef",
    {
        "tags": Sequence[TagTypeDef],
        "replicationSpecification": ReplicationSpecificationTypeDef,
    },
    total=False,
)


class CreateKeyspaceRequestRequestTypeDef(
    _RequiredCreateKeyspaceRequestRequestTypeDef, _OptionalCreateKeyspaceRequestRequestTypeDef
):
    pass


ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "nextToken": str,
        "tags": List[TagTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Sequence[TagTypeDef],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Sequence[TagTypeDef],
    },
)

_RequiredRestoreTableRequestRequestTypeDef = TypedDict(
    "_RequiredRestoreTableRequestRequestTypeDef",
    {
        "sourceKeyspaceName": str,
        "sourceTableName": str,
        "targetKeyspaceName": str,
        "targetTableName": str,
    },
)
_OptionalRestoreTableRequestRequestTypeDef = TypedDict(
    "_OptionalRestoreTableRequestRequestTypeDef",
    {
        "restoreTimestamp": Union[datetime, str],
        "capacitySpecificationOverride": CapacitySpecificationTypeDef,
        "encryptionSpecificationOverride": EncryptionSpecificationTypeDef,
        "pointInTimeRecoveryOverride": PointInTimeRecoveryTypeDef,
        "tagsOverride": Sequence[TagTypeDef],
    },
    total=False,
)


class RestoreTableRequestRequestTypeDef(
    _RequiredRestoreTableRequestRequestTypeDef, _OptionalRestoreTableRequestRequestTypeDef
):
    pass


_RequiredUpdateTableRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateTableRequestRequestTypeDef",
    {
        "keyspaceName": str,
        "tableName": str,
    },
)
_OptionalUpdateTableRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateTableRequestRequestTypeDef",
    {
        "addColumns": Sequence[ColumnDefinitionTypeDef],
        "capacitySpecification": CapacitySpecificationTypeDef,
        "encryptionSpecification": EncryptionSpecificationTypeDef,
        "pointInTimeRecovery": PointInTimeRecoveryTypeDef,
        "ttl": TimeToLiveTypeDef,
        "defaultTimeToLive": int,
        "clientSideTimestamps": ClientSideTimestampsTypeDef,
    },
    total=False,
)


class UpdateTableRequestRequestTypeDef(
    _RequiredUpdateTableRequestRequestTypeDef, _OptionalUpdateTableRequestRequestTypeDef
):
    pass


ListKeyspacesResponseTypeDef = TypedDict(
    "ListKeyspacesResponseTypeDef",
    {
        "nextToken": str,
        "keyspaces": List[KeyspaceSummaryTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListTablesResponseTypeDef = TypedDict(
    "ListTablesResponseTypeDef",
    {
        "nextToken": str,
        "tables": List[TableSummaryTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredSchemaDefinitionTypeDef = TypedDict(
    "_RequiredSchemaDefinitionTypeDef",
    {
        "allColumns": Sequence[ColumnDefinitionTypeDef],
        "partitionKeys": Sequence[PartitionKeyTypeDef],
    },
)
_OptionalSchemaDefinitionTypeDef = TypedDict(
    "_OptionalSchemaDefinitionTypeDef",
    {
        "clusteringKeys": Sequence[ClusteringKeyTypeDef],
        "staticColumns": Sequence[StaticColumnTypeDef],
    },
    total=False,
)


class SchemaDefinitionTypeDef(_RequiredSchemaDefinitionTypeDef, _OptionalSchemaDefinitionTypeDef):
    pass


_RequiredCreateTableRequestRequestTypeDef = TypedDict(
    "_RequiredCreateTableRequestRequestTypeDef",
    {
        "keyspaceName": str,
        "tableName": str,
        "schemaDefinition": SchemaDefinitionTypeDef,
    },
)
_OptionalCreateTableRequestRequestTypeDef = TypedDict(
    "_OptionalCreateTableRequestRequestTypeDef",
    {
        "comment": CommentTypeDef,
        "capacitySpecification": CapacitySpecificationTypeDef,
        "encryptionSpecification": EncryptionSpecificationTypeDef,
        "pointInTimeRecovery": PointInTimeRecoveryTypeDef,
        "ttl": TimeToLiveTypeDef,
        "defaultTimeToLive": int,
        "tags": Sequence[TagTypeDef],
        "clientSideTimestamps": ClientSideTimestampsTypeDef,
    },
    total=False,
)


class CreateTableRequestRequestTypeDef(
    _RequiredCreateTableRequestRequestTypeDef, _OptionalCreateTableRequestRequestTypeDef
):
    pass


GetTableResponseTypeDef = TypedDict(
    "GetTableResponseTypeDef",
    {
        "keyspaceName": str,
        "tableName": str,
        "resourceArn": str,
        "creationTimestamp": datetime,
        "status": TableStatusType,
        "schemaDefinition": SchemaDefinitionTypeDef,
        "capacitySpecification": CapacitySpecificationSummaryTypeDef,
        "encryptionSpecification": EncryptionSpecificationTypeDef,
        "pointInTimeRecovery": PointInTimeRecoverySummaryTypeDef,
        "ttl": TimeToLiveTypeDef,
        "defaultTimeToLive": int,
        "comment": CommentTypeDef,
        "clientSideTimestamps": ClientSideTimestampsTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)
