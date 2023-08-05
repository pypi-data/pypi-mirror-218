"""
Type annotations for mgn service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/type_defs/)

Usage::

    ```python
    from mypy_boto3_mgn.type_defs import ApplicationAggregatedStatusTypeDef

    data: ApplicationAggregatedStatusTypeDef = {...}
    ```
"""
import sys
from typing import Dict, List, Mapping, Sequence

from .literals import (
    ActionCategoryType,
    ApplicationHealthStatusType,
    ApplicationProgressStatusType,
    BootModeType,
    ChangeServerLifeCycleStateSourceServerLifecycleStateType,
    DataReplicationErrorStringType,
    DataReplicationInitiationStepNameType,
    DataReplicationInitiationStepStatusType,
    DataReplicationStateType,
    ExportStatusType,
    FirstBootType,
    ImportErrorTypeType,
    ImportStatusType,
    InitiatedByType,
    JobLogEventType,
    JobStatusType,
    JobTypeType,
    LaunchDispositionType,
    LaunchStatusType,
    LifeCycleStateType,
    PostLaunchActionExecutionStatusType,
    PostLaunchActionsDeploymentTypeType,
    ReplicationConfigurationDataPlaneRoutingType,
    ReplicationConfigurationDefaultLargeStagingDiskTypeType,
    ReplicationConfigurationEbsEncryptionType,
    ReplicationConfigurationReplicatedDiskStagingDiskTypeType,
    ReplicationTypeType,
    SsmDocumentTypeType,
    TargetInstanceTypeRightSizingMethodType,
    VolumeTypeType,
    WaveHealthStatusType,
    WaveProgressStatusType,
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
    "ApplicationAggregatedStatusTypeDef",
    "ArchiveApplicationRequestRequestTypeDef",
    "ArchiveWaveRequestRequestTypeDef",
    "AssociateApplicationsRequestRequestTypeDef",
    "AssociateSourceServersRequestRequestTypeDef",
    "CPUTypeDef",
    "ChangeServerLifeCycleStateSourceServerLifecycleTypeDef",
    "CreateApplicationRequestRequestTypeDef",
    "LaunchTemplateDiskConfTypeDef",
    "LicensingTypeDef",
    "CreateReplicationConfigurationTemplateRequestRequestTypeDef",
    "CreateWaveRequestRequestTypeDef",
    "DataReplicationErrorTypeDef",
    "DataReplicationInfoReplicatedDiskTypeDef",
    "DataReplicationInitiationStepTypeDef",
    "DeleteApplicationRequestRequestTypeDef",
    "DeleteJobRequestRequestTypeDef",
    "DeleteLaunchConfigurationTemplateRequestRequestTypeDef",
    "DeleteReplicationConfigurationTemplateRequestRequestTypeDef",
    "DeleteSourceServerRequestRequestTypeDef",
    "DeleteVcenterClientRequestRequestTypeDef",
    "DeleteWaveRequestRequestTypeDef",
    "DescribeJobLogItemsRequestDescribeJobLogItemsPaginateTypeDef",
    "DescribeJobLogItemsRequestRequestTypeDef",
    "DescribeJobsRequestFiltersTypeDef",
    "DescribeLaunchConfigurationTemplatesRequestDescribeLaunchConfigurationTemplatesPaginateTypeDef",
    "DescribeLaunchConfigurationTemplatesRequestRequestTypeDef",
    "DescribeReplicationConfigurationTemplatesRequestDescribeReplicationConfigurationTemplatesPaginateTypeDef",
    "DescribeReplicationConfigurationTemplatesRequestRequestTypeDef",
    "ReplicationConfigurationTemplateTypeDef",
    "DescribeSourceServersRequestFiltersTypeDef",
    "DescribeVcenterClientsRequestDescribeVcenterClientsPaginateTypeDef",
    "DescribeVcenterClientsRequestRequestTypeDef",
    "VcenterClientTypeDef",
    "DisassociateApplicationsRequestRequestTypeDef",
    "DisassociateSourceServersRequestRequestTypeDef",
    "DisconnectFromServiceRequestRequestTypeDef",
    "DiskTypeDef",
    "EmptyResponseMetadataTypeDef",
    "ExportErrorDataTypeDef",
    "ExportTaskSummaryTypeDef",
    "FinalizeCutoverRequestRequestTypeDef",
    "GetLaunchConfigurationRequestRequestTypeDef",
    "GetReplicationConfigurationRequestRequestTypeDef",
    "IdentificationHintsTypeDef",
    "ImportErrorDataTypeDef",
    "ImportTaskSummaryApplicationsTypeDef",
    "ImportTaskSummaryServersTypeDef",
    "ImportTaskSummaryWavesTypeDef",
    "S3BucketSourceTypeDef",
    "JobLogEventDataTypeDef",
    "LaunchedInstanceTypeDef",
    "LifeCycleLastCutoverFinalizedTypeDef",
    "LifeCycleLastCutoverInitiatedTypeDef",
    "LifeCycleLastCutoverRevertedTypeDef",
    "LifeCycleLastTestFinalizedTypeDef",
    "LifeCycleLastTestInitiatedTypeDef",
    "LifeCycleLastTestRevertedTypeDef",
    "ListApplicationsRequestFiltersTypeDef",
    "ListExportErrorsRequestListExportErrorsPaginateTypeDef",
    "ListExportErrorsRequestRequestTypeDef",
    "ListExportsRequestFiltersTypeDef",
    "ListImportErrorsRequestListImportErrorsPaginateTypeDef",
    "ListImportErrorsRequestRequestTypeDef",
    "ListImportsRequestFiltersTypeDef",
    "ListManagedAccountsRequestListManagedAccountsPaginateTypeDef",
    "ListManagedAccountsRequestRequestTypeDef",
    "ManagedAccountTypeDef",
    "SourceServerActionsRequestFiltersTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "TemplateActionsRequestFiltersTypeDef",
    "ListWavesRequestFiltersTypeDef",
    "MarkAsArchivedRequestRequestTypeDef",
    "NetworkInterfaceTypeDef",
    "OSTypeDef",
    "PaginatorConfigTypeDef",
    "PauseReplicationRequestRequestTypeDef",
    "SsmExternalParameterTypeDef",
    "SsmParameterStoreParameterTypeDef",
    "RemoveSourceServerActionRequestRequestTypeDef",
    "RemoveTemplateActionRequestRequestTypeDef",
    "ReplicationConfigurationReplicatedDiskTypeDef",
    "ReplicationConfigurationTemplateResponseMetadataTypeDef",
    "ResponseMetadataTypeDef",
    "ResumeReplicationRequestRequestTypeDef",
    "RetryDataReplicationRequestRequestTypeDef",
    "StartCutoverRequestRequestTypeDef",
    "StartExportRequestRequestTypeDef",
    "StartReplicationRequestRequestTypeDef",
    "StartTestRequestRequestTypeDef",
    "StopReplicationRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TerminateTargetInstancesRequestRequestTypeDef",
    "UnarchiveApplicationRequestRequestTypeDef",
    "UnarchiveWaveRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateApplicationRequestRequestTypeDef",
    "UpdateReplicationConfigurationTemplateRequestRequestTypeDef",
    "UpdateSourceServerReplicationTypeRequestRequestTypeDef",
    "UpdateWaveRequestRequestTypeDef",
    "WaveAggregatedStatusTypeDef",
    "ApplicationResponseMetadataTypeDef",
    "ApplicationTypeDef",
    "ChangeServerLifeCycleStateRequestRequestTypeDef",
    "DataReplicationInitiationTypeDef",
    "DescribeJobsRequestDescribeJobsPaginateTypeDef",
    "DescribeJobsRequestRequestTypeDef",
    "DescribeReplicationConfigurationTemplatesResponseTypeDef",
    "DescribeSourceServersRequestDescribeSourceServersPaginateTypeDef",
    "DescribeSourceServersRequestRequestTypeDef",
    "DescribeVcenterClientsResponseTypeDef",
    "ExportTaskErrorTypeDef",
    "ExportTaskTypeDef",
    "ImportTaskErrorTypeDef",
    "ImportTaskSummaryTypeDef",
    "StartImportRequestRequestTypeDef",
    "JobLogTypeDef",
    "LifeCycleLastCutoverTypeDef",
    "LifeCycleLastTestTypeDef",
    "ListApplicationsRequestListApplicationsPaginateTypeDef",
    "ListApplicationsRequestRequestTypeDef",
    "ListExportsRequestListExportsPaginateTypeDef",
    "ListExportsRequestRequestTypeDef",
    "ListImportsRequestListImportsPaginateTypeDef",
    "ListImportsRequestRequestTypeDef",
    "ListManagedAccountsResponseTypeDef",
    "ListSourceServerActionsRequestListSourceServerActionsPaginateTypeDef",
    "ListSourceServerActionsRequestRequestTypeDef",
    "ListTemplateActionsRequestListTemplateActionsPaginateTypeDef",
    "ListTemplateActionsRequestRequestTypeDef",
    "ListWavesRequestListWavesPaginateTypeDef",
    "ListWavesRequestRequestTypeDef",
    "SourcePropertiesTypeDef",
    "PutSourceServerActionRequestRequestTypeDef",
    "PutTemplateActionRequestRequestTypeDef",
    "SourceServerActionDocumentResponseMetadataTypeDef",
    "SourceServerActionDocumentTypeDef",
    "SsmDocumentTypeDef",
    "TemplateActionDocumentResponseMetadataTypeDef",
    "TemplateActionDocumentTypeDef",
    "ReplicationConfigurationTypeDef",
    "UpdateReplicationConfigurationRequestRequestTypeDef",
    "WaveResponseMetadataTypeDef",
    "WaveTypeDef",
    "ListApplicationsResponseTypeDef",
    "DataReplicationInfoTypeDef",
    "ListExportErrorsResponseTypeDef",
    "ListExportsResponseTypeDef",
    "StartExportResponseTypeDef",
    "ListImportErrorsResponseTypeDef",
    "ImportTaskTypeDef",
    "DescribeJobLogItemsResponseTypeDef",
    "LifeCycleTypeDef",
    "ListSourceServerActionsResponseTypeDef",
    "JobPostLaunchActionsLaunchStatusTypeDef",
    "PostLaunchActionsTypeDef",
    "ListTemplateActionsResponseTypeDef",
    "ListWavesResponseTypeDef",
    "ListImportsResponseTypeDef",
    "StartImportResponseTypeDef",
    "SourceServerResponseMetadataTypeDef",
    "SourceServerTypeDef",
    "PostLaunchActionsStatusTypeDef",
    "CreateLaunchConfigurationTemplateRequestRequestTypeDef",
    "LaunchConfigurationTemplateResponseMetadataTypeDef",
    "LaunchConfigurationTemplateTypeDef",
    "LaunchConfigurationTypeDef",
    "UpdateLaunchConfigurationRequestRequestTypeDef",
    "UpdateLaunchConfigurationTemplateRequestRequestTypeDef",
    "DescribeSourceServersResponseTypeDef",
    "ParticipatingServerTypeDef",
    "DescribeLaunchConfigurationTemplatesResponseTypeDef",
    "JobTypeDef",
    "DescribeJobsResponseTypeDef",
    "StartCutoverResponseTypeDef",
    "StartTestResponseTypeDef",
    "TerminateTargetInstancesResponseTypeDef",
)

