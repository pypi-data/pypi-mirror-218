"""
Type annotations for redshift-data service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_redshift_data/type_defs/)

Usage::

    ```python
    from mypy_boto3_redshift_data.type_defs import BatchExecuteStatementInputRequestTypeDef

    data: BatchExecuteStatementInputRequestTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence

from .literals import StatementStatusStringType, StatusStringType

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "BatchExecuteStatementInputRequestTypeDef",
    "BatchExecuteStatementOutputTypeDef",
    "CancelStatementRequestRequestTypeDef",
    "CancelStatementResponseTypeDef",
    "ColumnMetadataTypeDef",
    "DescribeStatementRequestRequestTypeDef",
    "SqlParameterTypeDef",
    "SubStatementDataTypeDef",
    "DescribeTableRequestDescribeTablePaginateTypeDef",
    "DescribeTableRequestRequestTypeDef",
    "ExecuteStatementOutputTypeDef",
    "FieldTypeDef",
    "GetStatementResultRequestGetStatementResultPaginateTypeDef",
    "GetStatementResultRequestRequestTypeDef",
    "ListDatabasesRequestListDatabasesPaginateTypeDef",
    "ListDatabasesRequestRequestTypeDef",
    "ListDatabasesResponseTypeDef",
    "ListSchemasRequestListSchemasPaginateTypeDef",
    "ListSchemasRequestRequestTypeDef",
    "ListSchemasResponseTypeDef",
    "ListStatementsRequestListStatementsPaginateTypeDef",
    "ListStatementsRequestRequestTypeDef",
    "ListTablesRequestListTablesPaginateTypeDef",
    "ListTablesRequestRequestTypeDef",
    "TableMemberTypeDef",
    "PaginatorConfigTypeDef",
    "ResponseMetadataTypeDef",
    "DescribeTableResponseTypeDef",
    "ExecuteStatementInputRequestTypeDef",
    "StatementDataTypeDef",
    "DescribeStatementResponseTypeDef",
    "GetStatementResultResponseTypeDef",
    "ListTablesResponseTypeDef",
    "ListStatementsResponseTypeDef",
)

_RequiredBatchExecuteStatementInputRequestTypeDef = TypedDict(
    "_RequiredBatchExecuteStatementInputRequestTypeDef",
    {
        "Database": str,
        "Sqls": Sequence[str],
    },
)
_OptionalBatchExecuteStatementInputRequestTypeDef = TypedDict(
    "_OptionalBatchExecuteStatementInputRequestTypeDef",
    {
        "ClientToken": str,
        "ClusterIdentifier": str,
        "DbUser": str,
        "SecretArn": str,
        "StatementName": str,
        "WithEvent": bool,
        "WorkgroupName": str,
    },
    total=False,
)

class BatchExecuteStatementInputRequestTypeDef(
    _RequiredBatchExecuteStatementInputRequestTypeDef,
    _OptionalBatchExecuteStatementInputRequestTypeDef,
):
    pass

BatchExecuteStatementOutputTypeDef = TypedDict(
    "BatchExecuteStatementOutputTypeDef",
    {
        "ClusterIdentifier": str,
        "CreatedAt": datetime,
        "Database": str,
        "DbUser": str,
        "Id": str,
        "SecretArn": str,
        "WorkgroupName": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CancelStatementRequestRequestTypeDef = TypedDict(
    "CancelStatementRequestRequestTypeDef",
    {
        "Id": str,
    },
)

CancelStatementResponseTypeDef = TypedDict(
    "CancelStatementResponseTypeDef",
    {
        "Status": bool,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ColumnMetadataTypeDef = TypedDict(
    "ColumnMetadataTypeDef",
    {
        "columnDefault": str,
        "isCaseSensitive": bool,
        "isCurrency": bool,
        "isSigned": bool,
        "label": str,
        "length": int,
        "name": str,
        "nullable": int,
        "precision": int,
        "scale": int,
        "schemaName": str,
        "tableName": str,
        "typeName": str,
    },
    total=False,
)

DescribeStatementRequestRequestTypeDef = TypedDict(
    "DescribeStatementRequestRequestTypeDef",
    {
        "Id": str,
    },
)

SqlParameterTypeDef = TypedDict(
    "SqlParameterTypeDef",
    {
        "name": str,
        "value": str,
    },
)

_RequiredSubStatementDataTypeDef = TypedDict(
    "_RequiredSubStatementDataTypeDef",
    {
        "Id": str,
    },
)
_OptionalSubStatementDataTypeDef = TypedDict(
    "_OptionalSubStatementDataTypeDef",
    {
        "CreatedAt": datetime,
        "Duration": int,
        "Error": str,
        "HasResultSet": bool,
        "QueryString": str,
        "RedshiftQueryId": int,
        "ResultRows": int,
        "ResultSize": int,
        "Status": StatementStatusStringType,
        "UpdatedAt": datetime,
    },
    total=False,
)

class SubStatementDataTypeDef(_RequiredSubStatementDataTypeDef, _OptionalSubStatementDataTypeDef):
    pass

_RequiredDescribeTableRequestDescribeTablePaginateTypeDef = TypedDict(
    "_RequiredDescribeTableRequestDescribeTablePaginateTypeDef",
    {
        "Database": str,
    },
)
_OptionalDescribeTableRequestDescribeTablePaginateTypeDef = TypedDict(
    "_OptionalDescribeTableRequestDescribeTablePaginateTypeDef",
    {
        "ClusterIdentifier": str,
        "ConnectedDatabase": str,
        "DbUser": str,
        "Schema": str,
        "SecretArn": str,
        "Table": str,
        "WorkgroupName": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

class DescribeTableRequestDescribeTablePaginateTypeDef(
    _RequiredDescribeTableRequestDescribeTablePaginateTypeDef,
    _OptionalDescribeTableRequestDescribeTablePaginateTypeDef,
):
    pass

_RequiredDescribeTableRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeTableRequestRequestTypeDef",
    {
        "Database": str,
    },
)
_OptionalDescribeTableRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeTableRequestRequestTypeDef",
    {
        "ClusterIdentifier": str,
        "ConnectedDatabase": str,
        "DbUser": str,
        "MaxResults": int,
        "NextToken": str,
        "Schema": str,
        "SecretArn": str,
        "Table": str,
        "WorkgroupName": str,
    },
    total=False,
)

class DescribeTableRequestRequestTypeDef(
    _RequiredDescribeTableRequestRequestTypeDef, _OptionalDescribeTableRequestRequestTypeDef
):
    pass

ExecuteStatementOutputTypeDef = TypedDict(
    "ExecuteStatementOutputTypeDef",
    {
        "ClusterIdentifier": str,
        "CreatedAt": datetime,
        "Database": str,
        "DbUser": str,
        "Id": str,
        "SecretArn": str,
        "WorkgroupName": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

FieldTypeDef = TypedDict(
    "FieldTypeDef",
    {
        "blobValue": bytes,
        "booleanValue": bool,
        "doubleValue": float,
        "isNull": bool,
        "longValue": int,
        "stringValue": str,
    },
    total=False,
)

_RequiredGetStatementResultRequestGetStatementResultPaginateTypeDef = TypedDict(
    "_RequiredGetStatementResultRequestGetStatementResultPaginateTypeDef",
    {
        "Id": str,
    },
)
_OptionalGetStatementResultRequestGetStatementResultPaginateTypeDef = TypedDict(
    "_OptionalGetStatementResultRequestGetStatementResultPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

class GetStatementResultRequestGetStatementResultPaginateTypeDef(
    _RequiredGetStatementResultRequestGetStatementResultPaginateTypeDef,
    _OptionalGetStatementResultRequestGetStatementResultPaginateTypeDef,
):
    pass

_RequiredGetStatementResultRequestRequestTypeDef = TypedDict(
    "_RequiredGetStatementResultRequestRequestTypeDef",
    {
        "Id": str,
    },
)
_OptionalGetStatementResultRequestRequestTypeDef = TypedDict(
    "_OptionalGetStatementResultRequestRequestTypeDef",
    {
        "NextToken": str,
    },
    total=False,
)

class GetStatementResultRequestRequestTypeDef(
    _RequiredGetStatementResultRequestRequestTypeDef,
    _OptionalGetStatementResultRequestRequestTypeDef,
):
    pass

_RequiredListDatabasesRequestListDatabasesPaginateTypeDef = TypedDict(
    "_RequiredListDatabasesRequestListDatabasesPaginateTypeDef",
    {
        "Database": str,
    },
)
_OptionalListDatabasesRequestListDatabasesPaginateTypeDef = TypedDict(
    "_OptionalListDatabasesRequestListDatabasesPaginateTypeDef",
    {
        "ClusterIdentifier": str,
        "DbUser": str,
        "SecretArn": str,
        "WorkgroupName": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

class ListDatabasesRequestListDatabasesPaginateTypeDef(
    _RequiredListDatabasesRequestListDatabasesPaginateTypeDef,
    _OptionalListDatabasesRequestListDatabasesPaginateTypeDef,
):
    pass

_RequiredListDatabasesRequestRequestTypeDef = TypedDict(
    "_RequiredListDatabasesRequestRequestTypeDef",
    {
        "Database": str,
    },
)
_OptionalListDatabasesRequestRequestTypeDef = TypedDict(
    "_OptionalListDatabasesRequestRequestTypeDef",
    {
        "ClusterIdentifier": str,
        "DbUser": str,
        "MaxResults": int,
        "NextToken": str,
        "SecretArn": str,
        "WorkgroupName": str,
    },
    total=False,
)

class ListDatabasesRequestRequestTypeDef(
    _RequiredListDatabasesRequestRequestTypeDef, _OptionalListDatabasesRequestRequestTypeDef
):
    pass

ListDatabasesResponseTypeDef = TypedDict(
    "ListDatabasesResponseTypeDef",
    {
        "Databases": List[str],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListSchemasRequestListSchemasPaginateTypeDef = TypedDict(
    "_RequiredListSchemasRequestListSchemasPaginateTypeDef",
    {
        "Database": str,
    },
)
_OptionalListSchemasRequestListSchemasPaginateTypeDef = TypedDict(
    "_OptionalListSchemasRequestListSchemasPaginateTypeDef",
    {
        "ClusterIdentifier": str,
        "ConnectedDatabase": str,
        "DbUser": str,
        "SchemaPattern": str,
        "SecretArn": str,
        "WorkgroupName": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

class ListSchemasRequestListSchemasPaginateTypeDef(
    _RequiredListSchemasRequestListSchemasPaginateTypeDef,
    _OptionalListSchemasRequestListSchemasPaginateTypeDef,
):
    pass

_RequiredListSchemasRequestRequestTypeDef = TypedDict(
    "_RequiredListSchemasRequestRequestTypeDef",
    {
        "Database": str,
    },
)
_OptionalListSchemasRequestRequestTypeDef = TypedDict(
    "_OptionalListSchemasRequestRequestTypeDef",
    {
        "ClusterIdentifier": str,
        "ConnectedDatabase": str,
        "DbUser": str,
        "MaxResults": int,
        "NextToken": str,
        "SchemaPattern": str,
        "SecretArn": str,
        "WorkgroupName": str,
    },
    total=False,
)

class ListSchemasRequestRequestTypeDef(
    _RequiredListSchemasRequestRequestTypeDef, _OptionalListSchemasRequestRequestTypeDef
):
    pass

ListSchemasResponseTypeDef = TypedDict(
    "ListSchemasResponseTypeDef",
    {
        "NextToken": str,
        "Schemas": List[str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListStatementsRequestListStatementsPaginateTypeDef = TypedDict(
    "ListStatementsRequestListStatementsPaginateTypeDef",
    {
        "RoleLevel": bool,
        "StatementName": str,
        "Status": StatusStringType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListStatementsRequestRequestTypeDef = TypedDict(
    "ListStatementsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
        "RoleLevel": bool,
        "StatementName": str,
        "Status": StatusStringType,
    },
    total=False,
)

_RequiredListTablesRequestListTablesPaginateTypeDef = TypedDict(
    "_RequiredListTablesRequestListTablesPaginateTypeDef",
    {
        "Database": str,
    },
)
_OptionalListTablesRequestListTablesPaginateTypeDef = TypedDict(
    "_OptionalListTablesRequestListTablesPaginateTypeDef",
    {
        "ClusterIdentifier": str,
        "ConnectedDatabase": str,
        "DbUser": str,
        "SchemaPattern": str,
        "SecretArn": str,
        "TablePattern": str,
        "WorkgroupName": str,
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
        "Database": str,
    },
)
_OptionalListTablesRequestRequestTypeDef = TypedDict(
    "_OptionalListTablesRequestRequestTypeDef",
    {
        "ClusterIdentifier": str,
        "ConnectedDatabase": str,
        "DbUser": str,
        "MaxResults": int,
        "NextToken": str,
        "SchemaPattern": str,
        "SecretArn": str,
        "TablePattern": str,
        "WorkgroupName": str,
    },
    total=False,
)

class ListTablesRequestRequestTypeDef(
    _RequiredListTablesRequestRequestTypeDef, _OptionalListTablesRequestRequestTypeDef
):
    pass

TableMemberTypeDef = TypedDict(
    "TableMemberTypeDef",
    {
        "name": str,
        "schema": str,
        "type": str,
    },
    total=False,
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

DescribeTableResponseTypeDef = TypedDict(
    "DescribeTableResponseTypeDef",
    {
        "ColumnList": List[ColumnMetadataTypeDef],
        "NextToken": str,
        "TableName": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredExecuteStatementInputRequestTypeDef = TypedDict(
    "_RequiredExecuteStatementInputRequestTypeDef",
    {
        "Database": str,
        "Sql": str,
    },
)
_OptionalExecuteStatementInputRequestTypeDef = TypedDict(
    "_OptionalExecuteStatementInputRequestTypeDef",
    {
        "ClientToken": str,
        "ClusterIdentifier": str,
        "DbUser": str,
        "Parameters": Sequence[SqlParameterTypeDef],
        "SecretArn": str,
        "StatementName": str,
        "WithEvent": bool,
        "WorkgroupName": str,
    },
    total=False,
)

class ExecuteStatementInputRequestTypeDef(
    _RequiredExecuteStatementInputRequestTypeDef, _OptionalExecuteStatementInputRequestTypeDef
):
    pass

_RequiredStatementDataTypeDef = TypedDict(
    "_RequiredStatementDataTypeDef",
    {
        "Id": str,
    },
)
_OptionalStatementDataTypeDef = TypedDict(
    "_OptionalStatementDataTypeDef",
    {
        "CreatedAt": datetime,
        "IsBatchStatement": bool,
        "QueryParameters": List[SqlParameterTypeDef],
        "QueryString": str,
        "QueryStrings": List[str],
        "SecretArn": str,
        "StatementName": str,
        "Status": StatusStringType,
        "UpdatedAt": datetime,
    },
    total=False,
)

class StatementDataTypeDef(_RequiredStatementDataTypeDef, _OptionalStatementDataTypeDef):
    pass

DescribeStatementResponseTypeDef = TypedDict(
    "DescribeStatementResponseTypeDef",
    {
        "ClusterIdentifier": str,
        "CreatedAt": datetime,
        "Database": str,
        "DbUser": str,
        "Duration": int,
        "Error": str,
        "HasResultSet": bool,
        "Id": str,
        "QueryParameters": List[SqlParameterTypeDef],
        "QueryString": str,
        "RedshiftPid": int,
        "RedshiftQueryId": int,
        "ResultRows": int,
        "ResultSize": int,
        "SecretArn": str,
        "Status": StatusStringType,
        "SubStatements": List[SubStatementDataTypeDef],
        "UpdatedAt": datetime,
        "WorkgroupName": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetStatementResultResponseTypeDef = TypedDict(
    "GetStatementResultResponseTypeDef",
    {
        "ColumnMetadata": List[ColumnMetadataTypeDef],
        "NextToken": str,
        "Records": List[List[FieldTypeDef]],
        "TotalNumRows": int,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListTablesResponseTypeDef = TypedDict(
    "ListTablesResponseTypeDef",
    {
        "NextToken": str,
        "Tables": List[TableMemberTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListStatementsResponseTypeDef = TypedDict(
    "ListStatementsResponseTypeDef",
    {
        "NextToken": str,
        "Statements": List[StatementDataTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)
