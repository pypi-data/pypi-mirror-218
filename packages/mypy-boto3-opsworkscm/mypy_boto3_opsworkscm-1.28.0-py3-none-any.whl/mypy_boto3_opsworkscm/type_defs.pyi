"""
Type annotations for opsworkscm service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opsworkscm/type_defs/)

Usage::

    ```python
    from mypy_boto3_opsworkscm.type_defs import AccountAttributeTypeDef

    data: AccountAttributeTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence

from .literals import (
    BackupStatusType,
    BackupTypeType,
    MaintenanceStatusType,
    NodeAssociationStatusType,
    ServerStatusType,
)

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "AccountAttributeTypeDef",
    "EngineAttributeTypeDef",
    "AssociateNodeResponseTypeDef",
    "BackupTypeDef",
    "TagTypeDef",
    "DeleteBackupRequestRequestTypeDef",
    "DeleteServerRequestRequestTypeDef",
    "DescribeBackupsRequestDescribeBackupsPaginateTypeDef",
    "DescribeBackupsRequestRequestTypeDef",
    "DescribeEventsRequestDescribeEventsPaginateTypeDef",
    "DescribeEventsRequestRequestTypeDef",
    "ServerEventTypeDef",
    "WaiterConfigTypeDef",
    "DescribeNodeAssociationStatusRequestRequestTypeDef",
    "DescribeServersRequestDescribeServersPaginateTypeDef",
    "DescribeServersRequestRequestTypeDef",
    "DisassociateNodeResponseTypeDef",
    "ListTagsForResourceRequestListTagsForResourcePaginateTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "ResponseMetadataTypeDef",
    "RestoreServerRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateServerEngineAttributesRequestRequestTypeDef",
    "UpdateServerRequestRequestTypeDef",
    "DescribeAccountAttributesResponseTypeDef",
    "AssociateNodeRequestRequestTypeDef",
    "DescribeNodeAssociationStatusResponseTypeDef",
    "DisassociateNodeRequestRequestTypeDef",
    "ExportServerEngineAttributeRequestRequestTypeDef",
    "ExportServerEngineAttributeResponseTypeDef",
    "ServerTypeDef",
    "StartMaintenanceRequestRequestTypeDef",
    "CreateBackupResponseTypeDef",
    "DescribeBackupsResponseTypeDef",
    "CreateBackupRequestRequestTypeDef",
    "CreateServerRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "DescribeEventsResponseTypeDef",
    "DescribeNodeAssociationStatusRequestNodeAssociatedWaitTypeDef",
    "CreateServerResponseTypeDef",
    "DescribeServersResponseTypeDef",
    "RestoreServerResponseTypeDef",
    "StartMaintenanceResponseTypeDef",
    "UpdateServerEngineAttributesResponseTypeDef",
    "UpdateServerResponseTypeDef",
)

AccountAttributeTypeDef = TypedDict(
    "AccountAttributeTypeDef",
    {
        "Name": str,
        "Maximum": int,
        "Used": int,
    },
    total=False,
)

EngineAttributeTypeDef = TypedDict(
    "EngineAttributeTypeDef",
    {
        "Name": str,
        "Value": str,
    },
    total=False,
)

AssociateNodeResponseTypeDef = TypedDict(
    "AssociateNodeResponseTypeDef",
    {
        "NodeAssociationStatusToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

BackupTypeDef = TypedDict(
    "BackupTypeDef",
    {
        "BackupArn": str,
        "BackupId": str,
        "BackupType": BackupTypeType,
        "CreatedAt": datetime,
        "Description": str,
        "Engine": str,
        "EngineModel": str,
        "EngineVersion": str,
        "InstanceProfileArn": str,
        "InstanceType": str,
        "KeyPair": str,
        "PreferredBackupWindow": str,
        "PreferredMaintenanceWindow": str,
        "S3DataSize": int,
        "S3DataUrl": str,
        "S3LogUrl": str,
        "SecurityGroupIds": List[str],
        "ServerName": str,
        "ServiceRoleArn": str,
        "Status": BackupStatusType,
        "StatusDescription": str,
        "SubnetIds": List[str],
        "ToolsVersion": str,
        "UserArn": str,
    },
    total=False,
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

DeleteBackupRequestRequestTypeDef = TypedDict(
    "DeleteBackupRequestRequestTypeDef",
    {
        "BackupId": str,
    },
)

DeleteServerRequestRequestTypeDef = TypedDict(
    "DeleteServerRequestRequestTypeDef",
    {
        "ServerName": str,
    },
)

DescribeBackupsRequestDescribeBackupsPaginateTypeDef = TypedDict(
    "DescribeBackupsRequestDescribeBackupsPaginateTypeDef",
    {
        "BackupId": str,
        "ServerName": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

DescribeBackupsRequestRequestTypeDef = TypedDict(
    "DescribeBackupsRequestRequestTypeDef",
    {
        "BackupId": str,
        "ServerName": str,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

_RequiredDescribeEventsRequestDescribeEventsPaginateTypeDef = TypedDict(
    "_RequiredDescribeEventsRequestDescribeEventsPaginateTypeDef",
    {
        "ServerName": str,
    },
)
_OptionalDescribeEventsRequestDescribeEventsPaginateTypeDef = TypedDict(
    "_OptionalDescribeEventsRequestDescribeEventsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

class DescribeEventsRequestDescribeEventsPaginateTypeDef(
    _RequiredDescribeEventsRequestDescribeEventsPaginateTypeDef,
    _OptionalDescribeEventsRequestDescribeEventsPaginateTypeDef,
):
    pass

_RequiredDescribeEventsRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeEventsRequestRequestTypeDef",
    {
        "ServerName": str,
    },
)
_OptionalDescribeEventsRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeEventsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class DescribeEventsRequestRequestTypeDef(
    _RequiredDescribeEventsRequestRequestTypeDef, _OptionalDescribeEventsRequestRequestTypeDef
):
    pass

ServerEventTypeDef = TypedDict(
    "ServerEventTypeDef",
    {
        "CreatedAt": datetime,
        "ServerName": str,
        "Message": str,
        "LogUrl": str,
    },
    total=False,
)

WaiterConfigTypeDef = TypedDict(
    "WaiterConfigTypeDef",
    {
        "Delay": int,
        "MaxAttempts": int,
    },
    total=False,
)

DescribeNodeAssociationStatusRequestRequestTypeDef = TypedDict(
    "DescribeNodeAssociationStatusRequestRequestTypeDef",
    {
        "NodeAssociationStatusToken": str,
        "ServerName": str,
    },
)

DescribeServersRequestDescribeServersPaginateTypeDef = TypedDict(
    "DescribeServersRequestDescribeServersPaginateTypeDef",
    {
        "ServerName": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

DescribeServersRequestRequestTypeDef = TypedDict(
    "DescribeServersRequestRequestTypeDef",
    {
        "ServerName": str,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

DisassociateNodeResponseTypeDef = TypedDict(
    "DisassociateNodeResponseTypeDef",
    {
        "NodeAssociationStatusToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListTagsForResourceRequestListTagsForResourcePaginateTypeDef = TypedDict(
    "_RequiredListTagsForResourceRequestListTagsForResourcePaginateTypeDef",
    {
        "ResourceArn": str,
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
        "ResourceArn": str,
    },
)
_OptionalListTagsForResourceRequestRequestTypeDef = TypedDict(
    "_OptionalListTagsForResourceRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
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

_RequiredRestoreServerRequestRequestTypeDef = TypedDict(
    "_RequiredRestoreServerRequestRequestTypeDef",
    {
        "BackupId": str,
        "ServerName": str,
    },
)
_OptionalRestoreServerRequestRequestTypeDef = TypedDict(
    "_OptionalRestoreServerRequestRequestTypeDef",
    {
        "InstanceType": str,
        "KeyPair": str,
    },
    total=False,
)

class RestoreServerRequestRequestTypeDef(
    _RequiredRestoreServerRequestRequestTypeDef, _OptionalRestoreServerRequestRequestTypeDef
):
    pass

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)

_RequiredUpdateServerEngineAttributesRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateServerEngineAttributesRequestRequestTypeDef",
    {
        "ServerName": str,
        "AttributeName": str,
    },
)
_OptionalUpdateServerEngineAttributesRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateServerEngineAttributesRequestRequestTypeDef",
    {
        "AttributeValue": str,
    },
    total=False,
)

class UpdateServerEngineAttributesRequestRequestTypeDef(
    _RequiredUpdateServerEngineAttributesRequestRequestTypeDef,
    _OptionalUpdateServerEngineAttributesRequestRequestTypeDef,
):
    pass

_RequiredUpdateServerRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateServerRequestRequestTypeDef",
    {
        "ServerName": str,
    },
)
_OptionalUpdateServerRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateServerRequestRequestTypeDef",
    {
        "DisableAutomatedBackup": bool,
        "BackupRetentionCount": int,
        "PreferredMaintenanceWindow": str,
        "PreferredBackupWindow": str,
    },
    total=False,
)

class UpdateServerRequestRequestTypeDef(
    _RequiredUpdateServerRequestRequestTypeDef, _OptionalUpdateServerRequestRequestTypeDef
):
    pass

DescribeAccountAttributesResponseTypeDef = TypedDict(
    "DescribeAccountAttributesResponseTypeDef",
    {
        "Attributes": List[AccountAttributeTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

AssociateNodeRequestRequestTypeDef = TypedDict(
    "AssociateNodeRequestRequestTypeDef",
    {
        "ServerName": str,
        "NodeName": str,
        "EngineAttributes": Sequence[EngineAttributeTypeDef],
    },
)

DescribeNodeAssociationStatusResponseTypeDef = TypedDict(
    "DescribeNodeAssociationStatusResponseTypeDef",
    {
        "NodeAssociationStatus": NodeAssociationStatusType,
        "EngineAttributes": List[EngineAttributeTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredDisassociateNodeRequestRequestTypeDef = TypedDict(
    "_RequiredDisassociateNodeRequestRequestTypeDef",
    {
        "ServerName": str,
        "NodeName": str,
    },
)
_OptionalDisassociateNodeRequestRequestTypeDef = TypedDict(
    "_OptionalDisassociateNodeRequestRequestTypeDef",
    {
        "EngineAttributes": Sequence[EngineAttributeTypeDef],
    },
    total=False,
)

class DisassociateNodeRequestRequestTypeDef(
    _RequiredDisassociateNodeRequestRequestTypeDef, _OptionalDisassociateNodeRequestRequestTypeDef
):
    pass

_RequiredExportServerEngineAttributeRequestRequestTypeDef = TypedDict(
    "_RequiredExportServerEngineAttributeRequestRequestTypeDef",
    {
        "ExportAttributeName": str,
        "ServerName": str,
    },
)
_OptionalExportServerEngineAttributeRequestRequestTypeDef = TypedDict(
    "_OptionalExportServerEngineAttributeRequestRequestTypeDef",
    {
        "InputAttributes": Sequence[EngineAttributeTypeDef],
    },
    total=False,
)

class ExportServerEngineAttributeRequestRequestTypeDef(
    _RequiredExportServerEngineAttributeRequestRequestTypeDef,
    _OptionalExportServerEngineAttributeRequestRequestTypeDef,
):
    pass

ExportServerEngineAttributeResponseTypeDef = TypedDict(
    "ExportServerEngineAttributeResponseTypeDef",
    {
        "EngineAttribute": EngineAttributeTypeDef,
        "ServerName": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ServerTypeDef = TypedDict(
    "ServerTypeDef",
    {
        "AssociatePublicIpAddress": bool,
        "BackupRetentionCount": int,
        "ServerName": str,
        "CreatedAt": datetime,
        "CloudFormationStackArn": str,
        "CustomDomain": str,
        "DisableAutomatedBackup": bool,
        "Endpoint": str,
        "Engine": str,
        "EngineModel": str,
        "EngineAttributes": List[EngineAttributeTypeDef],
        "EngineVersion": str,
        "InstanceProfileArn": str,
        "InstanceType": str,
        "KeyPair": str,
        "MaintenanceStatus": MaintenanceStatusType,
        "PreferredMaintenanceWindow": str,
        "PreferredBackupWindow": str,
        "SecurityGroupIds": List[str],
        "ServiceRoleArn": str,
        "Status": ServerStatusType,
        "StatusReason": str,
        "SubnetIds": List[str],
        "ServerArn": str,
    },
    total=False,
)

_RequiredStartMaintenanceRequestRequestTypeDef = TypedDict(
    "_RequiredStartMaintenanceRequestRequestTypeDef",
    {
        "ServerName": str,
    },
)
_OptionalStartMaintenanceRequestRequestTypeDef = TypedDict(
    "_OptionalStartMaintenanceRequestRequestTypeDef",
    {
        "EngineAttributes": Sequence[EngineAttributeTypeDef],
    },
    total=False,
)

class StartMaintenanceRequestRequestTypeDef(
    _RequiredStartMaintenanceRequestRequestTypeDef, _OptionalStartMaintenanceRequestRequestTypeDef
):
    pass

CreateBackupResponseTypeDef = TypedDict(
    "CreateBackupResponseTypeDef",
    {
        "Backup": BackupTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeBackupsResponseTypeDef = TypedDict(
    "DescribeBackupsResponseTypeDef",
    {
        "Backups": List[BackupTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateBackupRequestRequestTypeDef = TypedDict(
    "_RequiredCreateBackupRequestRequestTypeDef",
    {
        "ServerName": str,
    },
)
_OptionalCreateBackupRequestRequestTypeDef = TypedDict(
    "_OptionalCreateBackupRequestRequestTypeDef",
    {
        "Description": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)

class CreateBackupRequestRequestTypeDef(
    _RequiredCreateBackupRequestRequestTypeDef, _OptionalCreateBackupRequestRequestTypeDef
):
    pass

_RequiredCreateServerRequestRequestTypeDef = TypedDict(
    "_RequiredCreateServerRequestRequestTypeDef",
    {
        "Engine": str,
        "ServerName": str,
        "InstanceProfileArn": str,
        "InstanceType": str,
        "ServiceRoleArn": str,
    },
)
_OptionalCreateServerRequestRequestTypeDef = TypedDict(
    "_OptionalCreateServerRequestRequestTypeDef",
    {
        "AssociatePublicIpAddress": bool,
        "CustomDomain": str,
        "CustomCertificate": str,
        "CustomPrivateKey": str,
        "DisableAutomatedBackup": bool,
        "EngineModel": str,
        "EngineVersion": str,
        "EngineAttributes": Sequence[EngineAttributeTypeDef],
        "BackupRetentionCount": int,
        "KeyPair": str,
        "PreferredMaintenanceWindow": str,
        "PreferredBackupWindow": str,
        "SecurityGroupIds": Sequence[str],
        "SubnetIds": Sequence[str],
        "Tags": Sequence[TagTypeDef],
        "BackupId": str,
    },
    total=False,
)

class CreateServerRequestRequestTypeDef(
    _RequiredCreateServerRequestRequestTypeDef, _OptionalCreateServerRequestRequestTypeDef
):
    pass

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "Tags": List[TagTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "Tags": Sequence[TagTypeDef],
    },
)

DescribeEventsResponseTypeDef = TypedDict(
    "DescribeEventsResponseTypeDef",
    {
        "ServerEvents": List[ServerEventTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredDescribeNodeAssociationStatusRequestNodeAssociatedWaitTypeDef = TypedDict(
    "_RequiredDescribeNodeAssociationStatusRequestNodeAssociatedWaitTypeDef",
    {
        "NodeAssociationStatusToken": str,
        "ServerName": str,
    },
)
_OptionalDescribeNodeAssociationStatusRequestNodeAssociatedWaitTypeDef = TypedDict(
    "_OptionalDescribeNodeAssociationStatusRequestNodeAssociatedWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

class DescribeNodeAssociationStatusRequestNodeAssociatedWaitTypeDef(
    _RequiredDescribeNodeAssociationStatusRequestNodeAssociatedWaitTypeDef,
    _OptionalDescribeNodeAssociationStatusRequestNodeAssociatedWaitTypeDef,
):
    pass

CreateServerResponseTypeDef = TypedDict(
    "CreateServerResponseTypeDef",
    {
        "Server": ServerTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeServersResponseTypeDef = TypedDict(
    "DescribeServersResponseTypeDef",
    {
        "Servers": List[ServerTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

RestoreServerResponseTypeDef = TypedDict(
    "RestoreServerResponseTypeDef",
    {
        "Server": ServerTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StartMaintenanceResponseTypeDef = TypedDict(
    "StartMaintenanceResponseTypeDef",
    {
        "Server": ServerTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateServerEngineAttributesResponseTypeDef = TypedDict(
    "UpdateServerEngineAttributesResponseTypeDef",
    {
        "Server": ServerTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateServerResponseTypeDef = TypedDict(
    "UpdateServerResponseTypeDef",
    {
        "Server": ServerTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)