ApplicationAggregatedStatusTypeDef = TypedDict(
    "ApplicationAggregatedStatusTypeDef",
    {
        "healthStatus": ApplicationHealthStatusType,
        "lastUpdateDateTime": str,
        "progressStatus": ApplicationProgressStatusType,
        "totalSourceServers": int,
    },
    total=False,
)

_RequiredArchiveApplicationRequestRequestTypeDef = TypedDict(
    "_RequiredArchiveApplicationRequestRequestTypeDef",
    {
        "applicationID": str,
    },
)
_OptionalArchiveApplicationRequestRequestTypeDef = TypedDict(
    "_OptionalArchiveApplicationRequestRequestTypeDef",
    {
        "accountID": str,
    },
    total=False,
)


class ArchiveApplicationRequestRequestTypeDef(
    _RequiredArchiveApplicationRequestRequestTypeDef,
    _OptionalArchiveApplicationRequestRequestTypeDef,
):
    pass


_RequiredArchiveWaveRequestRequestTypeDef = TypedDict(
    "_RequiredArchiveWaveRequestRequestTypeDef",
    {
        "waveID": str,
    },
)
_OptionalArchiveWaveRequestRequestTypeDef = TypedDict(
    "_OptionalArchiveWaveRequestRequestTypeDef",
    {
        "accountID": str,
    },
    total=False,
)


class ArchiveWaveRequestRequestTypeDef(
    _RequiredArchiveWaveRequestRequestTypeDef, _OptionalArchiveWaveRequestRequestTypeDef
):
    pass


_RequiredAssociateApplicationsRequestRequestTypeDef = TypedDict(
    "_RequiredAssociateApplicationsRequestRequestTypeDef",
    {
        "applicationIDs": Sequence[str],
        "waveID": str,
    },
)
_OptionalAssociateApplicationsRequestRequestTypeDef = TypedDict(
    "_OptionalAssociateApplicationsRequestRequestTypeDef",
    {
        "accountID": str,
    },
    total=False,
)


class AssociateApplicationsRequestRequestTypeDef(
    _RequiredAssociateApplicationsRequestRequestTypeDef,
    _OptionalAssociateApplicationsRequestRequestTypeDef,
):
    pass


_RequiredAssociateSourceServersRequestRequestTypeDef = TypedDict(
    "_RequiredAssociateSourceServersRequestRequestTypeDef",
    {
        "applicationID": str,
        "sourceServerIDs": Sequence[str],
    },
)
_OptionalAssociateSourceServersRequestRequestTypeDef = TypedDict(
    "_OptionalAssociateSourceServersRequestRequestTypeDef",
    {
        "accountID": str,
    },
    total=False,
)


class AssociateSourceServersRequestRequestTypeDef(
    _RequiredAssociateSourceServersRequestRequestTypeDef,
    _OptionalAssociateSourceServersRequestRequestTypeDef,
):
    pass


CPUTypeDef = TypedDict(
    "CPUTypeDef",
    {
        "cores": int,
        "modelName": str,
    },
    total=False,
)

ChangeServerLifeCycleStateSourceServerLifecycleTypeDef = TypedDict(
    "ChangeServerLifeCycleStateSourceServerLifecycleTypeDef",
    {
        "state": ChangeServerLifeCycleStateSourceServerLifecycleStateType,
    },
)

_RequiredCreateApplicationRequestRequestTypeDef = TypedDict(
    "_RequiredCreateApplicationRequestRequestTypeDef",
    {
        "name": str,
    },
)
_OptionalCreateApplicationRequestRequestTypeDef = TypedDict(
    "_OptionalCreateApplicationRequestRequestTypeDef",
    {
        "accountID": str,
        "description": str,
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateApplicationRequestRequestTypeDef(
    _RequiredCreateApplicationRequestRequestTypeDef, _OptionalCreateApplicationRequestRequestTypeDef
):
    pass


LaunchTemplateDiskConfTypeDef = TypedDict(
    "LaunchTemplateDiskConfTypeDef",
    {
        "iops": int,
        "throughput": int,
        "volumeType": VolumeTypeType,
    },
    total=False,
)

LicensingTypeDef = TypedDict(
    "LicensingTypeDef",
    {
        "osByol": bool,
    },
    total=False,
)

_RequiredCreateReplicationConfigurationTemplateRequestRequestTypeDef = TypedDict(
    "_RequiredCreateReplicationConfigurationTemplateRequestRequestTypeDef",
    {
        "associateDefaultSecurityGroup": bool,
        "bandwidthThrottling": int,
        "createPublicIP": bool,
        "dataPlaneRouting": ReplicationConfigurationDataPlaneRoutingType,
        "defaultLargeStagingDiskType": ReplicationConfigurationDefaultLargeStagingDiskTypeType,
        "ebsEncryption": ReplicationConfigurationEbsEncryptionType,
        "replicationServerInstanceType": str,
        "replicationServersSecurityGroupsIDs": Sequence[str],
        "stagingAreaSubnetId": str,
        "stagingAreaTags": Mapping[str, str],
        "useDedicatedReplicationServer": bool,
    },
)
_OptionalCreateReplicationConfigurationTemplateRequestRequestTypeDef = TypedDict(
    "_OptionalCreateReplicationConfigurationTemplateRequestRequestTypeDef",
    {
        "ebsEncryptionKeyArn": str,
        "tags": Mapping[str, str],
        "useFipsEndpoint": bool,
    },
    total=False,
)


class CreateReplicationConfigurationTemplateRequestRequestTypeDef(
    _RequiredCreateReplicationConfigurationTemplateRequestRequestTypeDef,
    _OptionalCreateReplicationConfigurationTemplateRequestRequestTypeDef,
):
    pass


_RequiredCreateWaveRequestRequestTypeDef = TypedDict(
    "_RequiredCreateWaveRequestRequestTypeDef",
    {
        "name": str,
    },
)
_OptionalCreateWaveRequestRequestTypeDef = TypedDict(
    "_OptionalCreateWaveRequestRequestTypeDef",
    {
        "accountID": str,
        "description": str,
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateWaveRequestRequestTypeDef(
    _RequiredCreateWaveRequestRequestTypeDef, _OptionalCreateWaveRequestRequestTypeDef
):
    pass


DataReplicationErrorTypeDef = TypedDict(
    "DataReplicationErrorTypeDef",
    {
        "error": DataReplicationErrorStringType,
        "rawError": str,
    },
    total=False,
)

DataReplicationInfoReplicatedDiskTypeDef = TypedDict(
    "DataReplicationInfoReplicatedDiskTypeDef",
    {
        "backloggedStorageBytes": int,
        "deviceName": str,
        "replicatedStorageBytes": int,
        "rescannedStorageBytes": int,
        "totalStorageBytes": int,
    },
    total=False,
)

DataReplicationInitiationStepTypeDef = TypedDict(
    "DataReplicationInitiationStepTypeDef",
    {
        "name": DataReplicationInitiationStepNameType,
        "status": DataReplicationInitiationStepStatusType,
    },
    total=False,
)

_RequiredDeleteApplicationRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteApplicationRequestRequestTypeDef",
    {
        "applicationID": str,
    },
)
_OptionalDeleteApplicationRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteApplicationRequestRequestTypeDef",
    {
        "accountID": str,
    },
    total=False,
)


class DeleteApplicationRequestRequestTypeDef(
    _RequiredDeleteApplicationRequestRequestTypeDef, _OptionalDeleteApplicationRequestRequestTypeDef
):
    pass


_RequiredDeleteJobRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteJobRequestRequestTypeDef",
    {
        "jobID": str,
    },
)
_OptionalDeleteJobRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteJobRequestRequestTypeDef",
    {
        "accountID": str,
    },
    total=False,
)


class DeleteJobRequestRequestTypeDef(
    _RequiredDeleteJobRequestRequestTypeDef, _OptionalDeleteJobRequestRequestTypeDef
):
    pass


DeleteLaunchConfigurationTemplateRequestRequestTypeDef = TypedDict(
    "DeleteLaunchConfigurationTemplateRequestRequestTypeDef",
    {
        "launchConfigurationTemplateID": str,
    },
)

DeleteReplicationConfigurationTemplateRequestRequestTypeDef = TypedDict(
    "DeleteReplicationConfigurationTemplateRequestRequestTypeDef",
    {
        "replicationConfigurationTemplateID": str,
    },
)

_RequiredDeleteSourceServerRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteSourceServerRequestRequestTypeDef",
    {
        "sourceServerID": str,
    },
)
_OptionalDeleteSourceServerRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteSourceServerRequestRequestTypeDef",
    {
        "accountID": str,
    },
    total=False,
)


class DeleteSourceServerRequestRequestTypeDef(
    _RequiredDeleteSourceServerRequestRequestTypeDef,
    _OptionalDeleteSourceServerRequestRequestTypeDef,
):
    pass


DeleteVcenterClientRequestRequestTypeDef = TypedDict(
    "DeleteVcenterClientRequestRequestTypeDef",
    {
        "vcenterClientID": str,
    },
)

_RequiredDeleteWaveRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteWaveRequestRequestTypeDef",
    {
        "waveID": str,
    },
)
_OptionalDeleteWaveRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteWaveRequestRequestTypeDef",
    {
        "accountID": str,
    },
    total=False,
)


class DeleteWaveRequestRequestTypeDef(
    _RequiredDeleteWaveRequestRequestTypeDef, _OptionalDeleteWaveRequestRequestTypeDef
):
    pass


