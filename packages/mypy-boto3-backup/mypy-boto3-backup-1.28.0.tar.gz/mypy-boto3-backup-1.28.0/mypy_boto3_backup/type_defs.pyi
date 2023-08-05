"""
Type annotations for backup service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_backup/type_defs/)

Usage::

    ```python
    from mypy_boto3_backup.type_defs import AdvancedBackupSettingTypeDef

    data: AdvancedBackupSettingTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    BackupJobStateType,
    BackupVaultEventType,
    CopyJobStateType,
    LegalHoldStatusType,
    RecoveryPointStatusType,
    RestoreJobStatusType,
    StorageClassType,
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
    "AdvancedBackupSettingTypeDef",
    "RecoveryPointCreatorTypeDef",
    "BackupPlanTemplatesListMemberTypeDef",
    "LifecycleTypeDef",
    "ConditionTypeDef",
    "BackupSelectionsListMemberTypeDef",
    "BackupVaultListMemberTypeDef",
    "CalculatedLifecycleTypeDef",
    "CancelLegalHoldInputRequestTypeDef",
    "ConditionParameterTypeDef",
    "ControlInputParameterTypeDef",
    "ControlScopeTypeDef",
    "CreateBackupSelectionOutputTypeDef",
    "CreateBackupVaultInputRequestTypeDef",
    "CreateBackupVaultOutputTypeDef",
    "CreateFrameworkOutputTypeDef",
    "ReportDeliveryChannelTypeDef",
    "ReportSettingTypeDef",
    "CreateReportPlanOutputTypeDef",
    "DateRangeTypeDef",
    "DeleteBackupPlanInputRequestTypeDef",
    "DeleteBackupPlanOutputTypeDef",
    "DeleteBackupSelectionInputRequestTypeDef",
    "DeleteBackupVaultAccessPolicyInputRequestTypeDef",
    "DeleteBackupVaultInputRequestTypeDef",
    "DeleteBackupVaultLockConfigurationInputRequestTypeDef",
    "DeleteBackupVaultNotificationsInputRequestTypeDef",
    "DeleteFrameworkInputRequestTypeDef",
    "DeleteRecoveryPointInputRequestTypeDef",
    "DeleteReportPlanInputRequestTypeDef",
    "DescribeBackupJobInputRequestTypeDef",
    "DescribeBackupVaultInputRequestTypeDef",
    "DescribeBackupVaultOutputTypeDef",
    "DescribeCopyJobInputRequestTypeDef",
    "DescribeFrameworkInputRequestTypeDef",
    "DescribeGlobalSettingsOutputTypeDef",
    "DescribeProtectedResourceInputRequestTypeDef",
    "DescribeProtectedResourceOutputTypeDef",
    "DescribeRecoveryPointInputRequestTypeDef",
    "DescribeRegionSettingsOutputTypeDef",
    "DescribeReportJobInputRequestTypeDef",
    "DescribeReportPlanInputRequestTypeDef",
    "DescribeRestoreJobInputRequestTypeDef",
    "DescribeRestoreJobOutputTypeDef",
    "DisassociateRecoveryPointFromParentInputRequestTypeDef",
    "DisassociateRecoveryPointInputRequestTypeDef",
    "EmptyResponseMetadataTypeDef",
    "ExportBackupPlanTemplateInputRequestTypeDef",
    "ExportBackupPlanTemplateOutputTypeDef",
    "FrameworkTypeDef",
    "GetBackupPlanFromJSONInputRequestTypeDef",
    "GetBackupPlanFromTemplateInputRequestTypeDef",
    "GetBackupPlanInputRequestTypeDef",
    "GetBackupSelectionInputRequestTypeDef",
    "GetBackupVaultAccessPolicyInputRequestTypeDef",
    "GetBackupVaultAccessPolicyOutputTypeDef",
    "GetBackupVaultNotificationsInputRequestTypeDef",
    "GetBackupVaultNotificationsOutputTypeDef",
    "GetLegalHoldInputRequestTypeDef",
    "GetRecoveryPointRestoreMetadataInputRequestTypeDef",
    "GetRecoveryPointRestoreMetadataOutputTypeDef",
    "GetSupportedResourceTypesOutputTypeDef",
    "LegalHoldTypeDef",
    "ListBackupJobsInputListBackupJobsPaginateTypeDef",
    "ListBackupJobsInputRequestTypeDef",
    "ListBackupPlanTemplatesInputListBackupPlanTemplatesPaginateTypeDef",
    "ListBackupPlanTemplatesInputRequestTypeDef",
    "ListBackupPlanVersionsInputListBackupPlanVersionsPaginateTypeDef",
    "ListBackupPlanVersionsInputRequestTypeDef",
    "ListBackupPlansInputListBackupPlansPaginateTypeDef",
    "ListBackupPlansInputRequestTypeDef",
    "ListBackupSelectionsInputListBackupSelectionsPaginateTypeDef",
    "ListBackupSelectionsInputRequestTypeDef",
    "ListBackupVaultsInputListBackupVaultsPaginateTypeDef",
    "ListBackupVaultsInputRequestTypeDef",
    "ListCopyJobsInputListCopyJobsPaginateTypeDef",
    "ListCopyJobsInputRequestTypeDef",
    "ListFrameworksInputRequestTypeDef",
    "ListLegalHoldsInputListLegalHoldsPaginateTypeDef",
    "ListLegalHoldsInputRequestTypeDef",
    "ListProtectedResourcesInputListProtectedResourcesPaginateTypeDef",
    "ListProtectedResourcesInputRequestTypeDef",
    "ProtectedResourceTypeDef",
    "ListRecoveryPointsByBackupVaultInputListRecoveryPointsByBackupVaultPaginateTypeDef",
    "ListRecoveryPointsByBackupVaultInputRequestTypeDef",
    "ListRecoveryPointsByLegalHoldInputListRecoveryPointsByLegalHoldPaginateTypeDef",
    "ListRecoveryPointsByLegalHoldInputRequestTypeDef",
    "RecoveryPointMemberTypeDef",
    "ListRecoveryPointsByResourceInputListRecoveryPointsByResourcePaginateTypeDef",
    "ListRecoveryPointsByResourceInputRequestTypeDef",
    "RecoveryPointByResourceTypeDef",
    "ListReportJobsInputRequestTypeDef",
    "ListReportPlansInputRequestTypeDef",
    "ListRestoreJobsInputListRestoreJobsPaginateTypeDef",
    "ListRestoreJobsInputRequestTypeDef",
    "RestoreJobsListMemberTypeDef",
    "ListTagsInputRequestTypeDef",
    "ListTagsOutputTypeDef",
    "PaginatorConfigTypeDef",
    "PutBackupVaultAccessPolicyInputRequestTypeDef",
    "PutBackupVaultLockConfigurationInputRequestTypeDef",
    "PutBackupVaultNotificationsInputRequestTypeDef",
    "ReportDestinationTypeDef",
    "ResponseMetadataTypeDef",
    "StartBackupJobOutputTypeDef",
    "StartCopyJobOutputTypeDef",
    "StartReportJobInputRequestTypeDef",
    "StartReportJobOutputTypeDef",
    "StartRestoreJobInputRequestTypeDef",
    "StartRestoreJobOutputTypeDef",
    "StopBackupJobInputRequestTypeDef",
    "TagResourceInputRequestTypeDef",
    "UntagResourceInputRequestTypeDef",
    "UpdateFrameworkOutputTypeDef",
    "UpdateGlobalSettingsInputRequestTypeDef",
    "UpdateRegionSettingsInputRequestTypeDef",
    "UpdateReportPlanOutputTypeDef",
    "BackupPlansListMemberTypeDef",
    "CreateBackupPlanOutputTypeDef",
    "UpdateBackupPlanOutputTypeDef",
    "BackupJobTypeDef",
    "CopyJobTypeDef",
    "DescribeBackupJobOutputTypeDef",
    "ListBackupPlanTemplatesOutputTypeDef",
    "CopyActionTypeDef",
    "StartBackupJobInputRequestTypeDef",
    "StartCopyJobInputRequestTypeDef",
    "UpdateRecoveryPointLifecycleInputRequestTypeDef",
    "ListBackupSelectionsOutputTypeDef",
    "ListBackupVaultsOutputTypeDef",
    "DescribeRecoveryPointOutputTypeDef",
    "RecoveryPointByBackupVaultTypeDef",
    "UpdateRecoveryPointLifecycleOutputTypeDef",
    "ConditionsTypeDef",
    "FrameworkControlTypeDef",
    "CreateReportPlanInputRequestTypeDef",
    "ReportPlanTypeDef",
    "UpdateReportPlanInputRequestTypeDef",
    "RecoveryPointSelectionTypeDef",
    "ListFrameworksOutputTypeDef",
    "ListLegalHoldsOutputTypeDef",
    "ListProtectedResourcesOutputTypeDef",
    "ListRecoveryPointsByLegalHoldOutputTypeDef",
    "ListRecoveryPointsByResourceOutputTypeDef",
    "ListRestoreJobsOutputTypeDef",
    "ReportJobTypeDef",
    "ListBackupPlanVersionsOutputTypeDef",
    "ListBackupPlansOutputTypeDef",
    "ListBackupJobsOutputTypeDef",
    "DescribeCopyJobOutputTypeDef",
    "ListCopyJobsOutputTypeDef",
    "BackupRuleInputTypeDef",
    "BackupRuleTypeDef",
    "ListRecoveryPointsByBackupVaultOutputTypeDef",
    "BackupSelectionTypeDef",
    "CreateFrameworkInputRequestTypeDef",
    "DescribeFrameworkOutputTypeDef",
    "UpdateFrameworkInputRequestTypeDef",
    "DescribeReportPlanOutputTypeDef",
    "ListReportPlansOutputTypeDef",
    "CreateLegalHoldInputRequestTypeDef",
    "CreateLegalHoldOutputTypeDef",
    "GetLegalHoldOutputTypeDef",
    "DescribeReportJobOutputTypeDef",
    "ListReportJobsOutputTypeDef",
    "BackupPlanInputTypeDef",
    "BackupPlanTypeDef",
    "CreateBackupSelectionInputRequestTypeDef",
    "GetBackupSelectionOutputTypeDef",
    "CreateBackupPlanInputRequestTypeDef",
    "UpdateBackupPlanInputRequestTypeDef",
    "GetBackupPlanFromJSONOutputTypeDef",
    "GetBackupPlanFromTemplateOutputTypeDef",
    "GetBackupPlanOutputTypeDef",
)

AdvancedBackupSettingTypeDef = TypedDict(
    "AdvancedBackupSettingTypeDef",
    {
        "ResourceType": str,
        "BackupOptions": Mapping[str, str],
    },
    total=False,
)

RecoveryPointCreatorTypeDef = TypedDict(
    "RecoveryPointCreatorTypeDef",
    {
        "BackupPlanId": str,
        "BackupPlanArn": str,
        "BackupPlanVersion": str,
        "BackupRuleId": str,
    },
    total=False,
)

BackupPlanTemplatesListMemberTypeDef = TypedDict(
    "BackupPlanTemplatesListMemberTypeDef",
    {
        "BackupPlanTemplateId": str,
        "BackupPlanTemplateName": str,
    },
    total=False,
)

LifecycleTypeDef = TypedDict(
    "LifecycleTypeDef",
    {
        "MoveToColdStorageAfterDays": int,
        "DeleteAfterDays": int,
    },
    total=False,
)

ConditionTypeDef = TypedDict(
    "ConditionTypeDef",
    {
        "ConditionType": Literal["STRINGEQUALS"],
        "ConditionKey": str,
        "ConditionValue": str,
    },
)

BackupSelectionsListMemberTypeDef = TypedDict(
    "BackupSelectionsListMemberTypeDef",
    {
        "SelectionId": str,
        "SelectionName": str,
        "BackupPlanId": str,
        "CreationDate": datetime,
        "CreatorRequestId": str,
        "IamRoleArn": str,
    },
    total=False,
)

BackupVaultListMemberTypeDef = TypedDict(
    "BackupVaultListMemberTypeDef",
    {
        "BackupVaultName": str,
        "BackupVaultArn": str,
        "CreationDate": datetime,
        "EncryptionKeyArn": str,
        "CreatorRequestId": str,
        "NumberOfRecoveryPoints": int,
        "Locked": bool,
        "MinRetentionDays": int,
        "MaxRetentionDays": int,
        "LockDate": datetime,
    },
    total=False,
)

CalculatedLifecycleTypeDef = TypedDict(
    "CalculatedLifecycleTypeDef",
    {
        "MoveToColdStorageAt": datetime,
        "DeleteAt": datetime,
    },
    total=False,
)

_RequiredCancelLegalHoldInputRequestTypeDef = TypedDict(
    "_RequiredCancelLegalHoldInputRequestTypeDef",
    {
        "LegalHoldId": str,
        "CancelDescription": str,
    },
)
_OptionalCancelLegalHoldInputRequestTypeDef = TypedDict(
    "_OptionalCancelLegalHoldInputRequestTypeDef",
    {
        "RetainRecordInDays": int,
    },
    total=False,
)

class CancelLegalHoldInputRequestTypeDef(
    _RequiredCancelLegalHoldInputRequestTypeDef, _OptionalCancelLegalHoldInputRequestTypeDef
):
    pass

ConditionParameterTypeDef = TypedDict(
    "ConditionParameterTypeDef",
    {
        "ConditionKey": str,
        "ConditionValue": str,
    },
    total=False,
)

ControlInputParameterTypeDef = TypedDict(
    "ControlInputParameterTypeDef",
    {
        "ParameterName": str,
        "ParameterValue": str,
    },
    total=False,
)

ControlScopeTypeDef = TypedDict(
    "ControlScopeTypeDef",
    {
        "ComplianceResourceIds": Sequence[str],
        "ComplianceResourceTypes": Sequence[str],
        "Tags": Mapping[str, str],
    },
    total=False,
)

CreateBackupSelectionOutputTypeDef = TypedDict(
    "CreateBackupSelectionOutputTypeDef",
    {
        "SelectionId": str,
        "BackupPlanId": str,
        "CreationDate": datetime,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateBackupVaultInputRequestTypeDef = TypedDict(
    "_RequiredCreateBackupVaultInputRequestTypeDef",
    {
        "BackupVaultName": str,
    },
)
_OptionalCreateBackupVaultInputRequestTypeDef = TypedDict(
    "_OptionalCreateBackupVaultInputRequestTypeDef",
    {
        "BackupVaultTags": Mapping[str, str],
        "EncryptionKeyArn": str,
        "CreatorRequestId": str,
    },
    total=False,
)

class CreateBackupVaultInputRequestTypeDef(
    _RequiredCreateBackupVaultInputRequestTypeDef, _OptionalCreateBackupVaultInputRequestTypeDef
):
    pass

CreateBackupVaultOutputTypeDef = TypedDict(
    "CreateBackupVaultOutputTypeDef",
    {
        "BackupVaultName": str,
        "BackupVaultArn": str,
        "CreationDate": datetime,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateFrameworkOutputTypeDef = TypedDict(
    "CreateFrameworkOutputTypeDef",
    {
        "FrameworkName": str,
        "FrameworkArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredReportDeliveryChannelTypeDef = TypedDict(
    "_RequiredReportDeliveryChannelTypeDef",
    {
        "S3BucketName": str,
    },
)
_OptionalReportDeliveryChannelTypeDef = TypedDict(
    "_OptionalReportDeliveryChannelTypeDef",
    {
        "S3KeyPrefix": str,
        "Formats": Sequence[str],
    },
    total=False,
)

class ReportDeliveryChannelTypeDef(
    _RequiredReportDeliveryChannelTypeDef, _OptionalReportDeliveryChannelTypeDef
):
    pass

_RequiredReportSettingTypeDef = TypedDict(
    "_RequiredReportSettingTypeDef",
    {
        "ReportTemplate": str,
    },
)
_OptionalReportSettingTypeDef = TypedDict(
    "_OptionalReportSettingTypeDef",
    {
        "FrameworkArns": Sequence[str],
        "NumberOfFrameworks": int,
        "Accounts": Sequence[str],
        "OrganizationUnits": Sequence[str],
        "Regions": Sequence[str],
    },
    total=False,
)

class ReportSettingTypeDef(_RequiredReportSettingTypeDef, _OptionalReportSettingTypeDef):
    pass

CreateReportPlanOutputTypeDef = TypedDict(
    "CreateReportPlanOutputTypeDef",
    {
        "ReportPlanName": str,
        "ReportPlanArn": str,
        "CreationTime": datetime,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DateRangeTypeDef = TypedDict(
    "DateRangeTypeDef",
    {
        "FromDate": Union[datetime, str],
        "ToDate": Union[datetime, str],
    },
)

DeleteBackupPlanInputRequestTypeDef = TypedDict(
    "DeleteBackupPlanInputRequestTypeDef",
    {
        "BackupPlanId": str,
    },
)

DeleteBackupPlanOutputTypeDef = TypedDict(
    "DeleteBackupPlanOutputTypeDef",
    {
        "BackupPlanId": str,
        "BackupPlanArn": str,
        "DeletionDate": datetime,
        "VersionId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteBackupSelectionInputRequestTypeDef = TypedDict(
    "DeleteBackupSelectionInputRequestTypeDef",
    {
        "BackupPlanId": str,
        "SelectionId": str,
    },
)

DeleteBackupVaultAccessPolicyInputRequestTypeDef = TypedDict(
    "DeleteBackupVaultAccessPolicyInputRequestTypeDef",
    {
        "BackupVaultName": str,
    },
)

DeleteBackupVaultInputRequestTypeDef = TypedDict(
    "DeleteBackupVaultInputRequestTypeDef",
    {
        "BackupVaultName": str,
    },
)

DeleteBackupVaultLockConfigurationInputRequestTypeDef = TypedDict(
    "DeleteBackupVaultLockConfigurationInputRequestTypeDef",
    {
        "BackupVaultName": str,
    },
)

DeleteBackupVaultNotificationsInputRequestTypeDef = TypedDict(
    "DeleteBackupVaultNotificationsInputRequestTypeDef",
    {
        "BackupVaultName": str,
    },
)

DeleteFrameworkInputRequestTypeDef = TypedDict(
    "DeleteFrameworkInputRequestTypeDef",
    {
        "FrameworkName": str,
    },
)

DeleteRecoveryPointInputRequestTypeDef = TypedDict(
    "DeleteRecoveryPointInputRequestTypeDef",
    {
        "BackupVaultName": str,
        "RecoveryPointArn": str,
    },
)

DeleteReportPlanInputRequestTypeDef = TypedDict(
    "DeleteReportPlanInputRequestTypeDef",
    {
        "ReportPlanName": str,
    },
)

DescribeBackupJobInputRequestTypeDef = TypedDict(
    "DescribeBackupJobInputRequestTypeDef",
    {
        "BackupJobId": str,
    },
)

DescribeBackupVaultInputRequestTypeDef = TypedDict(
    "DescribeBackupVaultInputRequestTypeDef",
    {
        "BackupVaultName": str,
    },
)

DescribeBackupVaultOutputTypeDef = TypedDict(
    "DescribeBackupVaultOutputTypeDef",
    {
        "BackupVaultName": str,
        "BackupVaultArn": str,
        "EncryptionKeyArn": str,
        "CreationDate": datetime,
        "CreatorRequestId": str,
        "NumberOfRecoveryPoints": int,
        "Locked": bool,
        "MinRetentionDays": int,
        "MaxRetentionDays": int,
        "LockDate": datetime,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeCopyJobInputRequestTypeDef = TypedDict(
    "DescribeCopyJobInputRequestTypeDef",
    {
        "CopyJobId": str,
    },
)

DescribeFrameworkInputRequestTypeDef = TypedDict(
    "DescribeFrameworkInputRequestTypeDef",
    {
        "FrameworkName": str,
    },
)

DescribeGlobalSettingsOutputTypeDef = TypedDict(
    "DescribeGlobalSettingsOutputTypeDef",
    {
        "GlobalSettings": Dict[str, str],
        "LastUpdateTime": datetime,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeProtectedResourceInputRequestTypeDef = TypedDict(
    "DescribeProtectedResourceInputRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

DescribeProtectedResourceOutputTypeDef = TypedDict(
    "DescribeProtectedResourceOutputTypeDef",
    {
        "ResourceArn": str,
        "ResourceType": str,
        "LastBackupTime": datetime,
        "ResourceName": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeRecoveryPointInputRequestTypeDef = TypedDict(
    "DescribeRecoveryPointInputRequestTypeDef",
    {
        "BackupVaultName": str,
        "RecoveryPointArn": str,
    },
)

DescribeRegionSettingsOutputTypeDef = TypedDict(
    "DescribeRegionSettingsOutputTypeDef",
    {
        "ResourceTypeOptInPreference": Dict[str, bool],
        "ResourceTypeManagementPreference": Dict[str, bool],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeReportJobInputRequestTypeDef = TypedDict(
    "DescribeReportJobInputRequestTypeDef",
    {
        "ReportJobId": str,
    },
)

DescribeReportPlanInputRequestTypeDef = TypedDict(
    "DescribeReportPlanInputRequestTypeDef",
    {
        "ReportPlanName": str,
    },
)

DescribeRestoreJobInputRequestTypeDef = TypedDict(
    "DescribeRestoreJobInputRequestTypeDef",
    {
        "RestoreJobId": str,
    },
)

DescribeRestoreJobOutputTypeDef = TypedDict(
    "DescribeRestoreJobOutputTypeDef",
    {
        "AccountId": str,
        "RestoreJobId": str,
        "RecoveryPointArn": str,
        "CreationDate": datetime,
        "CompletionDate": datetime,
        "Status": RestoreJobStatusType,
        "StatusMessage": str,
        "PercentDone": str,
        "BackupSizeInBytes": int,
        "IamRoleArn": str,
        "ExpectedCompletionTimeMinutes": int,
        "CreatedResourceArn": str,
        "ResourceType": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DisassociateRecoveryPointFromParentInputRequestTypeDef = TypedDict(
    "DisassociateRecoveryPointFromParentInputRequestTypeDef",
    {
        "BackupVaultName": str,
        "RecoveryPointArn": str,
    },
)

DisassociateRecoveryPointInputRequestTypeDef = TypedDict(
    "DisassociateRecoveryPointInputRequestTypeDef",
    {
        "BackupVaultName": str,
        "RecoveryPointArn": str,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ExportBackupPlanTemplateInputRequestTypeDef = TypedDict(
    "ExportBackupPlanTemplateInputRequestTypeDef",
    {
        "BackupPlanId": str,
    },
)

ExportBackupPlanTemplateOutputTypeDef = TypedDict(
    "ExportBackupPlanTemplateOutputTypeDef",
    {
        "BackupPlanTemplateJson": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

FrameworkTypeDef = TypedDict(
    "FrameworkTypeDef",
    {
        "FrameworkName": str,
        "FrameworkArn": str,
        "FrameworkDescription": str,
        "NumberOfControls": int,
        "CreationTime": datetime,
        "DeploymentStatus": str,
    },
    total=False,
)

GetBackupPlanFromJSONInputRequestTypeDef = TypedDict(
    "GetBackupPlanFromJSONInputRequestTypeDef",
    {
        "BackupPlanTemplateJson": str,
    },
)

GetBackupPlanFromTemplateInputRequestTypeDef = TypedDict(
    "GetBackupPlanFromTemplateInputRequestTypeDef",
    {
        "BackupPlanTemplateId": str,
    },
)

_RequiredGetBackupPlanInputRequestTypeDef = TypedDict(
    "_RequiredGetBackupPlanInputRequestTypeDef",
    {
        "BackupPlanId": str,
    },
)
_OptionalGetBackupPlanInputRequestTypeDef = TypedDict(
    "_OptionalGetBackupPlanInputRequestTypeDef",
    {
        "VersionId": str,
    },
    total=False,
)

class GetBackupPlanInputRequestTypeDef(
    _RequiredGetBackupPlanInputRequestTypeDef, _OptionalGetBackupPlanInputRequestTypeDef
):
    pass

GetBackupSelectionInputRequestTypeDef = TypedDict(
    "GetBackupSelectionInputRequestTypeDef",
    {
        "BackupPlanId": str,
        "SelectionId": str,
    },
)

GetBackupVaultAccessPolicyInputRequestTypeDef = TypedDict(
    "GetBackupVaultAccessPolicyInputRequestTypeDef",
    {
        "BackupVaultName": str,
    },
)

GetBackupVaultAccessPolicyOutputTypeDef = TypedDict(
    "GetBackupVaultAccessPolicyOutputTypeDef",
    {
        "BackupVaultName": str,
        "BackupVaultArn": str,
        "Policy": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetBackupVaultNotificationsInputRequestTypeDef = TypedDict(
    "GetBackupVaultNotificationsInputRequestTypeDef",
    {
        "BackupVaultName": str,
    },
)

GetBackupVaultNotificationsOutputTypeDef = TypedDict(
    "GetBackupVaultNotificationsOutputTypeDef",
    {
        "BackupVaultName": str,
        "BackupVaultArn": str,
        "SNSTopicArn": str,
        "BackupVaultEvents": List[BackupVaultEventType],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetLegalHoldInputRequestTypeDef = TypedDict(
    "GetLegalHoldInputRequestTypeDef",
    {
        "LegalHoldId": str,
    },
)

GetRecoveryPointRestoreMetadataInputRequestTypeDef = TypedDict(
    "GetRecoveryPointRestoreMetadataInputRequestTypeDef",
    {
        "BackupVaultName": str,
        "RecoveryPointArn": str,
    },
)

GetRecoveryPointRestoreMetadataOutputTypeDef = TypedDict(
    "GetRecoveryPointRestoreMetadataOutputTypeDef",
    {
        "BackupVaultArn": str,
        "RecoveryPointArn": str,
        "RestoreMetadata": Dict[str, str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetSupportedResourceTypesOutputTypeDef = TypedDict(
    "GetSupportedResourceTypesOutputTypeDef",
    {
        "ResourceTypes": List[str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

LegalHoldTypeDef = TypedDict(
    "LegalHoldTypeDef",
    {
        "Title": str,
        "Status": LegalHoldStatusType,
        "Description": str,
        "LegalHoldId": str,
        "LegalHoldArn": str,
        "CreationDate": datetime,
        "CancellationDate": datetime,
    },
    total=False,
)

ListBackupJobsInputListBackupJobsPaginateTypeDef = TypedDict(
    "ListBackupJobsInputListBackupJobsPaginateTypeDef",
    {
        "ByResourceArn": str,
        "ByState": BackupJobStateType,
        "ByBackupVaultName": str,
        "ByCreatedBefore": Union[datetime, str],
        "ByCreatedAfter": Union[datetime, str],
        "ByResourceType": str,
        "ByAccountId": str,
        "ByCompleteAfter": Union[datetime, str],
        "ByCompleteBefore": Union[datetime, str],
        "ByParentJobId": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListBackupJobsInputRequestTypeDef = TypedDict(
    "ListBackupJobsInputRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "ByResourceArn": str,
        "ByState": BackupJobStateType,
        "ByBackupVaultName": str,
        "ByCreatedBefore": Union[datetime, str],
        "ByCreatedAfter": Union[datetime, str],
        "ByResourceType": str,
        "ByAccountId": str,
        "ByCompleteAfter": Union[datetime, str],
        "ByCompleteBefore": Union[datetime, str],
        "ByParentJobId": str,
    },
    total=False,
)

ListBackupPlanTemplatesInputListBackupPlanTemplatesPaginateTypeDef = TypedDict(
    "ListBackupPlanTemplatesInputListBackupPlanTemplatesPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListBackupPlanTemplatesInputRequestTypeDef = TypedDict(
    "ListBackupPlanTemplatesInputRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

_RequiredListBackupPlanVersionsInputListBackupPlanVersionsPaginateTypeDef = TypedDict(
    "_RequiredListBackupPlanVersionsInputListBackupPlanVersionsPaginateTypeDef",
    {
        "BackupPlanId": str,
    },
)
_OptionalListBackupPlanVersionsInputListBackupPlanVersionsPaginateTypeDef = TypedDict(
    "_OptionalListBackupPlanVersionsInputListBackupPlanVersionsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

class ListBackupPlanVersionsInputListBackupPlanVersionsPaginateTypeDef(
    _RequiredListBackupPlanVersionsInputListBackupPlanVersionsPaginateTypeDef,
    _OptionalListBackupPlanVersionsInputListBackupPlanVersionsPaginateTypeDef,
):
    pass

_RequiredListBackupPlanVersionsInputRequestTypeDef = TypedDict(
    "_RequiredListBackupPlanVersionsInputRequestTypeDef",
    {
        "BackupPlanId": str,
    },
)
_OptionalListBackupPlanVersionsInputRequestTypeDef = TypedDict(
    "_OptionalListBackupPlanVersionsInputRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListBackupPlanVersionsInputRequestTypeDef(
    _RequiredListBackupPlanVersionsInputRequestTypeDef,
    _OptionalListBackupPlanVersionsInputRequestTypeDef,
):
    pass

ListBackupPlansInputListBackupPlansPaginateTypeDef = TypedDict(
    "ListBackupPlansInputListBackupPlansPaginateTypeDef",
    {
        "IncludeDeleted": bool,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListBackupPlansInputRequestTypeDef = TypedDict(
    "ListBackupPlansInputRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "IncludeDeleted": bool,
    },
    total=False,
)

_RequiredListBackupSelectionsInputListBackupSelectionsPaginateTypeDef = TypedDict(
    "_RequiredListBackupSelectionsInputListBackupSelectionsPaginateTypeDef",
    {
        "BackupPlanId": str,
    },
)
_OptionalListBackupSelectionsInputListBackupSelectionsPaginateTypeDef = TypedDict(
    "_OptionalListBackupSelectionsInputListBackupSelectionsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

class ListBackupSelectionsInputListBackupSelectionsPaginateTypeDef(
    _RequiredListBackupSelectionsInputListBackupSelectionsPaginateTypeDef,
    _OptionalListBackupSelectionsInputListBackupSelectionsPaginateTypeDef,
):
    pass

_RequiredListBackupSelectionsInputRequestTypeDef = TypedDict(
    "_RequiredListBackupSelectionsInputRequestTypeDef",
    {
        "BackupPlanId": str,
    },
)
_OptionalListBackupSelectionsInputRequestTypeDef = TypedDict(
    "_OptionalListBackupSelectionsInputRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListBackupSelectionsInputRequestTypeDef(
    _RequiredListBackupSelectionsInputRequestTypeDef,
    _OptionalListBackupSelectionsInputRequestTypeDef,
):
    pass

ListBackupVaultsInputListBackupVaultsPaginateTypeDef = TypedDict(
    "ListBackupVaultsInputListBackupVaultsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListBackupVaultsInputRequestTypeDef = TypedDict(
    "ListBackupVaultsInputRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListCopyJobsInputListCopyJobsPaginateTypeDef = TypedDict(
    "ListCopyJobsInputListCopyJobsPaginateTypeDef",
    {
        "ByResourceArn": str,
        "ByState": CopyJobStateType,
        "ByCreatedBefore": Union[datetime, str],
        "ByCreatedAfter": Union[datetime, str],
        "ByResourceType": str,
        "ByDestinationVaultArn": str,
        "ByAccountId": str,
        "ByCompleteBefore": Union[datetime, str],
        "ByCompleteAfter": Union[datetime, str],
        "ByParentJobId": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListCopyJobsInputRequestTypeDef = TypedDict(
    "ListCopyJobsInputRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "ByResourceArn": str,
        "ByState": CopyJobStateType,
        "ByCreatedBefore": Union[datetime, str],
        "ByCreatedAfter": Union[datetime, str],
        "ByResourceType": str,
        "ByDestinationVaultArn": str,
        "ByAccountId": str,
        "ByCompleteBefore": Union[datetime, str],
        "ByCompleteAfter": Union[datetime, str],
        "ByParentJobId": str,
    },
    total=False,
)

ListFrameworksInputRequestTypeDef = TypedDict(
    "ListFrameworksInputRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListLegalHoldsInputListLegalHoldsPaginateTypeDef = TypedDict(
    "ListLegalHoldsInputListLegalHoldsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListLegalHoldsInputRequestTypeDef = TypedDict(
    "ListLegalHoldsInputRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListProtectedResourcesInputListProtectedResourcesPaginateTypeDef = TypedDict(
    "ListProtectedResourcesInputListProtectedResourcesPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListProtectedResourcesInputRequestTypeDef = TypedDict(
    "ListProtectedResourcesInputRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ProtectedResourceTypeDef = TypedDict(
    "ProtectedResourceTypeDef",
    {
        "ResourceArn": str,
        "ResourceType": str,
        "LastBackupTime": datetime,
        "ResourceName": str,
    },
    total=False,
)

_RequiredListRecoveryPointsByBackupVaultInputListRecoveryPointsByBackupVaultPaginateTypeDef = TypedDict(
    "_RequiredListRecoveryPointsByBackupVaultInputListRecoveryPointsByBackupVaultPaginateTypeDef",
    {
        "BackupVaultName": str,
    },
)
_OptionalListRecoveryPointsByBackupVaultInputListRecoveryPointsByBackupVaultPaginateTypeDef = TypedDict(
    "_OptionalListRecoveryPointsByBackupVaultInputListRecoveryPointsByBackupVaultPaginateTypeDef",
    {
        "ByResourceArn": str,
        "ByResourceType": str,
        "ByBackupPlanId": str,
        "ByCreatedBefore": Union[datetime, str],
        "ByCreatedAfter": Union[datetime, str],
        "ByParentRecoveryPointArn": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

class ListRecoveryPointsByBackupVaultInputListRecoveryPointsByBackupVaultPaginateTypeDef(
    _RequiredListRecoveryPointsByBackupVaultInputListRecoveryPointsByBackupVaultPaginateTypeDef,
    _OptionalListRecoveryPointsByBackupVaultInputListRecoveryPointsByBackupVaultPaginateTypeDef,
):
    pass

_RequiredListRecoveryPointsByBackupVaultInputRequestTypeDef = TypedDict(
    "_RequiredListRecoveryPointsByBackupVaultInputRequestTypeDef",
    {
        "BackupVaultName": str,
    },
)
_OptionalListRecoveryPointsByBackupVaultInputRequestTypeDef = TypedDict(
    "_OptionalListRecoveryPointsByBackupVaultInputRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "ByResourceArn": str,
        "ByResourceType": str,
        "ByBackupPlanId": str,
        "ByCreatedBefore": Union[datetime, str],
        "ByCreatedAfter": Union[datetime, str],
        "ByParentRecoveryPointArn": str,
    },
    total=False,
)

class ListRecoveryPointsByBackupVaultInputRequestTypeDef(
    _RequiredListRecoveryPointsByBackupVaultInputRequestTypeDef,
    _OptionalListRecoveryPointsByBackupVaultInputRequestTypeDef,
):
    pass

_RequiredListRecoveryPointsByLegalHoldInputListRecoveryPointsByLegalHoldPaginateTypeDef = TypedDict(
    "_RequiredListRecoveryPointsByLegalHoldInputListRecoveryPointsByLegalHoldPaginateTypeDef",
    {
        "LegalHoldId": str,
    },
)
_OptionalListRecoveryPointsByLegalHoldInputListRecoveryPointsByLegalHoldPaginateTypeDef = TypedDict(
    "_OptionalListRecoveryPointsByLegalHoldInputListRecoveryPointsByLegalHoldPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

class ListRecoveryPointsByLegalHoldInputListRecoveryPointsByLegalHoldPaginateTypeDef(
    _RequiredListRecoveryPointsByLegalHoldInputListRecoveryPointsByLegalHoldPaginateTypeDef,
    _OptionalListRecoveryPointsByLegalHoldInputListRecoveryPointsByLegalHoldPaginateTypeDef,
):
    pass

_RequiredListRecoveryPointsByLegalHoldInputRequestTypeDef = TypedDict(
    "_RequiredListRecoveryPointsByLegalHoldInputRequestTypeDef",
    {
        "LegalHoldId": str,
    },
)
_OptionalListRecoveryPointsByLegalHoldInputRequestTypeDef = TypedDict(
    "_OptionalListRecoveryPointsByLegalHoldInputRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListRecoveryPointsByLegalHoldInputRequestTypeDef(
    _RequiredListRecoveryPointsByLegalHoldInputRequestTypeDef,
    _OptionalListRecoveryPointsByLegalHoldInputRequestTypeDef,
):
    pass

RecoveryPointMemberTypeDef = TypedDict(
    "RecoveryPointMemberTypeDef",
    {
        "RecoveryPointArn": str,
        "ResourceArn": str,
        "ResourceType": str,
        "BackupVaultName": str,
    },
    total=False,
)

_RequiredListRecoveryPointsByResourceInputListRecoveryPointsByResourcePaginateTypeDef = TypedDict(
    "_RequiredListRecoveryPointsByResourceInputListRecoveryPointsByResourcePaginateTypeDef",
    {
        "ResourceArn": str,
    },
)
_OptionalListRecoveryPointsByResourceInputListRecoveryPointsByResourcePaginateTypeDef = TypedDict(
    "_OptionalListRecoveryPointsByResourceInputListRecoveryPointsByResourcePaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

class ListRecoveryPointsByResourceInputListRecoveryPointsByResourcePaginateTypeDef(
    _RequiredListRecoveryPointsByResourceInputListRecoveryPointsByResourcePaginateTypeDef,
    _OptionalListRecoveryPointsByResourceInputListRecoveryPointsByResourcePaginateTypeDef,
):
    pass

_RequiredListRecoveryPointsByResourceInputRequestTypeDef = TypedDict(
    "_RequiredListRecoveryPointsByResourceInputRequestTypeDef",
    {
        "ResourceArn": str,
    },
)
_OptionalListRecoveryPointsByResourceInputRequestTypeDef = TypedDict(
    "_OptionalListRecoveryPointsByResourceInputRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListRecoveryPointsByResourceInputRequestTypeDef(
    _RequiredListRecoveryPointsByResourceInputRequestTypeDef,
    _OptionalListRecoveryPointsByResourceInputRequestTypeDef,
):
    pass

RecoveryPointByResourceTypeDef = TypedDict(
    "RecoveryPointByResourceTypeDef",
    {
        "RecoveryPointArn": str,
        "CreationDate": datetime,
        "Status": RecoveryPointStatusType,
        "StatusMessage": str,
        "EncryptionKeyArn": str,
        "BackupSizeBytes": int,
        "BackupVaultName": str,
        "IsParent": bool,
        "ParentRecoveryPointArn": str,
        "ResourceName": str,
    },
    total=False,
)

ListReportJobsInputRequestTypeDef = TypedDict(
    "ListReportJobsInputRequestTypeDef",
    {
        "ByReportPlanName": str,
        "ByCreationBefore": Union[datetime, str],
        "ByCreationAfter": Union[datetime, str],
        "ByStatus": str,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListReportPlansInputRequestTypeDef = TypedDict(
    "ListReportPlansInputRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListRestoreJobsInputListRestoreJobsPaginateTypeDef = TypedDict(
    "ListRestoreJobsInputListRestoreJobsPaginateTypeDef",
    {
        "ByAccountId": str,
        "ByCreatedBefore": Union[datetime, str],
        "ByCreatedAfter": Union[datetime, str],
        "ByStatus": RestoreJobStatusType,
        "ByCompleteBefore": Union[datetime, str],
        "ByCompleteAfter": Union[datetime, str],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListRestoreJobsInputRequestTypeDef = TypedDict(
    "ListRestoreJobsInputRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "ByAccountId": str,
        "ByCreatedBefore": Union[datetime, str],
        "ByCreatedAfter": Union[datetime, str],
        "ByStatus": RestoreJobStatusType,
        "ByCompleteBefore": Union[datetime, str],
        "ByCompleteAfter": Union[datetime, str],
    },
    total=False,
)

RestoreJobsListMemberTypeDef = TypedDict(
    "RestoreJobsListMemberTypeDef",
    {
        "AccountId": str,
        "RestoreJobId": str,
        "RecoveryPointArn": str,
        "CreationDate": datetime,
        "CompletionDate": datetime,
        "Status": RestoreJobStatusType,
        "StatusMessage": str,
        "PercentDone": str,
        "BackupSizeInBytes": int,
        "IamRoleArn": str,
        "ExpectedCompletionTimeMinutes": int,
        "CreatedResourceArn": str,
        "ResourceType": str,
    },
    total=False,
)

_RequiredListTagsInputRequestTypeDef = TypedDict(
    "_RequiredListTagsInputRequestTypeDef",
    {
        "ResourceArn": str,
    },
)
_OptionalListTagsInputRequestTypeDef = TypedDict(
    "_OptionalListTagsInputRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListTagsInputRequestTypeDef(
    _RequiredListTagsInputRequestTypeDef, _OptionalListTagsInputRequestTypeDef
):
    pass

ListTagsOutputTypeDef = TypedDict(
    "ListTagsOutputTypeDef",
    {
        "NextToken": str,
        "Tags": Dict[str, str],
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

_RequiredPutBackupVaultAccessPolicyInputRequestTypeDef = TypedDict(
    "_RequiredPutBackupVaultAccessPolicyInputRequestTypeDef",
    {
        "BackupVaultName": str,
    },
)
_OptionalPutBackupVaultAccessPolicyInputRequestTypeDef = TypedDict(
    "_OptionalPutBackupVaultAccessPolicyInputRequestTypeDef",
    {
        "Policy": str,
    },
    total=False,
)

class PutBackupVaultAccessPolicyInputRequestTypeDef(
    _RequiredPutBackupVaultAccessPolicyInputRequestTypeDef,
    _OptionalPutBackupVaultAccessPolicyInputRequestTypeDef,
):
    pass

_RequiredPutBackupVaultLockConfigurationInputRequestTypeDef = TypedDict(
    "_RequiredPutBackupVaultLockConfigurationInputRequestTypeDef",
    {
        "BackupVaultName": str,
    },
)
_OptionalPutBackupVaultLockConfigurationInputRequestTypeDef = TypedDict(
    "_OptionalPutBackupVaultLockConfigurationInputRequestTypeDef",
    {
        "MinRetentionDays": int,
        "MaxRetentionDays": int,
        "ChangeableForDays": int,
    },
    total=False,
)

class PutBackupVaultLockConfigurationInputRequestTypeDef(
    _RequiredPutBackupVaultLockConfigurationInputRequestTypeDef,
    _OptionalPutBackupVaultLockConfigurationInputRequestTypeDef,
):
    pass

PutBackupVaultNotificationsInputRequestTypeDef = TypedDict(
    "PutBackupVaultNotificationsInputRequestTypeDef",
    {
        "BackupVaultName": str,
        "SNSTopicArn": str,
        "BackupVaultEvents": Sequence[BackupVaultEventType],
    },
)

ReportDestinationTypeDef = TypedDict(
    "ReportDestinationTypeDef",
    {
        "S3BucketName": str,
        "S3Keys": List[str],
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

StartBackupJobOutputTypeDef = TypedDict(
    "StartBackupJobOutputTypeDef",
    {
        "BackupJobId": str,
        "RecoveryPointArn": str,
        "CreationDate": datetime,
        "IsParent": bool,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StartCopyJobOutputTypeDef = TypedDict(
    "StartCopyJobOutputTypeDef",
    {
        "CopyJobId": str,
        "CreationDate": datetime,
        "IsParent": bool,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredStartReportJobInputRequestTypeDef = TypedDict(
    "_RequiredStartReportJobInputRequestTypeDef",
    {
        "ReportPlanName": str,
    },
)
_OptionalStartReportJobInputRequestTypeDef = TypedDict(
    "_OptionalStartReportJobInputRequestTypeDef",
    {
        "IdempotencyToken": str,
    },
    total=False,
)

class StartReportJobInputRequestTypeDef(
    _RequiredStartReportJobInputRequestTypeDef, _OptionalStartReportJobInputRequestTypeDef
):
    pass

StartReportJobOutputTypeDef = TypedDict(
    "StartReportJobOutputTypeDef",
    {
        "ReportJobId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredStartRestoreJobInputRequestTypeDef = TypedDict(
    "_RequiredStartRestoreJobInputRequestTypeDef",
    {
        "RecoveryPointArn": str,
        "Metadata": Mapping[str, str],
    },
)
_OptionalStartRestoreJobInputRequestTypeDef = TypedDict(
    "_OptionalStartRestoreJobInputRequestTypeDef",
    {
        "IamRoleArn": str,
        "IdempotencyToken": str,
        "ResourceType": str,
        "CopySourceTagsToRestoredResource": bool,
    },
    total=False,
)

class StartRestoreJobInputRequestTypeDef(
    _RequiredStartRestoreJobInputRequestTypeDef, _OptionalStartRestoreJobInputRequestTypeDef
):
    pass

StartRestoreJobOutputTypeDef = TypedDict(
    "StartRestoreJobOutputTypeDef",
    {
        "RestoreJobId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StopBackupJobInputRequestTypeDef = TypedDict(
    "StopBackupJobInputRequestTypeDef",
    {
        "BackupJobId": str,
    },
)

TagResourceInputRequestTypeDef = TypedDict(
    "TagResourceInputRequestTypeDef",
    {
        "ResourceArn": str,
        "Tags": Mapping[str, str],
    },
)

UntagResourceInputRequestTypeDef = TypedDict(
    "UntagResourceInputRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeyList": Sequence[str],
    },
)

UpdateFrameworkOutputTypeDef = TypedDict(
    "UpdateFrameworkOutputTypeDef",
    {
        "FrameworkName": str,
        "FrameworkArn": str,
        "CreationTime": datetime,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateGlobalSettingsInputRequestTypeDef = TypedDict(
    "UpdateGlobalSettingsInputRequestTypeDef",
    {
        "GlobalSettings": Mapping[str, str],
    },
    total=False,
)

UpdateRegionSettingsInputRequestTypeDef = TypedDict(
    "UpdateRegionSettingsInputRequestTypeDef",
    {
        "ResourceTypeOptInPreference": Mapping[str, bool],
        "ResourceTypeManagementPreference": Mapping[str, bool],
    },
    total=False,
)

UpdateReportPlanOutputTypeDef = TypedDict(
    "UpdateReportPlanOutputTypeDef",
    {
        "ReportPlanName": str,
        "ReportPlanArn": str,
        "CreationTime": datetime,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

BackupPlansListMemberTypeDef = TypedDict(
    "BackupPlansListMemberTypeDef",
    {
        "BackupPlanArn": str,
        "BackupPlanId": str,
        "CreationDate": datetime,
        "DeletionDate": datetime,
        "VersionId": str,
        "BackupPlanName": str,
        "CreatorRequestId": str,
        "LastExecutionDate": datetime,
        "AdvancedBackupSettings": List[AdvancedBackupSettingTypeDef],
    },
    total=False,
)

CreateBackupPlanOutputTypeDef = TypedDict(
    "CreateBackupPlanOutputTypeDef",
    {
        "BackupPlanId": str,
        "BackupPlanArn": str,
        "CreationDate": datetime,
        "VersionId": str,
        "AdvancedBackupSettings": List[AdvancedBackupSettingTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateBackupPlanOutputTypeDef = TypedDict(
    "UpdateBackupPlanOutputTypeDef",
    {
        "BackupPlanId": str,
        "BackupPlanArn": str,
        "CreationDate": datetime,
        "VersionId": str,
        "AdvancedBackupSettings": List[AdvancedBackupSettingTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

BackupJobTypeDef = TypedDict(
    "BackupJobTypeDef",
    {
        "AccountId": str,
        "BackupJobId": str,
        "BackupVaultName": str,
        "BackupVaultArn": str,
        "RecoveryPointArn": str,
        "ResourceArn": str,
        "CreationDate": datetime,
        "CompletionDate": datetime,
        "State": BackupJobStateType,
        "StatusMessage": str,
        "PercentDone": str,
        "BackupSizeInBytes": int,
        "IamRoleArn": str,
        "CreatedBy": RecoveryPointCreatorTypeDef,
        "ExpectedCompletionDate": datetime,
        "StartBy": datetime,
        "ResourceType": str,
        "BytesTransferred": int,
        "BackupOptions": Dict[str, str],
        "BackupType": str,
        "ParentJobId": str,
        "IsParent": bool,
        "ResourceName": str,
    },
    total=False,
)

CopyJobTypeDef = TypedDict(
    "CopyJobTypeDef",
    {
        "AccountId": str,
        "CopyJobId": str,
        "SourceBackupVaultArn": str,
        "SourceRecoveryPointArn": str,
        "DestinationBackupVaultArn": str,
        "DestinationRecoveryPointArn": str,
        "ResourceArn": str,
        "CreationDate": datetime,
        "CompletionDate": datetime,
        "State": CopyJobStateType,
        "StatusMessage": str,
        "BackupSizeInBytes": int,
        "IamRoleArn": str,
        "CreatedBy": RecoveryPointCreatorTypeDef,
        "ResourceType": str,
        "ParentJobId": str,
        "IsParent": bool,
        "CompositeMemberIdentifier": str,
        "NumberOfChildJobs": int,
        "ChildJobsInState": Dict[CopyJobStateType, int],
        "ResourceName": str,
    },
    total=False,
)

DescribeBackupJobOutputTypeDef = TypedDict(
    "DescribeBackupJobOutputTypeDef",
    {
        "AccountId": str,
        "BackupJobId": str,
        "BackupVaultName": str,
        "BackupVaultArn": str,
        "RecoveryPointArn": str,
        "ResourceArn": str,
        "CreationDate": datetime,
        "CompletionDate": datetime,
        "State": BackupJobStateType,
        "StatusMessage": str,
        "PercentDone": str,
        "BackupSizeInBytes": int,
        "IamRoleArn": str,
        "CreatedBy": RecoveryPointCreatorTypeDef,
        "ResourceType": str,
        "BytesTransferred": int,
        "ExpectedCompletionDate": datetime,
        "StartBy": datetime,
        "BackupOptions": Dict[str, str],
        "BackupType": str,
        "ParentJobId": str,
        "IsParent": bool,
        "NumberOfChildJobs": int,
        "ChildJobsInState": Dict[BackupJobStateType, int],
        "ResourceName": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListBackupPlanTemplatesOutputTypeDef = TypedDict(
    "ListBackupPlanTemplatesOutputTypeDef",
    {
        "NextToken": str,
        "BackupPlanTemplatesList": List[BackupPlanTemplatesListMemberTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCopyActionTypeDef = TypedDict(
    "_RequiredCopyActionTypeDef",
    {
        "DestinationBackupVaultArn": str,
    },
)
_OptionalCopyActionTypeDef = TypedDict(
    "_OptionalCopyActionTypeDef",
    {
        "Lifecycle": LifecycleTypeDef,
    },
    total=False,
)

class CopyActionTypeDef(_RequiredCopyActionTypeDef, _OptionalCopyActionTypeDef):
    pass

_RequiredStartBackupJobInputRequestTypeDef = TypedDict(
    "_RequiredStartBackupJobInputRequestTypeDef",
    {
        "BackupVaultName": str,
        "ResourceArn": str,
        "IamRoleArn": str,
    },
)
_OptionalStartBackupJobInputRequestTypeDef = TypedDict(
    "_OptionalStartBackupJobInputRequestTypeDef",
    {
        "IdempotencyToken": str,
        "StartWindowMinutes": int,
        "CompleteWindowMinutes": int,
        "Lifecycle": LifecycleTypeDef,
        "RecoveryPointTags": Mapping[str, str],
        "BackupOptions": Mapping[str, str],
    },
    total=False,
)

class StartBackupJobInputRequestTypeDef(
    _RequiredStartBackupJobInputRequestTypeDef, _OptionalStartBackupJobInputRequestTypeDef
):
    pass

_RequiredStartCopyJobInputRequestTypeDef = TypedDict(
    "_RequiredStartCopyJobInputRequestTypeDef",
    {
        "RecoveryPointArn": str,
        "SourceBackupVaultName": str,
        "DestinationBackupVaultArn": str,
        "IamRoleArn": str,
    },
)
_OptionalStartCopyJobInputRequestTypeDef = TypedDict(
    "_OptionalStartCopyJobInputRequestTypeDef",
    {
        "IdempotencyToken": str,
        "Lifecycle": LifecycleTypeDef,
    },
    total=False,
)

class StartCopyJobInputRequestTypeDef(
    _RequiredStartCopyJobInputRequestTypeDef, _OptionalStartCopyJobInputRequestTypeDef
):
    pass

_RequiredUpdateRecoveryPointLifecycleInputRequestTypeDef = TypedDict(
    "_RequiredUpdateRecoveryPointLifecycleInputRequestTypeDef",
    {
        "BackupVaultName": str,
        "RecoveryPointArn": str,
    },
)
_OptionalUpdateRecoveryPointLifecycleInputRequestTypeDef = TypedDict(
    "_OptionalUpdateRecoveryPointLifecycleInputRequestTypeDef",
    {
        "Lifecycle": LifecycleTypeDef,
    },
    total=False,
)

class UpdateRecoveryPointLifecycleInputRequestTypeDef(
    _RequiredUpdateRecoveryPointLifecycleInputRequestTypeDef,
    _OptionalUpdateRecoveryPointLifecycleInputRequestTypeDef,
):
    pass

ListBackupSelectionsOutputTypeDef = TypedDict(
    "ListBackupSelectionsOutputTypeDef",
    {
        "NextToken": str,
        "BackupSelectionsList": List[BackupSelectionsListMemberTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListBackupVaultsOutputTypeDef = TypedDict(
    "ListBackupVaultsOutputTypeDef",
    {
        "BackupVaultList": List[BackupVaultListMemberTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeRecoveryPointOutputTypeDef = TypedDict(
    "DescribeRecoveryPointOutputTypeDef",
    {
        "RecoveryPointArn": str,
        "BackupVaultName": str,
        "BackupVaultArn": str,
        "SourceBackupVaultArn": str,
        "ResourceArn": str,
        "ResourceType": str,
        "CreatedBy": RecoveryPointCreatorTypeDef,
        "IamRoleArn": str,
        "Status": RecoveryPointStatusType,
        "StatusMessage": str,
        "CreationDate": datetime,
        "CompletionDate": datetime,
        "BackupSizeInBytes": int,
        "CalculatedLifecycle": CalculatedLifecycleTypeDef,
        "Lifecycle": LifecycleTypeDef,
        "EncryptionKeyArn": str,
        "IsEncrypted": bool,
        "StorageClass": StorageClassType,
        "LastRestoreTime": datetime,
        "ParentRecoveryPointArn": str,
        "CompositeMemberIdentifier": str,
        "IsParent": bool,
        "ResourceName": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

RecoveryPointByBackupVaultTypeDef = TypedDict(
    "RecoveryPointByBackupVaultTypeDef",
    {
        "RecoveryPointArn": str,
        "BackupVaultName": str,
        "BackupVaultArn": str,
        "SourceBackupVaultArn": str,
        "ResourceArn": str,
        "ResourceType": str,
        "CreatedBy": RecoveryPointCreatorTypeDef,
        "IamRoleArn": str,
        "Status": RecoveryPointStatusType,
        "StatusMessage": str,
        "CreationDate": datetime,
        "CompletionDate": datetime,
        "BackupSizeInBytes": int,
        "CalculatedLifecycle": CalculatedLifecycleTypeDef,
        "Lifecycle": LifecycleTypeDef,
        "EncryptionKeyArn": str,
        "IsEncrypted": bool,
        "LastRestoreTime": datetime,
        "ParentRecoveryPointArn": str,
        "CompositeMemberIdentifier": str,
        "IsParent": bool,
        "ResourceName": str,
    },
    total=False,
)

UpdateRecoveryPointLifecycleOutputTypeDef = TypedDict(
    "UpdateRecoveryPointLifecycleOutputTypeDef",
    {
        "BackupVaultArn": str,
        "RecoveryPointArn": str,
        "Lifecycle": LifecycleTypeDef,
        "CalculatedLifecycle": CalculatedLifecycleTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ConditionsTypeDef = TypedDict(
    "ConditionsTypeDef",
    {
        "StringEquals": Sequence[ConditionParameterTypeDef],
        "StringNotEquals": Sequence[ConditionParameterTypeDef],
        "StringLike": Sequence[ConditionParameterTypeDef],
        "StringNotLike": Sequence[ConditionParameterTypeDef],
    },
    total=False,
)

_RequiredFrameworkControlTypeDef = TypedDict(
    "_RequiredFrameworkControlTypeDef",
    {
        "ControlName": str,
    },
)
_OptionalFrameworkControlTypeDef = TypedDict(
    "_OptionalFrameworkControlTypeDef",
    {
        "ControlInputParameters": Sequence[ControlInputParameterTypeDef],
        "ControlScope": ControlScopeTypeDef,
    },
    total=False,
)

class FrameworkControlTypeDef(_RequiredFrameworkControlTypeDef, _OptionalFrameworkControlTypeDef):
    pass

_RequiredCreateReportPlanInputRequestTypeDef = TypedDict(
    "_RequiredCreateReportPlanInputRequestTypeDef",
    {
        "ReportPlanName": str,
        "ReportDeliveryChannel": ReportDeliveryChannelTypeDef,
        "ReportSetting": ReportSettingTypeDef,
    },
)
_OptionalCreateReportPlanInputRequestTypeDef = TypedDict(
    "_OptionalCreateReportPlanInputRequestTypeDef",
    {
        "ReportPlanDescription": str,
        "ReportPlanTags": Mapping[str, str],
        "IdempotencyToken": str,
    },
    total=False,
)

class CreateReportPlanInputRequestTypeDef(
    _RequiredCreateReportPlanInputRequestTypeDef, _OptionalCreateReportPlanInputRequestTypeDef
):
    pass

ReportPlanTypeDef = TypedDict(
    "ReportPlanTypeDef",
    {
        "ReportPlanArn": str,
        "ReportPlanName": str,
        "ReportPlanDescription": str,
        "ReportSetting": ReportSettingTypeDef,
        "ReportDeliveryChannel": ReportDeliveryChannelTypeDef,
        "DeploymentStatus": str,
        "CreationTime": datetime,
        "LastAttemptedExecutionTime": datetime,
        "LastSuccessfulExecutionTime": datetime,
    },
    total=False,
)

_RequiredUpdateReportPlanInputRequestTypeDef = TypedDict(
    "_RequiredUpdateReportPlanInputRequestTypeDef",
    {
        "ReportPlanName": str,
    },
)
_OptionalUpdateReportPlanInputRequestTypeDef = TypedDict(
    "_OptionalUpdateReportPlanInputRequestTypeDef",
    {
        "ReportPlanDescription": str,
        "ReportDeliveryChannel": ReportDeliveryChannelTypeDef,
        "ReportSetting": ReportSettingTypeDef,
        "IdempotencyToken": str,
    },
    total=False,
)

class UpdateReportPlanInputRequestTypeDef(
    _RequiredUpdateReportPlanInputRequestTypeDef, _OptionalUpdateReportPlanInputRequestTypeDef
):
    pass

RecoveryPointSelectionTypeDef = TypedDict(
    "RecoveryPointSelectionTypeDef",
    {
        "VaultNames": Sequence[str],
        "ResourceIdentifiers": Sequence[str],
        "DateRange": DateRangeTypeDef,
    },
    total=False,
)

ListFrameworksOutputTypeDef = TypedDict(
    "ListFrameworksOutputTypeDef",
    {
        "Frameworks": List[FrameworkTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListLegalHoldsOutputTypeDef = TypedDict(
    "ListLegalHoldsOutputTypeDef",
    {
        "NextToken": str,
        "LegalHolds": List[LegalHoldTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListProtectedResourcesOutputTypeDef = TypedDict(
    "ListProtectedResourcesOutputTypeDef",
    {
        "Results": List[ProtectedResourceTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListRecoveryPointsByLegalHoldOutputTypeDef = TypedDict(
    "ListRecoveryPointsByLegalHoldOutputTypeDef",
    {
        "RecoveryPoints": List[RecoveryPointMemberTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListRecoveryPointsByResourceOutputTypeDef = TypedDict(
    "ListRecoveryPointsByResourceOutputTypeDef",
    {
        "NextToken": str,
        "RecoveryPoints": List[RecoveryPointByResourceTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListRestoreJobsOutputTypeDef = TypedDict(
    "ListRestoreJobsOutputTypeDef",
    {
        "RestoreJobs": List[RestoreJobsListMemberTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ReportJobTypeDef = TypedDict(
    "ReportJobTypeDef",
    {
        "ReportJobId": str,
        "ReportPlanArn": str,
        "ReportTemplate": str,
        "CreationTime": datetime,
        "CompletionTime": datetime,
        "Status": str,
        "StatusMessage": str,
        "ReportDestination": ReportDestinationTypeDef,
    },
    total=False,
)

ListBackupPlanVersionsOutputTypeDef = TypedDict(
    "ListBackupPlanVersionsOutputTypeDef",
    {
        "NextToken": str,
        "BackupPlanVersionsList": List[BackupPlansListMemberTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListBackupPlansOutputTypeDef = TypedDict(
    "ListBackupPlansOutputTypeDef",
    {
        "NextToken": str,
        "BackupPlansList": List[BackupPlansListMemberTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListBackupJobsOutputTypeDef = TypedDict(
    "ListBackupJobsOutputTypeDef",
    {
        "BackupJobs": List[BackupJobTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeCopyJobOutputTypeDef = TypedDict(
    "DescribeCopyJobOutputTypeDef",
    {
        "CopyJob": CopyJobTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListCopyJobsOutputTypeDef = TypedDict(
    "ListCopyJobsOutputTypeDef",
    {
        "CopyJobs": List[CopyJobTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredBackupRuleInputTypeDef = TypedDict(
    "_RequiredBackupRuleInputTypeDef",
    {
        "RuleName": str,
        "TargetBackupVaultName": str,
    },
)
_OptionalBackupRuleInputTypeDef = TypedDict(
    "_OptionalBackupRuleInputTypeDef",
    {
        "ScheduleExpression": str,
        "StartWindowMinutes": int,
        "CompletionWindowMinutes": int,
        "Lifecycle": LifecycleTypeDef,
        "RecoveryPointTags": Mapping[str, str],
        "CopyActions": Sequence[CopyActionTypeDef],
        "EnableContinuousBackup": bool,
    },
    total=False,
)

class BackupRuleInputTypeDef(_RequiredBackupRuleInputTypeDef, _OptionalBackupRuleInputTypeDef):
    pass

_RequiredBackupRuleTypeDef = TypedDict(
    "_RequiredBackupRuleTypeDef",
    {
        "RuleName": str,
        "TargetBackupVaultName": str,
    },
)
_OptionalBackupRuleTypeDef = TypedDict(
    "_OptionalBackupRuleTypeDef",
    {
        "ScheduleExpression": str,
        "StartWindowMinutes": int,
        "CompletionWindowMinutes": int,
        "Lifecycle": LifecycleTypeDef,
        "RecoveryPointTags": Dict[str, str],
        "RuleId": str,
        "CopyActions": List[CopyActionTypeDef],
        "EnableContinuousBackup": bool,
    },
    total=False,
)

class BackupRuleTypeDef(_RequiredBackupRuleTypeDef, _OptionalBackupRuleTypeDef):
    pass

ListRecoveryPointsByBackupVaultOutputTypeDef = TypedDict(
    "ListRecoveryPointsByBackupVaultOutputTypeDef",
    {
        "NextToken": str,
        "RecoveryPoints": List[RecoveryPointByBackupVaultTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredBackupSelectionTypeDef = TypedDict(
    "_RequiredBackupSelectionTypeDef",
    {
        "SelectionName": str,
        "IamRoleArn": str,
    },
)
_OptionalBackupSelectionTypeDef = TypedDict(
    "_OptionalBackupSelectionTypeDef",
    {
        "Resources": Sequence[str],
        "ListOfTags": Sequence[ConditionTypeDef],
        "NotResources": Sequence[str],
        "Conditions": ConditionsTypeDef,
    },
    total=False,
)

class BackupSelectionTypeDef(_RequiredBackupSelectionTypeDef, _OptionalBackupSelectionTypeDef):
    pass

_RequiredCreateFrameworkInputRequestTypeDef = TypedDict(
    "_RequiredCreateFrameworkInputRequestTypeDef",
    {
        "FrameworkName": str,
        "FrameworkControls": Sequence[FrameworkControlTypeDef],
    },
)
_OptionalCreateFrameworkInputRequestTypeDef = TypedDict(
    "_OptionalCreateFrameworkInputRequestTypeDef",
    {
        "FrameworkDescription": str,
        "IdempotencyToken": str,
        "FrameworkTags": Mapping[str, str],
    },
    total=False,
)

class CreateFrameworkInputRequestTypeDef(
    _RequiredCreateFrameworkInputRequestTypeDef, _OptionalCreateFrameworkInputRequestTypeDef
):
    pass

DescribeFrameworkOutputTypeDef = TypedDict(
    "DescribeFrameworkOutputTypeDef",
    {
        "FrameworkName": str,
        "FrameworkArn": str,
        "FrameworkDescription": str,
        "FrameworkControls": List[FrameworkControlTypeDef],
        "CreationTime": datetime,
        "DeploymentStatus": str,
        "FrameworkStatus": str,
        "IdempotencyToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredUpdateFrameworkInputRequestTypeDef = TypedDict(
    "_RequiredUpdateFrameworkInputRequestTypeDef",
    {
        "FrameworkName": str,
    },
)
_OptionalUpdateFrameworkInputRequestTypeDef = TypedDict(
    "_OptionalUpdateFrameworkInputRequestTypeDef",
    {
        "FrameworkDescription": str,
        "FrameworkControls": Sequence[FrameworkControlTypeDef],
        "IdempotencyToken": str,
    },
    total=False,
)

class UpdateFrameworkInputRequestTypeDef(
    _RequiredUpdateFrameworkInputRequestTypeDef, _OptionalUpdateFrameworkInputRequestTypeDef
):
    pass

DescribeReportPlanOutputTypeDef = TypedDict(
    "DescribeReportPlanOutputTypeDef",
    {
        "ReportPlan": ReportPlanTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListReportPlansOutputTypeDef = TypedDict(
    "ListReportPlansOutputTypeDef",
    {
        "ReportPlans": List[ReportPlanTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateLegalHoldInputRequestTypeDef = TypedDict(
    "_RequiredCreateLegalHoldInputRequestTypeDef",
    {
        "Title": str,
        "Description": str,
    },
)
_OptionalCreateLegalHoldInputRequestTypeDef = TypedDict(
    "_OptionalCreateLegalHoldInputRequestTypeDef",
    {
        "IdempotencyToken": str,
        "RecoveryPointSelection": RecoveryPointSelectionTypeDef,
        "Tags": Mapping[str, str],
    },
    total=False,
)

class CreateLegalHoldInputRequestTypeDef(
    _RequiredCreateLegalHoldInputRequestTypeDef, _OptionalCreateLegalHoldInputRequestTypeDef
):
    pass

CreateLegalHoldOutputTypeDef = TypedDict(
    "CreateLegalHoldOutputTypeDef",
    {
        "Title": str,
        "Status": LegalHoldStatusType,
        "Description": str,
        "LegalHoldId": str,
        "LegalHoldArn": str,
        "CreationDate": datetime,
        "RecoveryPointSelection": RecoveryPointSelectionTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetLegalHoldOutputTypeDef = TypedDict(
    "GetLegalHoldOutputTypeDef",
    {
        "Title": str,
        "Status": LegalHoldStatusType,
        "Description": str,
        "CancelDescription": str,
        "LegalHoldId": str,
        "LegalHoldArn": str,
        "CreationDate": datetime,
        "CancellationDate": datetime,
        "RetainRecordUntil": datetime,
        "RecoveryPointSelection": RecoveryPointSelectionTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeReportJobOutputTypeDef = TypedDict(
    "DescribeReportJobOutputTypeDef",
    {
        "ReportJob": ReportJobTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListReportJobsOutputTypeDef = TypedDict(
    "ListReportJobsOutputTypeDef",
    {
        "ReportJobs": List[ReportJobTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredBackupPlanInputTypeDef = TypedDict(
    "_RequiredBackupPlanInputTypeDef",
    {
        "BackupPlanName": str,
        "Rules": Sequence[BackupRuleInputTypeDef],
    },
)
_OptionalBackupPlanInputTypeDef = TypedDict(
    "_OptionalBackupPlanInputTypeDef",
    {
        "AdvancedBackupSettings": Sequence[AdvancedBackupSettingTypeDef],
    },
    total=False,
)

class BackupPlanInputTypeDef(_RequiredBackupPlanInputTypeDef, _OptionalBackupPlanInputTypeDef):
    pass

_RequiredBackupPlanTypeDef = TypedDict(
    "_RequiredBackupPlanTypeDef",
    {
        "BackupPlanName": str,
        "Rules": List[BackupRuleTypeDef],
    },
)
_OptionalBackupPlanTypeDef = TypedDict(
    "_OptionalBackupPlanTypeDef",
    {
        "AdvancedBackupSettings": List[AdvancedBackupSettingTypeDef],
    },
    total=False,
)

class BackupPlanTypeDef(_RequiredBackupPlanTypeDef, _OptionalBackupPlanTypeDef):
    pass

_RequiredCreateBackupSelectionInputRequestTypeDef = TypedDict(
    "_RequiredCreateBackupSelectionInputRequestTypeDef",
    {
        "BackupPlanId": str,
        "BackupSelection": BackupSelectionTypeDef,
    },
)
_OptionalCreateBackupSelectionInputRequestTypeDef = TypedDict(
    "_OptionalCreateBackupSelectionInputRequestTypeDef",
    {
        "CreatorRequestId": str,
    },
    total=False,
)

class CreateBackupSelectionInputRequestTypeDef(
    _RequiredCreateBackupSelectionInputRequestTypeDef,
    _OptionalCreateBackupSelectionInputRequestTypeDef,
):
    pass

GetBackupSelectionOutputTypeDef = TypedDict(
    "GetBackupSelectionOutputTypeDef",
    {
        "BackupSelection": BackupSelectionTypeDef,
        "SelectionId": str,
        "BackupPlanId": str,
        "CreationDate": datetime,
        "CreatorRequestId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateBackupPlanInputRequestTypeDef = TypedDict(
    "_RequiredCreateBackupPlanInputRequestTypeDef",
    {
        "BackupPlan": BackupPlanInputTypeDef,
    },
)
_OptionalCreateBackupPlanInputRequestTypeDef = TypedDict(
    "_OptionalCreateBackupPlanInputRequestTypeDef",
    {
        "BackupPlanTags": Mapping[str, str],
        "CreatorRequestId": str,
    },
    total=False,
)

class CreateBackupPlanInputRequestTypeDef(
    _RequiredCreateBackupPlanInputRequestTypeDef, _OptionalCreateBackupPlanInputRequestTypeDef
):
    pass

UpdateBackupPlanInputRequestTypeDef = TypedDict(
    "UpdateBackupPlanInputRequestTypeDef",
    {
        "BackupPlanId": str,
        "BackupPlan": BackupPlanInputTypeDef,
    },
)

GetBackupPlanFromJSONOutputTypeDef = TypedDict(
    "GetBackupPlanFromJSONOutputTypeDef",
    {
        "BackupPlan": BackupPlanTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetBackupPlanFromTemplateOutputTypeDef = TypedDict(
    "GetBackupPlanFromTemplateOutputTypeDef",
    {
        "BackupPlanDocument": BackupPlanTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetBackupPlanOutputTypeDef = TypedDict(
    "GetBackupPlanOutputTypeDef",
    {
        "BackupPlan": BackupPlanTypeDef,
        "BackupPlanId": str,
        "BackupPlanArn": str,
        "VersionId": str,
        "CreatorRequestId": str,
        "CreationDate": datetime,
        "DeletionDate": datetime,
        "LastExecutionDate": datetime,
        "AdvancedBackupSettings": List[AdvancedBackupSettingTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)