_RequiredDescribeJobLogItemsRequestDescribeJobLogItemsPaginateTypeDef = TypedDict(
    "_RequiredDescribeJobLogItemsRequestDescribeJobLogItemsPaginateTypeDef",
    {
        "jobID": str,
    },
)
_OptionalDescribeJobLogItemsRequestDescribeJobLogItemsPaginateTypeDef = TypedDict(
    "_OptionalDescribeJobLogItemsRequestDescribeJobLogItemsPaginateTypeDef",
    {
        "accountID": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class DescribeJobLogItemsRequestDescribeJobLogItemsPaginateTypeDef(
    _RequiredDescribeJobLogItemsRequestDescribeJobLogItemsPaginateTypeDef,
    _OptionalDescribeJobLogItemsRequestDescribeJobLogItemsPaginateTypeDef,
):
    pass


_RequiredDescribeJobLogItemsRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeJobLogItemsRequestRequestTypeDef",
    {
        "jobID": str,
    },
)
_OptionalDescribeJobLogItemsRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeJobLogItemsRequestRequestTypeDef",
    {
        "accountID": str,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)


class DescribeJobLogItemsRequestRequestTypeDef(
    _RequiredDescribeJobLogItemsRequestRequestTypeDef,
    _OptionalDescribeJobLogItemsRequestRequestTypeDef,
):
    pass


DescribeJobsRequestFiltersTypeDef = TypedDict(
    "DescribeJobsRequestFiltersTypeDef",
    {
        "fromDate": str,
        "jobIDs": Sequence[str],
        "toDate": str,
    },
    total=False,
)

DescribeLaunchConfigurationTemplatesRequestDescribeLaunchConfigurationTemplatesPaginateTypeDef = TypedDict(
    "DescribeLaunchConfigurationTemplatesRequestDescribeLaunchConfigurationTemplatesPaginateTypeDef",
    {
        "launchConfigurationTemplateIDs": Sequence[str],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

DescribeLaunchConfigurationTemplatesRequestRequestTypeDef = TypedDict(
    "DescribeLaunchConfigurationTemplatesRequestRequestTypeDef",
    {
        "launchConfigurationTemplateIDs": Sequence[str],
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

DescribeReplicationConfigurationTemplatesRequestDescribeReplicationConfigurationTemplatesPaginateTypeDef = TypedDict(
    "DescribeReplicationConfigurationTemplatesRequestDescribeReplicationConfigurationTemplatesPaginateTypeDef",
    {
        "replicationConfigurationTemplateIDs": Sequence[str],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

DescribeReplicationConfigurationTemplatesRequestRequestTypeDef = TypedDict(
    "DescribeReplicationConfigurationTemplatesRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
        "replicationConfigurationTemplateIDs": Sequence[str],
    },
    total=False,
)

_RequiredReplicationConfigurationTemplateTypeDef = TypedDict(
    "_RequiredReplicationConfigurationTemplateTypeDef",
    {
        "replicationConfigurationTemplateID": str,
    },
)
_OptionalReplicationConfigurationTemplateTypeDef = TypedDict(
    "_OptionalReplicationConfigurationTemplateTypeDef",
    {
        "arn": str,
        "associateDefaultSecurityGroup": bool,
        "bandwidthThrottling": int,
        "createPublicIP": bool,
        "dataPlaneRouting": ReplicationConfigurationDataPlaneRoutingType,
        "defaultLargeStagingDiskType": ReplicationConfigurationDefaultLargeStagingDiskTypeType,
        "ebsEncryption": ReplicationConfigurationEbsEncryptionType,
        "ebsEncryptionKeyArn": str,
        "replicationServerInstanceType": str,
        "replicationServersSecurityGroupsIDs": List[str],
        "stagingAreaSubnetId": str,
        "stagingAreaTags": Dict[str, str],
        "tags": Dict[str, str],
        "useDedicatedReplicationServer": bool,
        "useFipsEndpoint": bool,
    },
    total=False,
)


class ReplicationConfigurationTemplateTypeDef(
    _RequiredReplicationConfigurationTemplateTypeDef,
    _OptionalReplicationConfigurationTemplateTypeDef,
):
    pass


DescribeSourceServersRequestFiltersTypeDef = TypedDict(
    "DescribeSourceServersRequestFiltersTypeDef",
    {
        "applicationIDs": Sequence[str],
        "isArchived": bool,
        "lifeCycleStates": Sequence[LifeCycleStateType],
        "replicationTypes": Sequence[ReplicationTypeType],
        "sourceServerIDs": Sequence[str],
    },
    total=False,
)

DescribeVcenterClientsRequestDescribeVcenterClientsPaginateTypeDef = TypedDict(
    "DescribeVcenterClientsRequestDescribeVcenterClientsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

DescribeVcenterClientsRequestRequestTypeDef = TypedDict(
    "DescribeVcenterClientsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

VcenterClientTypeDef = TypedDict(
    "VcenterClientTypeDef",
    {
        "arn": str,
        "datacenterName": str,
        "hostname": str,
        "lastSeenDatetime": str,
        "sourceServerTags": Dict[str, str],
        "tags": Dict[str, str],
        "vcenterClientID": str,
        "vcenterUUID": str,
    },
    total=False,
)

_RequiredDisassociateApplicationsRequestRequestTypeDef = TypedDict(
    "_RequiredDisassociateApplicationsRequestRequestTypeDef",
    {
        "applicationIDs": Sequence[str],
        "waveID": str,
    },
)
_OptionalDisassociateApplicationsRequestRequestTypeDef = TypedDict(
    "_OptionalDisassociateApplicationsRequestRequestTypeDef",
    {
        "accountID": str,
    },
    total=False,
)


class DisassociateApplicationsRequestRequestTypeDef(
    _RequiredDisassociateApplicationsRequestRequestTypeDef,
    _OptionalDisassociateApplicationsRequestRequestTypeDef,
):
    pass


_RequiredDisassociateSourceServersRequestRequestTypeDef = TypedDict(
    "_RequiredDisassociateSourceServersRequestRequestTypeDef",
    {
        "applicationID": str,
        "sourceServerIDs": Sequence[str],
    },
)
_OptionalDisassociateSourceServersRequestRequestTypeDef = TypedDict(
    "_OptionalDisassociateSourceServersRequestRequestTypeDef",
    {
        "accountID": str,
    },
    total=False,
)


class DisassociateSourceServersRequestRequestTypeDef(
    _RequiredDisassociateSourceServersRequestRequestTypeDef,
    _OptionalDisassociateSourceServersRequestRequestTypeDef,
):
    pass


_RequiredDisconnectFromServiceRequestRequestTypeDef = TypedDict(
    "_RequiredDisconnectFromServiceRequestRequestTypeDef",
    {
        "sourceServerID": str,
    },
)
_OptionalDisconnectFromServiceRequestRequestTypeDef = TypedDict(
    "_OptionalDisconnectFromServiceRequestRequestTypeDef",
    {
        "accountID": str,
    },
    total=False,
)


class DisconnectFromServiceRequestRequestTypeDef(
    _RequiredDisconnectFromServiceRequestRequestTypeDef,
    _OptionalDisconnectFromServiceRequestRequestTypeDef,
):
    pass


DiskTypeDef = TypedDict(
    "DiskTypeDef",
    {
        "bytes": int,
        "deviceName": str,
    },
    total=False,
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ExportErrorDataTypeDef = TypedDict(
    "ExportErrorDataTypeDef",
    {
        "rawError": str,
    },
    total=False,
)

ExportTaskSummaryTypeDef = TypedDict(
    "ExportTaskSummaryTypeDef",
    {
        "applicationsCount": int,
        "serversCount": int,
        "wavesCount": int,
    },
    total=False,
)

_RequiredFinalizeCutoverRequestRequestTypeDef = TypedDict(
    "_RequiredFinalizeCutoverRequestRequestTypeDef",
    {
        "sourceServerID": str,
    },
)
_OptionalFinalizeCutoverRequestRequestTypeDef = TypedDict(
    "_OptionalFinalizeCutoverRequestRequestTypeDef",
    {
        "accountID": str,
    },
    total=False,
)


class FinalizeCutoverRequestRequestTypeDef(
    _RequiredFinalizeCutoverRequestRequestTypeDef, _OptionalFinalizeCutoverRequestRequestTypeDef
):
    pass


_RequiredGetLaunchConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredGetLaunchConfigurationRequestRequestTypeDef",
    {
        "sourceServerID": str,
    },
)
_OptionalGetLaunchConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalGetLaunchConfigurationRequestRequestTypeDef",
    {
        "accountID": str,
    },
    total=False,
)


class GetLaunchConfigurationRequestRequestTypeDef(
    _RequiredGetLaunchConfigurationRequestRequestTypeDef,
    _OptionalGetLaunchConfigurationRequestRequestTypeDef,
):
    pass


_RequiredGetReplicationConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredGetReplicationConfigurationRequestRequestTypeDef",
    {
        "sourceServerID": str,
    },
)
_OptionalGetReplicationConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalGetReplicationConfigurationRequestRequestTypeDef",
    {
        "accountID": str,
    },
    total=False,
)


class GetReplicationConfigurationRequestRequestTypeDef(
    _RequiredGetReplicationConfigurationRequestRequestTypeDef,
    _OptionalGetReplicationConfigurationRequestRequestTypeDef,
):
    pass


IdentificationHintsTypeDef = TypedDict(
    "IdentificationHintsTypeDef",
    {
        "awsInstanceID": str,
        "fqdn": str,
        "hostname": str,
        "vmPath": str,
        "vmWareUuid": str,
    },
    total=False,
)

ImportErrorDataTypeDef = TypedDict(
    "ImportErrorDataTypeDef",
    {
        "accountID": str,
        "applicationID": str,
        "ec2LaunchTemplateID": str,
        "rawError": str,
        "rowNumber": int,
        "sourceServerID": str,
        "waveID": str,
    },
    total=False,
)

ImportTaskSummaryApplicationsTypeDef = TypedDict(
    "ImportTaskSummaryApplicationsTypeDef",
    {
        "createdCount": int,
        "modifiedCount": int,
    },
    total=False,
)

ImportTaskSummaryServersTypeDef = TypedDict(
    "ImportTaskSummaryServersTypeDef",
    {
        "createdCount": int,
        "modifiedCount": int,
    },
    total=False,
)

ImportTaskSummaryWavesTypeDef = TypedDict(
    "ImportTaskSummaryWavesTypeDef",
    {
        "createdCount": int,
        "modifiedCount": int,
    },
    total=False,
)

_RequiredS3BucketSourceTypeDef = TypedDict(
    "_RequiredS3BucketSourceTypeDef",
    {
        "s3Bucket": str,
        "s3Key": str,
    },
)
_OptionalS3BucketSourceTypeDef = TypedDict(
    "_OptionalS3BucketSourceTypeDef",
    {
        "s3BucketOwner": str,
    },
    total=False,
)


class S3BucketSourceTypeDef(_RequiredS3BucketSourceTypeDef, _OptionalS3BucketSourceTypeDef):
    pass


JobLogEventDataTypeDef = TypedDict(
    "JobLogEventDataTypeDef",
    {
        "conversionServerID": str,
        "rawError": str,
        "sourceServerID": str,
        "targetInstanceID": str,
    },
    total=False,
)

LaunchedInstanceTypeDef = TypedDict(
    "LaunchedInstanceTypeDef",
    {
        "ec2InstanceID": str,
        "firstBoot": FirstBootType,
        "jobID": str,
    },
    total=False,
)

LifeCycleLastCutoverFinalizedTypeDef = TypedDict(
    "LifeCycleLastCutoverFinalizedTypeDef",
    {
        "apiCallDateTime": str,
    },
    total=False,
)

LifeCycleLastCutoverInitiatedTypeDef = TypedDict(
    "LifeCycleLastCutoverInitiatedTypeDef",
    {
        "apiCallDateTime": str,
        "jobID": str,
    },
    total=False,
)

LifeCycleLastCutoverRevertedTypeDef = TypedDict(
    "LifeCycleLastCutoverRevertedTypeDef",
    {
        "apiCallDateTime": str,
    },
    total=False,
)

LifeCycleLastTestFinalizedTypeDef = TypedDict(
    "LifeCycleLastTestFinalizedTypeDef",
    {
        "apiCallDateTime": str,
    },
    total=False,
)

LifeCycleLastTestInitiatedTypeDef = TypedDict(
    "LifeCycleLastTestInitiatedTypeDef",
    {
        "apiCallDateTime": str,
        "jobID": str,
    },
    total=False,
)

LifeCycleLastTestRevertedTypeDef = TypedDict(
    "LifeCycleLastTestRevertedTypeDef",
    {
        "apiCallDateTime": str,
    },
    total=False,
)

ListApplicationsRequestFiltersTypeDef = TypedDict(
    "ListApplicationsRequestFiltersTypeDef",
    {
        "applicationIDs": Sequence[str],
        "isArchived": bool,
        "waveIDs": Sequence[str],
    },
    total=False,
)

_RequiredListExportErrorsRequestListExportErrorsPaginateTypeDef = TypedDict(
    "_RequiredListExportErrorsRequestListExportErrorsPaginateTypeDef",
    {
        "exportID": str,
    },
)
_OptionalListExportErrorsRequestListExportErrorsPaginateTypeDef = TypedDict(
    "_OptionalListExportErrorsRequestListExportErrorsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListExportErrorsRequestListExportErrorsPaginateTypeDef(
    _RequiredListExportErrorsRequestListExportErrorsPaginateTypeDef,
    _OptionalListExportErrorsRequestListExportErrorsPaginateTypeDef,
):
    pass


_RequiredListExportErrorsRequestRequestTypeDef = TypedDict(
    "_RequiredListExportErrorsRequestRequestTypeDef",
    {
        "exportID": str,
    },
)
_OptionalListExportErrorsRequestRequestTypeDef = TypedDict(
    "_OptionalListExportErrorsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)


class ListExportErrorsRequestRequestTypeDef(
    _RequiredListExportErrorsRequestRequestTypeDef, _OptionalListExportErrorsRequestRequestTypeDef
):
    pass


ListExportsRequestFiltersTypeDef = TypedDict(
    "ListExportsRequestFiltersTypeDef",
    {
        "exportIDs": Sequence[str],
    },
    total=False,
)

_RequiredListImportErrorsRequestListImportErrorsPaginateTypeDef = TypedDict(
    "_RequiredListImportErrorsRequestListImportErrorsPaginateTypeDef",
    {
        "importID": str,
    },
)
_OptionalListImportErrorsRequestListImportErrorsPaginateTypeDef = TypedDict(
    "_OptionalListImportErrorsRequestListImportErrorsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListImportErrorsRequestListImportErrorsPaginateTypeDef(
    _RequiredListImportErrorsRequestListImportErrorsPaginateTypeDef,
    _OptionalListImportErrorsRequestListImportErrorsPaginateTypeDef,
):
    pass


_RequiredListImportErrorsRequestRequestTypeDef = TypedDict(
    "_RequiredListImportErrorsRequestRequestTypeDef",
    {
        "importID": str,
    },
)
_OptionalListImportErrorsRequestRequestTypeDef = TypedDict(
    "_OptionalListImportErrorsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)


class ListImportErrorsRequestRequestTypeDef(
    _RequiredListImportErrorsRequestRequestTypeDef, _OptionalListImportErrorsRequestRequestTypeDef
):
    pass


ListImportsRequestFiltersTypeDef = TypedDict(
    "ListImportsRequestFiltersTypeDef",
    {
        "importIDs": Sequence[str],
    },
    total=False,
)

ListManagedAccountsRequestListManagedAccountsPaginateTypeDef = TypedDict(
    "ListManagedAccountsRequestListManagedAccountsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListManagedAccountsRequestRequestTypeDef = TypedDict(
    "ListManagedAccountsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ManagedAccountTypeDef = TypedDict(
    "ManagedAccountTypeDef",
    {
        "accountId": str,
    },
    total=False,
)

SourceServerActionsRequestFiltersTypeDef = TypedDict(
    "SourceServerActionsRequestFiltersTypeDef",
    {
        "actionIDs": Sequence[str],
    },
    total=False,
)

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

TemplateActionsRequestFiltersTypeDef = TypedDict(
    "TemplateActionsRequestFiltersTypeDef",
    {
        "actionIDs": Sequence[str],
    },
    total=False,
)

ListWavesRequestFiltersTypeDef = TypedDict(
    "ListWavesRequestFiltersTypeDef",
    {
        "isArchived": bool,
        "waveIDs": Sequence[str],
    },
    total=False,
)

_RequiredMarkAsArchivedRequestRequestTypeDef = TypedDict(
    "_RequiredMarkAsArchivedRequestRequestTypeDef",
    {
        "sourceServerID": str,
    },
)
_OptionalMarkAsArchivedRequestRequestTypeDef = TypedDict(
    "_OptionalMarkAsArchivedRequestRequestTypeDef",
    {
        "accountID": str,
    },
    total=False,
)


class MarkAsArchivedRequestRequestTypeDef(
    _RequiredMarkAsArchivedRequestRequestTypeDef, _OptionalMarkAsArchivedRequestRequestTypeDef
):
    pass


NetworkInterfaceTypeDef = TypedDict(
    "NetworkInterfaceTypeDef",
    {
        "ips": List[str],
        "isPrimary": bool,
        "macAddress": str,
    },
    total=False,
)

OSTypeDef = TypedDict(
    "OSTypeDef",
    {
        "fullString": str,
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

_RequiredPauseReplicationRequestRequestTypeDef = TypedDict(
    "_RequiredPauseReplicationRequestRequestTypeDef",
    {
        "sourceServerID": str,
    },
)
_OptionalPauseReplicationRequestRequestTypeDef = TypedDict(
    "_OptionalPauseReplicationRequestRequestTypeDef",
    {
        "accountID": str,
    },
    total=False,
)


class PauseReplicationRequestRequestTypeDef(
    _RequiredPauseReplicationRequestRequestTypeDef, _OptionalPauseReplicationRequestRequestTypeDef
):
    pass


SsmExternalParameterTypeDef = TypedDict(
    "SsmExternalParameterTypeDef",
    {
        "dynamicPath": str,
    },
    total=False,
)

SsmParameterStoreParameterTypeDef = TypedDict(
    "SsmParameterStoreParameterTypeDef",
    {
        "parameterName": str,
        "parameterType": Literal["STRING"],
    },
)

_RequiredRemoveSourceServerActionRequestRequestTypeDef = TypedDict(
    "_RequiredRemoveSourceServerActionRequestRequestTypeDef",
    {
        "actionID": str,
        "sourceServerID": str,
    },
)
_OptionalRemoveSourceServerActionRequestRequestTypeDef = TypedDict(
    "_OptionalRemoveSourceServerActionRequestRequestTypeDef",
    {
        "accountID": str,
    },
    total=False,
)


class RemoveSourceServerActionRequestRequestTypeDef(
    _RequiredRemoveSourceServerActionRequestRequestTypeDef,
    _OptionalRemoveSourceServerActionRequestRequestTypeDef,
):
    pass


RemoveTemplateActionRequestRequestTypeDef = TypedDict(
    "RemoveTemplateActionRequestRequestTypeDef",
    {
        "actionID": str,
        "launchConfigurationTemplateID": str,
    },
)

ReplicationConfigurationReplicatedDiskTypeDef = TypedDict(
    "ReplicationConfigurationReplicatedDiskTypeDef",
    {
        "deviceName": str,
        "iops": int,
        "isBootDisk": bool,
        "stagingDiskType": ReplicationConfigurationReplicatedDiskStagingDiskTypeType,
        "throughput": int,
    },
    total=False,
)

ReplicationConfigurationTemplateResponseMetadataTypeDef = TypedDict(
    "ReplicationConfigurationTemplateResponseMetadataTypeDef",
    {
        "arn": str,
        "associateDefaultSecurityGroup": bool,
        "bandwidthThrottling": int,
        "createPublicIP": bool,
        "dataPlaneRouting": ReplicationConfigurationDataPlaneRoutingType,
        "defaultLargeStagingDiskType": ReplicationConfigurationDefaultLargeStagingDiskTypeType,
        "ebsEncryption": ReplicationConfigurationEbsEncryptionType,
        "ebsEncryptionKeyArn": str,
        "replicationConfigurationTemplateID": str,
        "replicationServerInstanceType": str,
        "replicationServersSecurityGroupsIDs": List[str],
        "stagingAreaSubnetId": str,
        "stagingAreaTags": Dict[str, str],
        "tags": Dict[str, str],
        "useDedicatedReplicationServer": bool,
        "useFipsEndpoint": bool,
        "ResponseMetadata": "ResponseMetadataTypeDef",
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

_RequiredResumeReplicationRequestRequestTypeDef = TypedDict(
    "_RequiredResumeReplicationRequestRequestTypeDef",
    {
        "sourceServerID": str,
    },
)
_OptionalResumeReplicationRequestRequestTypeDef = TypedDict(
    "_OptionalResumeReplicationRequestRequestTypeDef",
    {
        "accountID": str,
    },
    total=False,
)


class ResumeReplicationRequestRequestTypeDef(
    _RequiredResumeReplicationRequestRequestTypeDef, _OptionalResumeReplicationRequestRequestTypeDef
):
    pass


_RequiredRetryDataReplicationRequestRequestTypeDef = TypedDict(
    "_RequiredRetryDataReplicationRequestRequestTypeDef",
    {
        "sourceServerID": str,
    },
)
_OptionalRetryDataReplicationRequestRequestTypeDef = TypedDict(
    "_OptionalRetryDataReplicationRequestRequestTypeDef",
    {
        "accountID": str,
    },
    total=False,
)


class RetryDataReplicationRequestRequestTypeDef(
    _RequiredRetryDataReplicationRequestRequestTypeDef,
    _OptionalRetryDataReplicationRequestRequestTypeDef,
):
    pass


_RequiredStartCutoverRequestRequestTypeDef = TypedDict(
    "_RequiredStartCutoverRequestRequestTypeDef",
    {
        "sourceServerIDs": Sequence[str],
    },
)
_OptionalStartCutoverRequestRequestTypeDef = TypedDict(
    "_OptionalStartCutoverRequestRequestTypeDef",
    {
        "accountID": str,
        "tags": Mapping[str, str],
    },
    total=False,
)


class StartCutoverRequestRequestTypeDef(
    _RequiredStartCutoverRequestRequestTypeDef, _OptionalStartCutoverRequestRequestTypeDef
):
    pass


_RequiredStartExportRequestRequestTypeDef = TypedDict(
    "_RequiredStartExportRequestRequestTypeDef",
    {
        "s3Bucket": str,
        "s3Key": str,
    },
)
_OptionalStartExportRequestRequestTypeDef = TypedDict(
    "_OptionalStartExportRequestRequestTypeDef",
    {
        "s3BucketOwner": str,
    },
    total=False,
)


class StartExportRequestRequestTypeDef(
    _RequiredStartExportRequestRequestTypeDef, _OptionalStartExportRequestRequestTypeDef
):
    pass


_RequiredStartReplicationRequestRequestTypeDef = TypedDict(
    "_RequiredStartReplicationRequestRequestTypeDef",
    {
        "sourceServerID": str,
    },
)
_OptionalStartReplicationRequestRequestTypeDef = TypedDict(
    "_OptionalStartReplicationRequestRequestTypeDef",
    {
        "accountID": str,
    },
    total=False,
)


class StartReplicationRequestRequestTypeDef(
    _RequiredStartReplicationRequestRequestTypeDef, _OptionalStartReplicationRequestRequestTypeDef
):
    pass


_RequiredStartTestRequestRequestTypeDef = TypedDict(
    "_RequiredStartTestRequestRequestTypeDef",
    {
        "sourceServerIDs": Sequence[str],
    },
)
_OptionalStartTestRequestRequestTypeDef = TypedDict(
    "_OptionalStartTestRequestRequestTypeDef",
    {
        "accountID": str,
        "tags": Mapping[str, str],
    },
    total=False,
)


class StartTestRequestRequestTypeDef(
    _RequiredStartTestRequestRequestTypeDef, _OptionalStartTestRequestRequestTypeDef
):
    pass


_RequiredStopReplicationRequestRequestTypeDef = TypedDict(
    "_RequiredStopReplicationRequestRequestTypeDef",
    {
        "sourceServerID": str,
    },
)
_OptionalStopReplicationRequestRequestTypeDef = TypedDict(
    "_OptionalStopReplicationRequestRequestTypeDef",
    {
        "accountID": str,
    },
    total=False,
)


class StopReplicationRequestRequestTypeDef(
    _RequiredStopReplicationRequestRequestTypeDef, _OptionalStopReplicationRequestRequestTypeDef
):
    pass


TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Mapping[str, str],
    },
)

_RequiredTerminateTargetInstancesRequestRequestTypeDef = TypedDict(
    "_RequiredTerminateTargetInstancesRequestRequestTypeDef",
    {
        "sourceServerIDs": Sequence[str],
    },
)
_OptionalTerminateTargetInstancesRequestRequestTypeDef = TypedDict(
    "_OptionalTerminateTargetInstancesRequestRequestTypeDef",
    {
        "accountID": str,
        "tags": Mapping[str, str],
    },
    total=False,
)


class TerminateTargetInstancesRequestRequestTypeDef(
    _RequiredTerminateTargetInstancesRequestRequestTypeDef,
    _OptionalTerminateTargetInstancesRequestRequestTypeDef,
):
    pass


_RequiredUnarchiveApplicationRequestRequestTypeDef = TypedDict(
    "_RequiredUnarchiveApplicationRequestRequestTypeDef",
    {
        "applicationID": str,
    },
)
_OptionalUnarchiveApplicationRequestRequestTypeDef = TypedDict(
    "_OptionalUnarchiveApplicationRequestRequestTypeDef",
    {
        "accountID": str,
    },
    total=False,
)


class UnarchiveApplicationRequestRequestTypeDef(
    _RequiredUnarchiveApplicationRequestRequestTypeDef,
    _OptionalUnarchiveApplicationRequestRequestTypeDef,
):
    pass


_RequiredUnarchiveWaveRequestRequestTypeDef = TypedDict(
    "_RequiredUnarchiveWaveRequestRequestTypeDef",
    {
        "waveID": str,
    },
)
_OptionalUnarchiveWaveRequestRequestTypeDef = TypedDict(
    "_OptionalUnarchiveWaveRequestRequestTypeDef",
    {
        "accountID": str,
    },
    total=False,
)


class UnarchiveWaveRequestRequestTypeDef(
    _RequiredUnarchiveWaveRequestRequestTypeDef, _OptionalUnarchiveWaveRequestRequestTypeDef
):
    pass


UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)

_RequiredUpdateApplicationRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateApplicationRequestRequestTypeDef",
    {
        "applicationID": str,
    },
)
_OptionalUpdateApplicationRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateApplicationRequestRequestTypeDef",
    {
        "accountID": str,
        "description": str,
        "name": str,
    },
    total=False,
)


class UpdateApplicationRequestRequestTypeDef(
    _RequiredUpdateApplicationRequestRequestTypeDef, _OptionalUpdateApplicationRequestRequestTypeDef
):
    pass


_RequiredUpdateReplicationConfigurationTemplateRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateReplicationConfigurationTemplateRequestRequestTypeDef",
    {
        "replicationConfigurationTemplateID": str,
    },
)
_OptionalUpdateReplicationConfigurationTemplateRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateReplicationConfigurationTemplateRequestRequestTypeDef",
    {
        "arn": str,
        "associateDefaultSecurityGroup": bool,
        "bandwidthThrottling": int,
        "createPublicIP": bool,
        "dataPlaneRouting": ReplicationConfigurationDataPlaneRoutingType,
        "defaultLargeStagingDiskType": ReplicationConfigurationDefaultLargeStagingDiskTypeType,
        "ebsEncryption": ReplicationConfigurationEbsEncryptionType,
        "ebsEncryptionKeyArn": str,
        "replicationServerInstanceType": str,
        "replicationServersSecurityGroupsIDs": Sequence[str],
        "stagingAreaSubnetId": str,
        "stagingAreaTags": Mapping[str, str],
        "useDedicatedReplicationServer": bool,
        "useFipsEndpoint": bool,
    },
    total=False,
)


class UpdateReplicationConfigurationTemplateRequestRequestTypeDef(
    _RequiredUpdateReplicationConfigurationTemplateRequestRequestTypeDef,
    _OptionalUpdateReplicationConfigurationTemplateRequestRequestTypeDef,
):
    pass


_RequiredUpdateSourceServerReplicationTypeRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateSourceServerReplicationTypeRequestRequestTypeDef",
    {
        "replicationType": ReplicationTypeType,
        "sourceServerID": str,
    },
)
_OptionalUpdateSourceServerReplicationTypeRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateSourceServerReplicationTypeRequestRequestTypeDef",
    {
        "accountID": str,
    },
    total=False,
)


class UpdateSourceServerReplicationTypeRequestRequestTypeDef(
    _RequiredUpdateSourceServerReplicationTypeRequestRequestTypeDef,
    _OptionalUpdateSourceServerReplicationTypeRequestRequestTypeDef,
):
    pass


_RequiredUpdateWaveRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateWaveRequestRequestTypeDef",
    {
        "waveID": str,
    },
)
_OptionalUpdateWaveRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateWaveRequestRequestTypeDef",
    {
        "accountID": str,
        "description": str,
        "name": str,
    },
    total=False,
)


class UpdateWaveRequestRequestTypeDef(
    _RequiredUpdateWaveRequestRequestTypeDef, _OptionalUpdateWaveRequestRequestTypeDef
):
    pass


WaveAggregatedStatusTypeDef = TypedDict(
    "WaveAggregatedStatusTypeDef",
    {
        "healthStatus": WaveHealthStatusType,
        "lastUpdateDateTime": str,
        "progressStatus": WaveProgressStatusType,
        "replicationStartedDateTime": str,
        "totalApplications": int,
    },
    total=False,
)

ApplicationResponseMetadataTypeDef = TypedDict(
    "ApplicationResponseMetadataTypeDef",
    {
        "applicationAggregatedStatus": ApplicationAggregatedStatusTypeDef,
        "applicationID": str,
        "arn": str,
        "creationDateTime": str,
        "description": str,
        "isArchived": bool,
        "lastModifiedDateTime": str,
        "name": str,
        "tags": Dict[str, str],
        "waveID": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ApplicationTypeDef = TypedDict(
    "ApplicationTypeDef",
    {
        "applicationAggregatedStatus": ApplicationAggregatedStatusTypeDef,
        "applicationID": str,
        "arn": str,
        "creationDateTime": str,
        "description": str,
        "isArchived": bool,
        "lastModifiedDateTime": str,
        "name": str,
        "tags": Dict[str, str],
        "waveID": str,
    },
    total=False,
)

_RequiredChangeServerLifeCycleStateRequestRequestTypeDef = TypedDict(
    "_RequiredChangeServerLifeCycleStateRequestRequestTypeDef",
    {
        "lifeCycle": ChangeServerLifeCycleStateSourceServerLifecycleTypeDef,
        "sourceServerID": str,
    },
)
_OptionalChangeServerLifeCycleStateRequestRequestTypeDef = TypedDict(
    "_OptionalChangeServerLifeCycleStateRequestRequestTypeDef",
    {
        "accountID": str,
    },
    total=False,
)


class ChangeServerLifeCycleStateRequestRequestTypeDef(
    _RequiredChangeServerLifeCycleStateRequestRequestTypeDef,
    _OptionalChangeServerLifeCycleStateRequestRequestTypeDef,
):
    pass


DataReplicationInitiationTypeDef = TypedDict(
    "DataReplicationInitiationTypeDef",
    {
        "nextAttemptDateTime": str,
        "startDateTime": str,
        "steps": List[DataReplicationInitiationStepTypeDef],
    },
    total=False,
)

DescribeJobsRequestDescribeJobsPaginateTypeDef = TypedDict(
    "DescribeJobsRequestDescribeJobsPaginateTypeDef",
    {
        "accountID": str,
        "filters": DescribeJobsRequestFiltersTypeDef,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

DescribeJobsRequestRequestTypeDef = TypedDict(
    "DescribeJobsRequestRequestTypeDef",
    {
        "accountID": str,
        "filters": DescribeJobsRequestFiltersTypeDef,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

DescribeReplicationConfigurationTemplatesResponseTypeDef = TypedDict(
    "DescribeReplicationConfigurationTemplatesResponseTypeDef",
    {
        "items": List[ReplicationConfigurationTemplateTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeSourceServersRequestDescribeSourceServersPaginateTypeDef = TypedDict(
    "DescribeSourceServersRequestDescribeSourceServersPaginateTypeDef",
    {
        "accountID": str,
        "filters": DescribeSourceServersRequestFiltersTypeDef,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

DescribeSourceServersRequestRequestTypeDef = TypedDict(
    "DescribeSourceServersRequestRequestTypeDef",
    {
        "accountID": str,
        "filters": DescribeSourceServersRequestFiltersTypeDef,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

DescribeVcenterClientsResponseTypeDef = TypedDict(
    "DescribeVcenterClientsResponseTypeDef",
    {
        "items": List[VcenterClientTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ExportTaskErrorTypeDef = TypedDict(
    "ExportTaskErrorTypeDef",
    {
        "errorData": ExportErrorDataTypeDef,
        "errorDateTime": str,
    },
    total=False,
)

ExportTaskTypeDef = TypedDict(
    "ExportTaskTypeDef",
    {
        "creationDateTime": str,
        "endDateTime": str,
        "exportID": str,
        "progressPercentage": float,
        "s3Bucket": str,
        "s3BucketOwner": str,
        "s3Key": str,
        "status": ExportStatusType,
        "summary": ExportTaskSummaryTypeDef,
    },
    total=False,
)

ImportTaskErrorTypeDef = TypedDict(
    "ImportTaskErrorTypeDef",
    {
        "errorData": ImportErrorDataTypeDef,
        "errorDateTime": str,
        "errorType": ImportErrorTypeType,
    },
    total=False,
)

ImportTaskSummaryTypeDef = TypedDict(
    "ImportTaskSummaryTypeDef",
    {
        "applications": ImportTaskSummaryApplicationsTypeDef,
        "servers": ImportTaskSummaryServersTypeDef,
        "waves": ImportTaskSummaryWavesTypeDef,
    },
    total=False,
)

_RequiredStartImportRequestRequestTypeDef = TypedDict(
    "_RequiredStartImportRequestRequestTypeDef",
    {
        "s3BucketSource": S3BucketSourceTypeDef,
    },
)
_OptionalStartImportRequestRequestTypeDef = TypedDict(
    "_OptionalStartImportRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class StartImportRequestRequestTypeDef(
    _RequiredStartImportRequestRequestTypeDef, _OptionalStartImportRequestRequestTypeDef
):
    pass


JobLogTypeDef = TypedDict(
    "JobLogTypeDef",
    {
        "event": JobLogEventType,
        "eventData": JobLogEventDataTypeDef,
        "logDateTime": str,
    },
    total=False,
)

LifeCycleLastCutoverTypeDef = TypedDict(
    "LifeCycleLastCutoverTypeDef",
    {
        "finalized": LifeCycleLastCutoverFinalizedTypeDef,
        "initiated": LifeCycleLastCutoverInitiatedTypeDef,
        "reverted": LifeCycleLastCutoverRevertedTypeDef,
    },
    total=False,
)

LifeCycleLastTestTypeDef = TypedDict(
    "LifeCycleLastTestTypeDef",
    {
        "finalized": LifeCycleLastTestFinalizedTypeDef,
        "initiated": LifeCycleLastTestInitiatedTypeDef,
        "reverted": LifeCycleLastTestRevertedTypeDef,
    },
    total=False,
)

ListApplicationsRequestListApplicationsPaginateTypeDef = TypedDict(
    "ListApplicationsRequestListApplicationsPaginateTypeDef",
    {
        "accountID": str,
        "filters": ListApplicationsRequestFiltersTypeDef,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListApplicationsRequestRequestTypeDef = TypedDict(
    "ListApplicationsRequestRequestTypeDef",
    {
        "accountID": str,
        "filters": ListApplicationsRequestFiltersTypeDef,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ListExportsRequestListExportsPaginateTypeDef = TypedDict(
    "ListExportsRequestListExportsPaginateTypeDef",
    {
        "filters": ListExportsRequestFiltersTypeDef,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListExportsRequestRequestTypeDef = TypedDict(
    "ListExportsRequestRequestTypeDef",
    {
        "filters": ListExportsRequestFiltersTypeDef,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ListImportsRequestListImportsPaginateTypeDef = TypedDict(
    "ListImportsRequestListImportsPaginateTypeDef",
    {
        "filters": ListImportsRequestFiltersTypeDef,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListImportsRequestRequestTypeDef = TypedDict(
    "ListImportsRequestRequestTypeDef",
    {
        "filters": ListImportsRequestFiltersTypeDef,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ListManagedAccountsResponseTypeDef = TypedDict(
    "ListManagedAccountsResponseTypeDef",
    {
        "items": List[ManagedAccountTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListSourceServerActionsRequestListSourceServerActionsPaginateTypeDef = TypedDict(
    "_RequiredListSourceServerActionsRequestListSourceServerActionsPaginateTypeDef",
    {
        "sourceServerID": str,
    },
)
_OptionalListSourceServerActionsRequestListSourceServerActionsPaginateTypeDef = TypedDict(
    "_OptionalListSourceServerActionsRequestListSourceServerActionsPaginateTypeDef",
    {
        "accountID": str,
        "filters": SourceServerActionsRequestFiltersTypeDef,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListSourceServerActionsRequestListSourceServerActionsPaginateTypeDef(
    _RequiredListSourceServerActionsRequestListSourceServerActionsPaginateTypeDef,
    _OptionalListSourceServerActionsRequestListSourceServerActionsPaginateTypeDef,
):
    pass


_RequiredListSourceServerActionsRequestRequestTypeDef = TypedDict(
    "_RequiredListSourceServerActionsRequestRequestTypeDef",
    {
        "sourceServerID": str,
    },
)
_OptionalListSourceServerActionsRequestRequestTypeDef = TypedDict(
    "_OptionalListSourceServerActionsRequestRequestTypeDef",
    {
        "accountID": str,
        "filters": SourceServerActionsRequestFiltersTypeDef,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)


class ListSourceServerActionsRequestRequestTypeDef(
    _RequiredListSourceServerActionsRequestRequestTypeDef,
    _OptionalListSourceServerActionsRequestRequestTypeDef,
):
    pass


_RequiredListTemplateActionsRequestListTemplateActionsPaginateTypeDef = TypedDict(
    "_RequiredListTemplateActionsRequestListTemplateActionsPaginateTypeDef",
    {
        "launchConfigurationTemplateID": str,
    },
)
_OptionalListTemplateActionsRequestListTemplateActionsPaginateTypeDef = TypedDict(
    "_OptionalListTemplateActionsRequestListTemplateActionsPaginateTypeDef",
    {
        "filters": TemplateActionsRequestFiltersTypeDef,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListTemplateActionsRequestListTemplateActionsPaginateTypeDef(
    _RequiredListTemplateActionsRequestListTemplateActionsPaginateTypeDef,
    _OptionalListTemplateActionsRequestListTemplateActionsPaginateTypeDef,
):
    pass


_RequiredListTemplateActionsRequestRequestTypeDef = TypedDict(
    "_RequiredListTemplateActionsRequestRequestTypeDef",
    {
        "launchConfigurationTemplateID": str,
    },
)
_OptionalListTemplateActionsRequestRequestTypeDef = TypedDict(
    "_OptionalListTemplateActionsRequestRequestTypeDef",
    {
        "filters": TemplateActionsRequestFiltersTypeDef,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)


class ListTemplateActionsRequestRequestTypeDef(
    _RequiredListTemplateActionsRequestRequestTypeDef,
    _OptionalListTemplateActionsRequestRequestTypeDef,
):
    pass


ListWavesRequestListWavesPaginateTypeDef = TypedDict(
    "ListWavesRequestListWavesPaginateTypeDef",
    {
        "accountID": str,
        "filters": ListWavesRequestFiltersTypeDef,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListWavesRequestRequestTypeDef = TypedDict(
    "ListWavesRequestRequestTypeDef",
    {
        "accountID": str,
        "filters": ListWavesRequestFiltersTypeDef,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

SourcePropertiesTypeDef = TypedDict(
    "SourcePropertiesTypeDef",
    {
        "cpus": List[CPUTypeDef],
        "disks": List[DiskTypeDef],
        "identificationHints": IdentificationHintsTypeDef,
        "lastUpdatedDateTime": str,
        "networkInterfaces": List[NetworkInterfaceTypeDef],
        "os": OSTypeDef,
        "ramBytes": int,
        "recommendedInstanceType": str,
    },
    total=False,
)

_RequiredPutSourceServerActionRequestRequestTypeDef = TypedDict(
    "_RequiredPutSourceServerActionRequestRequestTypeDef",
    {
        "actionID": str,
        "actionName": str,
        "documentIdentifier": str,
        "order": int,
        "sourceServerID": str,
    },
)
_OptionalPutSourceServerActionRequestRequestTypeDef = TypedDict(
    "_OptionalPutSourceServerActionRequestRequestTypeDef",
    {
        "accountID": str,
        "active": bool,
        "category": ActionCategoryType,
        "description": str,
        "documentVersion": str,
        "externalParameters": Mapping[str, SsmExternalParameterTypeDef],
        "mustSucceedForCutover": bool,
        "parameters": Mapping[str, Sequence[SsmParameterStoreParameterTypeDef]],
        "timeoutSeconds": int,
    },
    total=False,
)


class PutSourceServerActionRequestRequestTypeDef(
    _RequiredPutSourceServerActionRequestRequestTypeDef,
    _OptionalPutSourceServerActionRequestRequestTypeDef,
):
    pass


_RequiredPutTemplateActionRequestRequestTypeDef = TypedDict(
    "_RequiredPutTemplateActionRequestRequestTypeDef",
    {
        "actionID": str,
        "actionName": str,
        "documentIdentifier": str,
        "launchConfigurationTemplateID": str,
        "order": int,
    },
)
_OptionalPutTemplateActionRequestRequestTypeDef = TypedDict(
    "_OptionalPutTemplateActionRequestRequestTypeDef",
    {
        "active": bool,
        "category": ActionCategoryType,
        "description": str,
        "documentVersion": str,
        "externalParameters": Mapping[str, SsmExternalParameterTypeDef],
        "mustSucceedForCutover": bool,
        "operatingSystem": str,
        "parameters": Mapping[str, Sequence[SsmParameterStoreParameterTypeDef]],
        "timeoutSeconds": int,
    },
    total=False,
)


class PutTemplateActionRequestRequestTypeDef(
    _RequiredPutTemplateActionRequestRequestTypeDef, _OptionalPutTemplateActionRequestRequestTypeDef
):
    pass


SourceServerActionDocumentResponseMetadataTypeDef = TypedDict(
    "SourceServerActionDocumentResponseMetadataTypeDef",
    {
        "actionID": str,
        "actionName": str,
        "active": bool,
        "category": ActionCategoryType,
        "description": str,
        "documentIdentifier": str,
        "documentVersion": str,
        "externalParameters": Dict[str, SsmExternalParameterTypeDef],
        "mustSucceedForCutover": bool,
        "order": int,
        "parameters": Dict[str, List[SsmParameterStoreParameterTypeDef]],
        "timeoutSeconds": int,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

SourceServerActionDocumentTypeDef = TypedDict(
    "SourceServerActionDocumentTypeDef",
    {
        "actionID": str,
        "actionName": str,
        "active": bool,
        "category": ActionCategoryType,
        "description": str,
        "documentIdentifier": str,
        "documentVersion": str,
        "externalParameters": Dict[str, SsmExternalParameterTypeDef],
        "mustSucceedForCutover": bool,
        "order": int,
        "parameters": Dict[str, List[SsmParameterStoreParameterTypeDef]],
        "timeoutSeconds": int,
    },
    total=False,
)

_RequiredSsmDocumentTypeDef = TypedDict(
    "_RequiredSsmDocumentTypeDef",
    {
        "actionName": str,
        "ssmDocumentName": str,
    },
)
_OptionalSsmDocumentTypeDef = TypedDict(
    "_OptionalSsmDocumentTypeDef",
    {
        "externalParameters": Mapping[str, SsmExternalParameterTypeDef],
        "mustSucceedForCutover": bool,
        "parameters": Mapping[str, Sequence[SsmParameterStoreParameterTypeDef]],
        "timeoutSeconds": int,
    },
    total=False,
)


class SsmDocumentTypeDef(_RequiredSsmDocumentTypeDef, _OptionalSsmDocumentTypeDef):
    pass


TemplateActionDocumentResponseMetadataTypeDef = TypedDict(
    "TemplateActionDocumentResponseMetadataTypeDef",
    {
        "actionID": str,
        "actionName": str,
        "active": bool,
        "category": ActionCategoryType,
        "description": str,
        "documentIdentifier": str,
        "documentVersion": str,
        "externalParameters": Dict[str, SsmExternalParameterTypeDef],
        "mustSucceedForCutover": bool,
        "operatingSystem": str,
        "order": int,
        "parameters": Dict[str, List[SsmParameterStoreParameterTypeDef]],
        "timeoutSeconds": int,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

TemplateActionDocumentTypeDef = TypedDict(
    "TemplateActionDocumentTypeDef",
    {
        "actionID": str,
        "actionName": str,
        "active": bool,
        "category": ActionCategoryType,
        "description": str,
        "documentIdentifier": str,
        "documentVersion": str,
        "externalParameters": Dict[str, SsmExternalParameterTypeDef],
        "mustSucceedForCutover": bool,
        "operatingSystem": str,
        "order": int,
        "parameters": Dict[str, List[SsmParameterStoreParameterTypeDef]],
        "timeoutSeconds": int,
    },
    total=False,
)

ReplicationConfigurationTypeDef = TypedDict(
    "ReplicationConfigurationTypeDef",
    {
        "associateDefaultSecurityGroup": bool,
        "bandwidthThrottling": int,
        "createPublicIP": bool,
        "dataPlaneRouting": ReplicationConfigurationDataPlaneRoutingType,
        "defaultLargeStagingDiskType": ReplicationConfigurationDefaultLargeStagingDiskTypeType,
        "ebsEncryption": ReplicationConfigurationEbsEncryptionType,
        "ebsEncryptionKeyArn": str,
        "name": str,
        "replicatedDisks": List[ReplicationConfigurationReplicatedDiskTypeDef],
        "replicationServerInstanceType": str,
        "replicationServersSecurityGroupsIDs": List[str],
        "sourceServerID": str,
        "stagingAreaSubnetId": str,
        "stagingAreaTags": Dict[str, str],
        "useDedicatedReplicationServer": bool,
        "useFipsEndpoint": bool,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredUpdateReplicationConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateReplicationConfigurationRequestRequestTypeDef",
    {
        "sourceServerID": str,
    },
)
_OptionalUpdateReplicationConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateReplicationConfigurationRequestRequestTypeDef",
    {
        "accountID": str,
        "associateDefaultSecurityGroup": bool,
        "bandwidthThrottling": int,
        "createPublicIP": bool,
        "dataPlaneRouting": ReplicationConfigurationDataPlaneRoutingType,
        "defaultLargeStagingDiskType": ReplicationConfigurationDefaultLargeStagingDiskTypeType,
        "ebsEncryption": ReplicationConfigurationEbsEncryptionType,
        "ebsEncryptionKeyArn": str,
        "name": str,
        "replicatedDisks": Sequence[ReplicationConfigurationReplicatedDiskTypeDef],
        "replicationServerInstanceType": str,
        "replicationServersSecurityGroupsIDs": Sequence[str],
        "stagingAreaSubnetId": str,
        "stagingAreaTags": Mapping[str, str],
        "useDedicatedReplicationServer": bool,
        "useFipsEndpoint": bool,
    },
    total=False,
)


class UpdateReplicationConfigurationRequestRequestTypeDef(
    _RequiredUpdateReplicationConfigurationRequestRequestTypeDef,
    _OptionalUpdateReplicationConfigurationRequestRequestTypeDef,
):
    pass


WaveResponseMetadataTypeDef = TypedDict(
    "WaveResponseMetadataTypeDef",
    {
        "arn": str,
        "creationDateTime": str,
        "description": str,
        "isArchived": bool,
        "lastModifiedDateTime": str,
        "name": str,
        "tags": Dict[str, str],
        "waveAggregatedStatus": WaveAggregatedStatusTypeDef,
        "waveID": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

WaveTypeDef = TypedDict(
    "WaveTypeDef",
    {
        "arn": str,
        "creationDateTime": str,
        "description": str,
        "isArchived": bool,
        "lastModifiedDateTime": str,
        "name": str,
        "tags": Dict[str, str],
        "waveAggregatedStatus": WaveAggregatedStatusTypeDef,
        "waveID": str,
    },
    total=False,
)

ListApplicationsResponseTypeDef = TypedDict(
    "ListApplicationsResponseTypeDef",
    {
        "items": List[ApplicationTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DataReplicationInfoTypeDef = TypedDict(
    "DataReplicationInfoTypeDef",
    {
        "dataReplicationError": DataReplicationErrorTypeDef,
        "dataReplicationInitiation": DataReplicationInitiationTypeDef,
        "dataReplicationState": DataReplicationStateType,
        "etaDateTime": str,
        "lagDuration": str,
        "lastSnapshotDateTime": str,
        "replicatedDisks": List[DataReplicationInfoReplicatedDiskTypeDef],
    },
    total=False,
)

ListExportErrorsResponseTypeDef = TypedDict(
    "ListExportErrorsResponseTypeDef",
    {
        "items": List[ExportTaskErrorTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListExportsResponseTypeDef = TypedDict(
    "ListExportsResponseTypeDef",
    {
        "items": List[ExportTaskTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StartExportResponseTypeDef = TypedDict(
    "StartExportResponseTypeDef",
    {
        "exportTask": ExportTaskTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListImportErrorsResponseTypeDef = TypedDict(
    "ListImportErrorsResponseTypeDef",
    {
        "items": List[ImportTaskErrorTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ImportTaskTypeDef = TypedDict(
    "ImportTaskTypeDef",
    {
        "creationDateTime": str,
        "endDateTime": str,
        "importID": str,
        "progressPercentage": float,
        "s3BucketSource": S3BucketSourceTypeDef,
        "status": ImportStatusType,
        "summary": ImportTaskSummaryTypeDef,
    },
    total=False,
)

DescribeJobLogItemsResponseTypeDef = TypedDict(
    "DescribeJobLogItemsResponseTypeDef",
    {
        "items": List[JobLogTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

LifeCycleTypeDef = TypedDict(
    "LifeCycleTypeDef",
    {
        "addedToServiceDateTime": str,
        "elapsedReplicationDuration": str,
        "firstByteDateTime": str,
        "lastCutover": LifeCycleLastCutoverTypeDef,
        "lastSeenByServiceDateTime": str,
        "lastTest": LifeCycleLastTestTypeDef,
        "state": LifeCycleStateType,
    },
    total=False,
)

ListSourceServerActionsResponseTypeDef = TypedDict(
    "ListSourceServerActionsResponseTypeDef",
    {
        "items": List[SourceServerActionDocumentTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

JobPostLaunchActionsLaunchStatusTypeDef = TypedDict(
    "JobPostLaunchActionsLaunchStatusTypeDef",
    {
        "executionID": str,
        "executionStatus": PostLaunchActionExecutionStatusType,
        "failureReason": str,
        "ssmDocument": SsmDocumentTypeDef,
        "ssmDocumentType": SsmDocumentTypeType,
    },
    total=False,
)

PostLaunchActionsTypeDef = TypedDict(
    "PostLaunchActionsTypeDef",
    {
        "cloudWatchLogGroupName": str,
        "deployment": PostLaunchActionsDeploymentTypeType,
        "s3LogBucket": str,
        "s3OutputKeyPrefix": str,
        "ssmDocuments": Sequence[SsmDocumentTypeDef],
    },
    total=False,
)

ListTemplateActionsResponseTypeDef = TypedDict(
    "ListTemplateActionsResponseTypeDef",
    {
        "items": List[TemplateActionDocumentTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListWavesResponseTypeDef = TypedDict(
    "ListWavesResponseTypeDef",
    {
        "items": List[WaveTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListImportsResponseTypeDef = TypedDict(
    "ListImportsResponseTypeDef",
    {
        "items": List[ImportTaskTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StartImportResponseTypeDef = TypedDict(
    "StartImportResponseTypeDef",
    {
        "importTask": ImportTaskTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

SourceServerResponseMetadataTypeDef = TypedDict(
    "SourceServerResponseMetadataTypeDef",
    {
        "applicationID": str,
        "arn": str,
        "dataReplicationInfo": DataReplicationInfoTypeDef,
        "fqdnForActionFramework": str,
        "isArchived": bool,
        "launchedInstance": LaunchedInstanceTypeDef,
        "lifeCycle": LifeCycleTypeDef,
        "replicationType": ReplicationTypeType,
        "sourceProperties": SourcePropertiesTypeDef,
        "sourceServerID": str,
        "tags": Dict[str, str],
        "userProvidedID": str,
        "vcenterClientID": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

SourceServerTypeDef = TypedDict(
    "SourceServerTypeDef",
    {
        "applicationID": str,
        "arn": str,
        "dataReplicationInfo": DataReplicationInfoTypeDef,
        "fqdnForActionFramework": str,
        "isArchived": bool,
        "launchedInstance": LaunchedInstanceTypeDef,
        "lifeCycle": LifeCycleTypeDef,
        "replicationType": ReplicationTypeType,
        "sourceProperties": SourcePropertiesTypeDef,
        "sourceServerID": str,
        "tags": Dict[str, str],
        "userProvidedID": str,
        "vcenterClientID": str,
    },
    total=False,
)

PostLaunchActionsStatusTypeDef = TypedDict(
    "PostLaunchActionsStatusTypeDef",
    {
        "postLaunchActionsLaunchStatusList": List[JobPostLaunchActionsLaunchStatusTypeDef],
        "ssmAgentDiscoveryDatetime": str,
    },
    total=False,
)

CreateLaunchConfigurationTemplateRequestRequestTypeDef = TypedDict(
    "CreateLaunchConfigurationTemplateRequestRequestTypeDef",
    {
        "associatePublicIpAddress": bool,
        "bootMode": BootModeType,
        "copyPrivateIp": bool,
        "copyTags": bool,
        "enableMapAutoTagging": bool,
        "largeVolumeConf": LaunchTemplateDiskConfTypeDef,
        "launchDisposition": LaunchDispositionType,
        "licensing": LicensingTypeDef,
        "mapAutoTaggingMpeID": str,
        "postLaunchActions": PostLaunchActionsTypeDef,
        "smallVolumeConf": LaunchTemplateDiskConfTypeDef,
        "smallVolumeMaxSize": int,
        "tags": Mapping[str, str],
        "targetInstanceTypeRightSizingMethod": TargetInstanceTypeRightSizingMethodType,
    },
    total=False,
)

LaunchConfigurationTemplateResponseMetadataTypeDef = TypedDict(
    "LaunchConfigurationTemplateResponseMetadataTypeDef",
    {
        "arn": str,
        "associatePublicIpAddress": bool,
        "bootMode": BootModeType,
        "copyPrivateIp": bool,
        "copyTags": bool,
        "ec2LaunchTemplateID": str,
        "enableMapAutoTagging": bool,
        "largeVolumeConf": LaunchTemplateDiskConfTypeDef,
        "launchConfigurationTemplateID": str,
        "launchDisposition": LaunchDispositionType,
        "licensing": LicensingTypeDef,
        "mapAutoTaggingMpeID": str,
        "postLaunchActions": PostLaunchActionsTypeDef,
        "smallVolumeConf": LaunchTemplateDiskConfTypeDef,
        "smallVolumeMaxSize": int,
        "tags": Dict[str, str],
        "targetInstanceTypeRightSizingMethod": TargetInstanceTypeRightSizingMethodType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredLaunchConfigurationTemplateTypeDef = TypedDict(
    "_RequiredLaunchConfigurationTemplateTypeDef",
    {
        "launchConfigurationTemplateID": str,
    },
)
_OptionalLaunchConfigurationTemplateTypeDef = TypedDict(
    "_OptionalLaunchConfigurationTemplateTypeDef",
    {
        "arn": str,
        "associatePublicIpAddress": bool,
        "bootMode": BootModeType,
        "copyPrivateIp": bool,
        "copyTags": bool,
        "ec2LaunchTemplateID": str,
        "enableMapAutoTagging": bool,
        "largeVolumeConf": LaunchTemplateDiskConfTypeDef,
        "launchDisposition": LaunchDispositionType,
        "licensing": LicensingTypeDef,
        "mapAutoTaggingMpeID": str,
        "postLaunchActions": PostLaunchActionsTypeDef,
        "smallVolumeConf": LaunchTemplateDiskConfTypeDef,
        "smallVolumeMaxSize": int,
        "tags": Dict[str, str],
        "targetInstanceTypeRightSizingMethod": TargetInstanceTypeRightSizingMethodType,
    },
    total=False,
)


class LaunchConfigurationTemplateTypeDef(
    _RequiredLaunchConfigurationTemplateTypeDef, _OptionalLaunchConfigurationTemplateTypeDef
):
    pass


LaunchConfigurationTypeDef = TypedDict(
    "LaunchConfigurationTypeDef",
    {
        "bootMode": BootModeType,
        "copyPrivateIp": bool,
        "copyTags": bool,
        "ec2LaunchTemplateID": str,
        "enableMapAutoTagging": bool,
        "launchDisposition": LaunchDispositionType,
        "licensing": LicensingTypeDef,
        "mapAutoTaggingMpeID": str,
        "name": str,
        "postLaunchActions": PostLaunchActionsTypeDef,
        "sourceServerID": str,
        "targetInstanceTypeRightSizingMethod": TargetInstanceTypeRightSizingMethodType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredUpdateLaunchConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateLaunchConfigurationRequestRequestTypeDef",
    {
        "sourceServerID": str,
    },
)
_OptionalUpdateLaunchConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateLaunchConfigurationRequestRequestTypeDef",
    {
        "accountID": str,
        "bootMode": BootModeType,
        "copyPrivateIp": bool,
        "copyTags": bool,
        "enableMapAutoTagging": bool,
        "launchDisposition": LaunchDispositionType,
        "licensing": LicensingTypeDef,
        "mapAutoTaggingMpeID": str,
        "name": str,
        "postLaunchActions": PostLaunchActionsTypeDef,
        "targetInstanceTypeRightSizingMethod": TargetInstanceTypeRightSizingMethodType,
    },
    total=False,
)


class UpdateLaunchConfigurationRequestRequestTypeDef(
    _RequiredUpdateLaunchConfigurationRequestRequestTypeDef,
    _OptionalUpdateLaunchConfigurationRequestRequestTypeDef,
):
    pass


_RequiredUpdateLaunchConfigurationTemplateRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateLaunchConfigurationTemplateRequestRequestTypeDef",
    {
        "launchConfigurationTemplateID": str,
    },
)
_OptionalUpdateLaunchConfigurationTemplateRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateLaunchConfigurationTemplateRequestRequestTypeDef",
    {
        "associatePublicIpAddress": bool,
        "bootMode": BootModeType,
        "copyPrivateIp": bool,
        "copyTags": bool,
        "enableMapAutoTagging": bool,
        "largeVolumeConf": LaunchTemplateDiskConfTypeDef,
        "launchDisposition": LaunchDispositionType,
        "licensing": LicensingTypeDef,
        "mapAutoTaggingMpeID": str,
        "postLaunchActions": PostLaunchActionsTypeDef,
        "smallVolumeConf": LaunchTemplateDiskConfTypeDef,
        "smallVolumeMaxSize": int,
        "targetInstanceTypeRightSizingMethod": TargetInstanceTypeRightSizingMethodType,
    },
    total=False,
)


class UpdateLaunchConfigurationTemplateRequestRequestTypeDef(
    _RequiredUpdateLaunchConfigurationTemplateRequestRequestTypeDef,
    _OptionalUpdateLaunchConfigurationTemplateRequestRequestTypeDef,
):
    pass


DescribeSourceServersResponseTypeDef = TypedDict(
    "DescribeSourceServersResponseTypeDef",
    {
        "items": List[SourceServerTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredParticipatingServerTypeDef = TypedDict(
    "_RequiredParticipatingServerTypeDef",
    {
        "sourceServerID": str,
    },
)
_OptionalParticipatingServerTypeDef = TypedDict(
    "_OptionalParticipatingServerTypeDef",
    {
        "launchStatus": LaunchStatusType,
        "launchedEc2InstanceID": str,
        "postLaunchActionsStatus": PostLaunchActionsStatusTypeDef,
    },
    total=False,
)


class ParticipatingServerTypeDef(
    _RequiredParticipatingServerTypeDef, _OptionalParticipatingServerTypeDef
):
    pass


DescribeLaunchConfigurationTemplatesResponseTypeDef = TypedDict(
    "DescribeLaunchConfigurationTemplatesResponseTypeDef",
    {
        "items": List[LaunchConfigurationTemplateTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredJobTypeDef = TypedDict(
    "_RequiredJobTypeDef",
    {
        "jobID": str,
    },
)
_OptionalJobTypeDef = TypedDict(
    "_OptionalJobTypeDef",
    {
        "arn": str,
        "creationDateTime": str,
        "endDateTime": str,
        "initiatedBy": InitiatedByType,
        "participatingServers": List[ParticipatingServerTypeDef],
        "status": JobStatusType,
        "tags": Dict[str, str],
        "type": JobTypeType,
    },
    total=False,
)


class JobTypeDef(_RequiredJobTypeDef, _OptionalJobTypeDef):
    pass


DescribeJobsResponseTypeDef = TypedDict(
    "DescribeJobsResponseTypeDef",
    {
        "items": List[JobTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StartCutoverResponseTypeDef = TypedDict(
    "StartCutoverResponseTypeDef",
    {
        "job": JobTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StartTestResponseTypeDef = TypedDict(
    "StartTestResponseTypeDef",
    {
        "job": JobTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

TerminateTargetInstancesResponseTypeDef = TypedDict(
    "TerminateTargetInstancesResponseTypeDef",
    {
        "job": JobTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)
