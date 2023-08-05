"""
Type annotations for greengrassv2 service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_greengrassv2/type_defs/)

Usage::

    ```python
    from mypy_boto3_greengrassv2.type_defs import AssociateClientDeviceWithCoreDeviceEntryTypeDef

    data: AssociateClientDeviceWithCoreDeviceEntryTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    CloudComponentStateType,
    ComponentDependencyTypeType,
    ComponentVisibilityScopeType,
    CoreDeviceStatusType,
    DeploymentComponentUpdatePolicyActionType,
    DeploymentFailureHandlingPolicyType,
    DeploymentHistoryFilterType,
    DeploymentStatusType,
    EffectiveDeploymentExecutionStatusType,
    InstalledComponentLifecycleStateType,
    InstalledComponentTopologyFilterType,
    IoTJobExecutionFailureTypeType,
    LambdaEventSourceTypeType,
    LambdaFilesystemPermissionType,
    LambdaInputPayloadEncodingTypeType,
    LambdaIsolationModeType,
    RecipeOutputFormatType,
    VendorGuidanceType,
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
    "AssociateClientDeviceWithCoreDeviceEntryTypeDef",
    "AssociateClientDeviceWithCoreDeviceErrorEntryTypeDef",
    "AssociateServiceRoleToAccountRequestRequestTypeDef",
    "AssociateServiceRoleToAccountResponseTypeDef",
    "AssociatedClientDeviceTypeDef",
    "DisassociateClientDeviceFromCoreDeviceEntryTypeDef",
    "DisassociateClientDeviceFromCoreDeviceErrorEntryTypeDef",
    "CancelDeploymentRequestRequestTypeDef",
    "CancelDeploymentResponseTypeDef",
    "CloudComponentStatusTypeDef",
    "ComponentCandidateTypeDef",
    "ComponentConfigurationUpdateTypeDef",
    "ComponentDependencyRequirementTypeDef",
    "ComponentPlatformTypeDef",
    "SystemResourceLimitsTypeDef",
    "ComponentVersionListItemTypeDef",
    "ConnectivityInfoTypeDef",
    "CoreDeviceTypeDef",
    "CreateDeploymentResponseTypeDef",
    "DeleteComponentRequestRequestTypeDef",
    "DeleteCoreDeviceRequestRequestTypeDef",
    "DeleteDeploymentRequestRequestTypeDef",
    "DeploymentComponentUpdatePolicyTypeDef",
    "DeploymentConfigurationValidationPolicyTypeDef",
    "IoTJobTimeoutConfigTypeDef",
    "DeploymentTypeDef",
    "DescribeComponentRequestRequestTypeDef",
    "DisassociateServiceRoleFromAccountResponseTypeDef",
    "EffectiveDeploymentStatusDetailsTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetComponentRequestRequestTypeDef",
    "GetComponentResponseTypeDef",
    "GetComponentVersionArtifactRequestRequestTypeDef",
    "GetComponentVersionArtifactResponseTypeDef",
    "GetConnectivityInfoRequestRequestTypeDef",
    "GetCoreDeviceRequestRequestTypeDef",
    "GetCoreDeviceResponseTypeDef",
    "GetDeploymentRequestRequestTypeDef",
    "GetServiceRoleForAccountResponseTypeDef",
    "InstalledComponentTypeDef",
    "IoTJobAbortCriteriaTypeDef",
    "IoTJobRateIncreaseCriteriaTypeDef",
    "LambdaDeviceMountTypeDef",
    "LambdaVolumeMountTypeDef",
    "LambdaEventSourceTypeDef",
    "ListClientDevicesAssociatedWithCoreDeviceRequestListClientDevicesAssociatedWithCoreDevicePaginateTypeDef",
    "ListClientDevicesAssociatedWithCoreDeviceRequestRequestTypeDef",
    "ListComponentVersionsRequestListComponentVersionsPaginateTypeDef",
    "ListComponentVersionsRequestRequestTypeDef",
    "ListComponentsRequestListComponentsPaginateTypeDef",
    "ListComponentsRequestRequestTypeDef",
    "ListCoreDevicesRequestListCoreDevicesPaginateTypeDef",
    "ListCoreDevicesRequestRequestTypeDef",
    "ListDeploymentsRequestListDeploymentsPaginateTypeDef",
    "ListDeploymentsRequestRequestTypeDef",
    "ListEffectiveDeploymentsRequestListEffectiveDeploymentsPaginateTypeDef",
    "ListEffectiveDeploymentsRequestRequestTypeDef",
    "ListInstalledComponentsRequestListInstalledComponentsPaginateTypeDef",
    "ListInstalledComponentsRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PaginatorConfigTypeDef",
    "ResolvedComponentVersionTypeDef",
    "ResponseMetadataTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateConnectivityInfoResponseTypeDef",
    "BatchAssociateClientDeviceWithCoreDeviceRequestRequestTypeDef",
    "BatchAssociateClientDeviceWithCoreDeviceResponseTypeDef",
    "ListClientDevicesAssociatedWithCoreDeviceResponseTypeDef",
    "BatchDisassociateClientDeviceFromCoreDeviceRequestRequestTypeDef",
    "BatchDisassociateClientDeviceFromCoreDeviceResponseTypeDef",
    "CreateComponentVersionResponseTypeDef",
    "ComponentLatestVersionTypeDef",
    "DescribeComponentResponseTypeDef",
    "ResolveComponentCandidatesRequestRequestTypeDef",
    "ComponentRunWithTypeDef",
    "ListComponentVersionsResponseTypeDef",
    "GetConnectivityInfoResponseTypeDef",
    "UpdateConnectivityInfoRequestRequestTypeDef",
    "ListCoreDevicesResponseTypeDef",
    "DeploymentPoliciesTypeDef",
    "ListDeploymentsResponseTypeDef",
    "EffectiveDeploymentTypeDef",
    "ListInstalledComponentsResponseTypeDef",
    "IoTJobAbortConfigTypeDef",
    "IoTJobExponentialRolloutRateTypeDef",
    "LambdaContainerParamsTypeDef",
    "ResolveComponentCandidatesResponseTypeDef",
    "ComponentTypeDef",
    "ComponentDeploymentSpecificationTypeDef",
    "ListEffectiveDeploymentsResponseTypeDef",
    "IoTJobExecutionsRolloutConfigTypeDef",
    "LambdaLinuxProcessParamsTypeDef",
    "ListComponentsResponseTypeDef",
    "DeploymentIoTJobConfigurationTypeDef",
    "LambdaExecutionParametersTypeDef",
    "CreateDeploymentRequestRequestTypeDef",
    "GetDeploymentResponseTypeDef",
    "LambdaFunctionRecipeSourceTypeDef",
    "CreateComponentVersionRequestRequestTypeDef",
)

AssociateClientDeviceWithCoreDeviceEntryTypeDef = TypedDict(
    "AssociateClientDeviceWithCoreDeviceEntryTypeDef",
    {
        "thingName": str,
    },
)

AssociateClientDeviceWithCoreDeviceErrorEntryTypeDef = TypedDict(
    "AssociateClientDeviceWithCoreDeviceErrorEntryTypeDef",
    {
        "thingName": str,
        "code": str,
        "message": str,
    },
    total=False,
)

AssociateServiceRoleToAccountRequestRequestTypeDef = TypedDict(
    "AssociateServiceRoleToAccountRequestRequestTypeDef",
    {
        "roleArn": str,
    },
)

AssociateServiceRoleToAccountResponseTypeDef = TypedDict(
    "AssociateServiceRoleToAccountResponseTypeDef",
    {
        "associatedAt": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

AssociatedClientDeviceTypeDef = TypedDict(
    "AssociatedClientDeviceTypeDef",
    {
        "thingName": str,
        "associationTimestamp": datetime,
    },
    total=False,
)

DisassociateClientDeviceFromCoreDeviceEntryTypeDef = TypedDict(
    "DisassociateClientDeviceFromCoreDeviceEntryTypeDef",
    {
        "thingName": str,
    },
)

DisassociateClientDeviceFromCoreDeviceErrorEntryTypeDef = TypedDict(
    "DisassociateClientDeviceFromCoreDeviceErrorEntryTypeDef",
    {
        "thingName": str,
        "code": str,
        "message": str,
    },
    total=False,
)

CancelDeploymentRequestRequestTypeDef = TypedDict(
    "CancelDeploymentRequestRequestTypeDef",
    {
        "deploymentId": str,
    },
)

CancelDeploymentResponseTypeDef = TypedDict(
    "CancelDeploymentResponseTypeDef",
    {
        "message": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CloudComponentStatusTypeDef = TypedDict(
    "CloudComponentStatusTypeDef",
    {
        "componentState": CloudComponentStateType,
        "message": str,
        "errors": Dict[str, str],
        "vendorGuidance": VendorGuidanceType,
        "vendorGuidanceMessage": str,
    },
    total=False,
)

ComponentCandidateTypeDef = TypedDict(
    "ComponentCandidateTypeDef",
    {
        "componentName": str,
        "componentVersion": str,
        "versionRequirements": Mapping[str, str],
    },
    total=False,
)

ComponentConfigurationUpdateTypeDef = TypedDict(
    "ComponentConfigurationUpdateTypeDef",
    {
        "merge": str,
        "reset": Sequence[str],
    },
    total=False,
)

ComponentDependencyRequirementTypeDef = TypedDict(
    "ComponentDependencyRequirementTypeDef",
    {
        "versionRequirement": str,
        "dependencyType": ComponentDependencyTypeType,
    },
    total=False,
)

ComponentPlatformTypeDef = TypedDict(
    "ComponentPlatformTypeDef",
    {
        "name": str,
        "attributes": Mapping[str, str],
    },
    total=False,
)

SystemResourceLimitsTypeDef = TypedDict(
    "SystemResourceLimitsTypeDef",
    {
        "memory": int,
        "cpus": float,
    },
    total=False,
)

ComponentVersionListItemTypeDef = TypedDict(
    "ComponentVersionListItemTypeDef",
    {
        "componentName": str,
        "componentVersion": str,
        "arn": str,
    },
    total=False,
)

ConnectivityInfoTypeDef = TypedDict(
    "ConnectivityInfoTypeDef",
    {
        "id": str,
        "hostAddress": str,
        "portNumber": int,
        "metadata": str,
    },
    total=False,
)

CoreDeviceTypeDef = TypedDict(
    "CoreDeviceTypeDef",
    {
        "coreDeviceThingName": str,
        "status": CoreDeviceStatusType,
        "lastStatusUpdateTimestamp": datetime,
    },
    total=False,
)

CreateDeploymentResponseTypeDef = TypedDict(
    "CreateDeploymentResponseTypeDef",
    {
        "deploymentId": str,
        "iotJobId": str,
        "iotJobArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteComponentRequestRequestTypeDef = TypedDict(
    "DeleteComponentRequestRequestTypeDef",
    {
        "arn": str,
    },
)

DeleteCoreDeviceRequestRequestTypeDef = TypedDict(
    "DeleteCoreDeviceRequestRequestTypeDef",
    {
        "coreDeviceThingName": str,
    },
)

DeleteDeploymentRequestRequestTypeDef = TypedDict(
    "DeleteDeploymentRequestRequestTypeDef",
    {
        "deploymentId": str,
    },
)

DeploymentComponentUpdatePolicyTypeDef = TypedDict(
    "DeploymentComponentUpdatePolicyTypeDef",
    {
        "timeoutInSeconds": int,
        "action": DeploymentComponentUpdatePolicyActionType,
    },
    total=False,
)

DeploymentConfigurationValidationPolicyTypeDef = TypedDict(
    "DeploymentConfigurationValidationPolicyTypeDef",
    {
        "timeoutInSeconds": int,
    },
    total=False,
)

IoTJobTimeoutConfigTypeDef = TypedDict(
    "IoTJobTimeoutConfigTypeDef",
    {
        "inProgressTimeoutInMinutes": int,
    },
    total=False,
)

DeploymentTypeDef = TypedDict(
    "DeploymentTypeDef",
    {
        "targetArn": str,
        "revisionId": str,
        "deploymentId": str,
        "deploymentName": str,
        "creationTimestamp": datetime,
        "deploymentStatus": DeploymentStatusType,
        "isLatestForTarget": bool,
        "parentTargetArn": str,
    },
    total=False,
)

DescribeComponentRequestRequestTypeDef = TypedDict(
    "DescribeComponentRequestRequestTypeDef",
    {
        "arn": str,
    },
)

DisassociateServiceRoleFromAccountResponseTypeDef = TypedDict(
    "DisassociateServiceRoleFromAccountResponseTypeDef",
    {
        "disassociatedAt": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

EffectiveDeploymentStatusDetailsTypeDef = TypedDict(
    "EffectiveDeploymentStatusDetailsTypeDef",
    {
        "errorStack": List[str],
        "errorTypes": List[str],
    },
    total=False,
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredGetComponentRequestRequestTypeDef = TypedDict(
    "_RequiredGetComponentRequestRequestTypeDef",
    {
        "arn": str,
    },
)
_OptionalGetComponentRequestRequestTypeDef = TypedDict(
    "_OptionalGetComponentRequestRequestTypeDef",
    {
        "recipeOutputFormat": RecipeOutputFormatType,
    },
    total=False,
)

class GetComponentRequestRequestTypeDef(
    _RequiredGetComponentRequestRequestTypeDef, _OptionalGetComponentRequestRequestTypeDef
):
    pass

GetComponentResponseTypeDef = TypedDict(
    "GetComponentResponseTypeDef",
    {
        "recipeOutputFormat": RecipeOutputFormatType,
        "recipe": bytes,
        "tags": Dict[str, str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetComponentVersionArtifactRequestRequestTypeDef = TypedDict(
    "GetComponentVersionArtifactRequestRequestTypeDef",
    {
        "arn": str,
        "artifactName": str,
    },
)

GetComponentVersionArtifactResponseTypeDef = TypedDict(
    "GetComponentVersionArtifactResponseTypeDef",
    {
        "preSignedUrl": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetConnectivityInfoRequestRequestTypeDef = TypedDict(
    "GetConnectivityInfoRequestRequestTypeDef",
    {
        "thingName": str,
    },
)

GetCoreDeviceRequestRequestTypeDef = TypedDict(
    "GetCoreDeviceRequestRequestTypeDef",
    {
        "coreDeviceThingName": str,
    },
)

GetCoreDeviceResponseTypeDef = TypedDict(
    "GetCoreDeviceResponseTypeDef",
    {
        "coreDeviceThingName": str,
        "coreVersion": str,
        "platform": str,
        "architecture": str,
        "status": CoreDeviceStatusType,
        "lastStatusUpdateTimestamp": datetime,
        "tags": Dict[str, str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetDeploymentRequestRequestTypeDef = TypedDict(
    "GetDeploymentRequestRequestTypeDef",
    {
        "deploymentId": str,
    },
)

GetServiceRoleForAccountResponseTypeDef = TypedDict(
    "GetServiceRoleForAccountResponseTypeDef",
    {
        "associatedAt": str,
        "roleArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

InstalledComponentTypeDef = TypedDict(
    "InstalledComponentTypeDef",
    {
        "componentName": str,
        "componentVersion": str,
        "lifecycleState": InstalledComponentLifecycleStateType,
        "lifecycleStateDetails": str,
        "isRoot": bool,
        "lastStatusChangeTimestamp": datetime,
        "lastReportedTimestamp": datetime,
        "lastInstallationSource": str,
        "lifecycleStatusCodes": List[str],
    },
    total=False,
)

IoTJobAbortCriteriaTypeDef = TypedDict(
    "IoTJobAbortCriteriaTypeDef",
    {
        "failureType": IoTJobExecutionFailureTypeType,
        "action": Literal["CANCEL"],
        "thresholdPercentage": float,
        "minNumberOfExecutedThings": int,
    },
)

IoTJobRateIncreaseCriteriaTypeDef = TypedDict(
    "IoTJobRateIncreaseCriteriaTypeDef",
    {
        "numberOfNotifiedThings": int,
        "numberOfSucceededThings": int,
    },
    total=False,
)

_RequiredLambdaDeviceMountTypeDef = TypedDict(
    "_RequiredLambdaDeviceMountTypeDef",
    {
        "path": str,
    },
)
_OptionalLambdaDeviceMountTypeDef = TypedDict(
    "_OptionalLambdaDeviceMountTypeDef",
    {
        "permission": LambdaFilesystemPermissionType,
        "addGroupOwner": bool,
    },
    total=False,
)

class LambdaDeviceMountTypeDef(
    _RequiredLambdaDeviceMountTypeDef, _OptionalLambdaDeviceMountTypeDef
):
    pass

_RequiredLambdaVolumeMountTypeDef = TypedDict(
    "_RequiredLambdaVolumeMountTypeDef",
    {
        "sourcePath": str,
        "destinationPath": str,
    },
)
_OptionalLambdaVolumeMountTypeDef = TypedDict(
    "_OptionalLambdaVolumeMountTypeDef",
    {
        "permission": LambdaFilesystemPermissionType,
        "addGroupOwner": bool,
    },
    total=False,
)

class LambdaVolumeMountTypeDef(
    _RequiredLambdaVolumeMountTypeDef, _OptionalLambdaVolumeMountTypeDef
):
    pass

LambdaEventSourceTypeDef = TypedDict(
    "LambdaEventSourceTypeDef",
    {
        "topic": str,
        "type": LambdaEventSourceTypeType,
    },
)

_RequiredListClientDevicesAssociatedWithCoreDeviceRequestListClientDevicesAssociatedWithCoreDevicePaginateTypeDef = TypedDict(
    "_RequiredListClientDevicesAssociatedWithCoreDeviceRequestListClientDevicesAssociatedWithCoreDevicePaginateTypeDef",
    {
        "coreDeviceThingName": str,
    },
)
_OptionalListClientDevicesAssociatedWithCoreDeviceRequestListClientDevicesAssociatedWithCoreDevicePaginateTypeDef = TypedDict(
    "_OptionalListClientDevicesAssociatedWithCoreDeviceRequestListClientDevicesAssociatedWithCoreDevicePaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

class ListClientDevicesAssociatedWithCoreDeviceRequestListClientDevicesAssociatedWithCoreDevicePaginateTypeDef(
    _RequiredListClientDevicesAssociatedWithCoreDeviceRequestListClientDevicesAssociatedWithCoreDevicePaginateTypeDef,
    _OptionalListClientDevicesAssociatedWithCoreDeviceRequestListClientDevicesAssociatedWithCoreDevicePaginateTypeDef,
):
    pass

_RequiredListClientDevicesAssociatedWithCoreDeviceRequestRequestTypeDef = TypedDict(
    "_RequiredListClientDevicesAssociatedWithCoreDeviceRequestRequestTypeDef",
    {
        "coreDeviceThingName": str,
    },
)
_OptionalListClientDevicesAssociatedWithCoreDeviceRequestRequestTypeDef = TypedDict(
    "_OptionalListClientDevicesAssociatedWithCoreDeviceRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

class ListClientDevicesAssociatedWithCoreDeviceRequestRequestTypeDef(
    _RequiredListClientDevicesAssociatedWithCoreDeviceRequestRequestTypeDef,
    _OptionalListClientDevicesAssociatedWithCoreDeviceRequestRequestTypeDef,
):
    pass

_RequiredListComponentVersionsRequestListComponentVersionsPaginateTypeDef = TypedDict(
    "_RequiredListComponentVersionsRequestListComponentVersionsPaginateTypeDef",
    {
        "arn": str,
    },
)
_OptionalListComponentVersionsRequestListComponentVersionsPaginateTypeDef = TypedDict(
    "_OptionalListComponentVersionsRequestListComponentVersionsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

class ListComponentVersionsRequestListComponentVersionsPaginateTypeDef(
    _RequiredListComponentVersionsRequestListComponentVersionsPaginateTypeDef,
    _OptionalListComponentVersionsRequestListComponentVersionsPaginateTypeDef,
):
    pass

_RequiredListComponentVersionsRequestRequestTypeDef = TypedDict(
    "_RequiredListComponentVersionsRequestRequestTypeDef",
    {
        "arn": str,
    },
)
_OptionalListComponentVersionsRequestRequestTypeDef = TypedDict(
    "_OptionalListComponentVersionsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

class ListComponentVersionsRequestRequestTypeDef(
    _RequiredListComponentVersionsRequestRequestTypeDef,
    _OptionalListComponentVersionsRequestRequestTypeDef,
):
    pass

ListComponentsRequestListComponentsPaginateTypeDef = TypedDict(
    "ListComponentsRequestListComponentsPaginateTypeDef",
    {
        "scope": ComponentVisibilityScopeType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListComponentsRequestRequestTypeDef = TypedDict(
    "ListComponentsRequestRequestTypeDef",
    {
        "scope": ComponentVisibilityScopeType,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ListCoreDevicesRequestListCoreDevicesPaginateTypeDef = TypedDict(
    "ListCoreDevicesRequestListCoreDevicesPaginateTypeDef",
    {
        "thingGroupArn": str,
        "status": CoreDeviceStatusType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListCoreDevicesRequestRequestTypeDef = TypedDict(
    "ListCoreDevicesRequestRequestTypeDef",
    {
        "thingGroupArn": str,
        "status": CoreDeviceStatusType,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ListDeploymentsRequestListDeploymentsPaginateTypeDef = TypedDict(
    "ListDeploymentsRequestListDeploymentsPaginateTypeDef",
    {
        "targetArn": str,
        "historyFilter": DeploymentHistoryFilterType,
        "parentTargetArn": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListDeploymentsRequestRequestTypeDef = TypedDict(
    "ListDeploymentsRequestRequestTypeDef",
    {
        "targetArn": str,
        "historyFilter": DeploymentHistoryFilterType,
        "parentTargetArn": str,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

_RequiredListEffectiveDeploymentsRequestListEffectiveDeploymentsPaginateTypeDef = TypedDict(
    "_RequiredListEffectiveDeploymentsRequestListEffectiveDeploymentsPaginateTypeDef",
    {
        "coreDeviceThingName": str,
    },
)
_OptionalListEffectiveDeploymentsRequestListEffectiveDeploymentsPaginateTypeDef = TypedDict(
    "_OptionalListEffectiveDeploymentsRequestListEffectiveDeploymentsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

class ListEffectiveDeploymentsRequestListEffectiveDeploymentsPaginateTypeDef(
    _RequiredListEffectiveDeploymentsRequestListEffectiveDeploymentsPaginateTypeDef,
    _OptionalListEffectiveDeploymentsRequestListEffectiveDeploymentsPaginateTypeDef,
):
    pass

_RequiredListEffectiveDeploymentsRequestRequestTypeDef = TypedDict(
    "_RequiredListEffectiveDeploymentsRequestRequestTypeDef",
    {
        "coreDeviceThingName": str,
    },
)
_OptionalListEffectiveDeploymentsRequestRequestTypeDef = TypedDict(
    "_OptionalListEffectiveDeploymentsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

class ListEffectiveDeploymentsRequestRequestTypeDef(
    _RequiredListEffectiveDeploymentsRequestRequestTypeDef,
    _OptionalListEffectiveDeploymentsRequestRequestTypeDef,
):
    pass

_RequiredListInstalledComponentsRequestListInstalledComponentsPaginateTypeDef = TypedDict(
    "_RequiredListInstalledComponentsRequestListInstalledComponentsPaginateTypeDef",
    {
        "coreDeviceThingName": str,
    },
)
_OptionalListInstalledComponentsRequestListInstalledComponentsPaginateTypeDef = TypedDict(
    "_OptionalListInstalledComponentsRequestListInstalledComponentsPaginateTypeDef",
    {
        "topologyFilter": InstalledComponentTopologyFilterType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

class ListInstalledComponentsRequestListInstalledComponentsPaginateTypeDef(
    _RequiredListInstalledComponentsRequestListInstalledComponentsPaginateTypeDef,
    _OptionalListInstalledComponentsRequestListInstalledComponentsPaginateTypeDef,
):
    pass

_RequiredListInstalledComponentsRequestRequestTypeDef = TypedDict(
    "_RequiredListInstalledComponentsRequestRequestTypeDef",
    {
        "coreDeviceThingName": str,
    },
)
_OptionalListInstalledComponentsRequestRequestTypeDef = TypedDict(
    "_OptionalListInstalledComponentsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
        "topologyFilter": InstalledComponentTopologyFilterType,
    },
    total=False,
)

class ListInstalledComponentsRequestRequestTypeDef(
    _RequiredListInstalledComponentsRequestRequestTypeDef,
    _OptionalListInstalledComponentsRequestRequestTypeDef,
):
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

ResolvedComponentVersionTypeDef = TypedDict(
    "ResolvedComponentVersionTypeDef",
    {
        "arn": str,
        "componentName": str,
        "componentVersion": str,
        "recipe": bytes,
        "vendorGuidance": VendorGuidanceType,
        "message": str,
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

UpdateConnectivityInfoResponseTypeDef = TypedDict(
    "UpdateConnectivityInfoResponseTypeDef",
    {
        "version": str,
        "message": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredBatchAssociateClientDeviceWithCoreDeviceRequestRequestTypeDef = TypedDict(
    "_RequiredBatchAssociateClientDeviceWithCoreDeviceRequestRequestTypeDef",
    {
        "coreDeviceThingName": str,
    },
)
_OptionalBatchAssociateClientDeviceWithCoreDeviceRequestRequestTypeDef = TypedDict(
    "_OptionalBatchAssociateClientDeviceWithCoreDeviceRequestRequestTypeDef",
    {
        "entries": Sequence[AssociateClientDeviceWithCoreDeviceEntryTypeDef],
    },
    total=False,
)

class BatchAssociateClientDeviceWithCoreDeviceRequestRequestTypeDef(
    _RequiredBatchAssociateClientDeviceWithCoreDeviceRequestRequestTypeDef,
    _OptionalBatchAssociateClientDeviceWithCoreDeviceRequestRequestTypeDef,
):
    pass

BatchAssociateClientDeviceWithCoreDeviceResponseTypeDef = TypedDict(
    "BatchAssociateClientDeviceWithCoreDeviceResponseTypeDef",
    {
        "errorEntries": List[AssociateClientDeviceWithCoreDeviceErrorEntryTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListClientDevicesAssociatedWithCoreDeviceResponseTypeDef = TypedDict(
    "ListClientDevicesAssociatedWithCoreDeviceResponseTypeDef",
    {
        "associatedClientDevices": List[AssociatedClientDeviceTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredBatchDisassociateClientDeviceFromCoreDeviceRequestRequestTypeDef = TypedDict(
    "_RequiredBatchDisassociateClientDeviceFromCoreDeviceRequestRequestTypeDef",
    {
        "coreDeviceThingName": str,
    },
)
_OptionalBatchDisassociateClientDeviceFromCoreDeviceRequestRequestTypeDef = TypedDict(
    "_OptionalBatchDisassociateClientDeviceFromCoreDeviceRequestRequestTypeDef",
    {
        "entries": Sequence[DisassociateClientDeviceFromCoreDeviceEntryTypeDef],
    },
    total=False,
)

class BatchDisassociateClientDeviceFromCoreDeviceRequestRequestTypeDef(
    _RequiredBatchDisassociateClientDeviceFromCoreDeviceRequestRequestTypeDef,
    _OptionalBatchDisassociateClientDeviceFromCoreDeviceRequestRequestTypeDef,
):
    pass

BatchDisassociateClientDeviceFromCoreDeviceResponseTypeDef = TypedDict(
    "BatchDisassociateClientDeviceFromCoreDeviceResponseTypeDef",
    {
        "errorEntries": List[DisassociateClientDeviceFromCoreDeviceErrorEntryTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateComponentVersionResponseTypeDef = TypedDict(
    "CreateComponentVersionResponseTypeDef",
    {
        "arn": str,
        "componentName": str,
        "componentVersion": str,
        "creationTimestamp": datetime,
        "status": CloudComponentStatusTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ComponentLatestVersionTypeDef = TypedDict(
    "ComponentLatestVersionTypeDef",
    {
        "arn": str,
        "componentVersion": str,
        "creationTimestamp": datetime,
        "description": str,
        "publisher": str,
        "platforms": List[ComponentPlatformTypeDef],
    },
    total=False,
)

DescribeComponentResponseTypeDef = TypedDict(
    "DescribeComponentResponseTypeDef",
    {
        "arn": str,
        "componentName": str,
        "componentVersion": str,
        "creationTimestamp": datetime,
        "publisher": str,
        "description": str,
        "status": CloudComponentStatusTypeDef,
        "platforms": List[ComponentPlatformTypeDef],
        "tags": Dict[str, str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ResolveComponentCandidatesRequestRequestTypeDef = TypedDict(
    "ResolveComponentCandidatesRequestRequestTypeDef",
    {
        "platform": ComponentPlatformTypeDef,
        "componentCandidates": Sequence[ComponentCandidateTypeDef],
    },
    total=False,
)

ComponentRunWithTypeDef = TypedDict(
    "ComponentRunWithTypeDef",
    {
        "posixUser": str,
        "systemResourceLimits": SystemResourceLimitsTypeDef,
        "windowsUser": str,
    },
    total=False,
)

ListComponentVersionsResponseTypeDef = TypedDict(
    "ListComponentVersionsResponseTypeDef",
    {
        "componentVersions": List[ComponentVersionListItemTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetConnectivityInfoResponseTypeDef = TypedDict(
    "GetConnectivityInfoResponseTypeDef",
    {
        "connectivityInfo": List[ConnectivityInfoTypeDef],
        "message": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateConnectivityInfoRequestRequestTypeDef = TypedDict(
    "UpdateConnectivityInfoRequestRequestTypeDef",
    {
        "thingName": str,
        "connectivityInfo": Sequence[ConnectivityInfoTypeDef],
    },
)

ListCoreDevicesResponseTypeDef = TypedDict(
    "ListCoreDevicesResponseTypeDef",
    {
        "coreDevices": List[CoreDeviceTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeploymentPoliciesTypeDef = TypedDict(
    "DeploymentPoliciesTypeDef",
    {
        "failureHandlingPolicy": DeploymentFailureHandlingPolicyType,
        "componentUpdatePolicy": DeploymentComponentUpdatePolicyTypeDef,
        "configurationValidationPolicy": DeploymentConfigurationValidationPolicyTypeDef,
    },
    total=False,
)

ListDeploymentsResponseTypeDef = TypedDict(
    "ListDeploymentsResponseTypeDef",
    {
        "deployments": List[DeploymentTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredEffectiveDeploymentTypeDef = TypedDict(
    "_RequiredEffectiveDeploymentTypeDef",
    {
        "deploymentId": str,
        "deploymentName": str,
        "targetArn": str,
        "coreDeviceExecutionStatus": EffectiveDeploymentExecutionStatusType,
        "creationTimestamp": datetime,
        "modifiedTimestamp": datetime,
    },
)
_OptionalEffectiveDeploymentTypeDef = TypedDict(
    "_OptionalEffectiveDeploymentTypeDef",
    {
        "iotJobId": str,
        "iotJobArn": str,
        "description": str,
        "reason": str,
        "statusDetails": EffectiveDeploymentStatusDetailsTypeDef,
    },
    total=False,
)

class EffectiveDeploymentTypeDef(
    _RequiredEffectiveDeploymentTypeDef, _OptionalEffectiveDeploymentTypeDef
):
    pass

ListInstalledComponentsResponseTypeDef = TypedDict(
    "ListInstalledComponentsResponseTypeDef",
    {
        "installedComponents": List[InstalledComponentTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

IoTJobAbortConfigTypeDef = TypedDict(
    "IoTJobAbortConfigTypeDef",
    {
        "criteriaList": Sequence[IoTJobAbortCriteriaTypeDef],
    },
)

IoTJobExponentialRolloutRateTypeDef = TypedDict(
    "IoTJobExponentialRolloutRateTypeDef",
    {
        "baseRatePerMinute": int,
        "incrementFactor": float,
        "rateIncreaseCriteria": IoTJobRateIncreaseCriteriaTypeDef,
    },
)

LambdaContainerParamsTypeDef = TypedDict(
    "LambdaContainerParamsTypeDef",
    {
        "memorySizeInKB": int,
        "mountROSysfs": bool,
        "volumes": Sequence[LambdaVolumeMountTypeDef],
        "devices": Sequence[LambdaDeviceMountTypeDef],
    },
    total=False,
)

ResolveComponentCandidatesResponseTypeDef = TypedDict(
    "ResolveComponentCandidatesResponseTypeDef",
    {
        "resolvedComponentVersions": List[ResolvedComponentVersionTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ComponentTypeDef = TypedDict(
    "ComponentTypeDef",
    {
        "arn": str,
        "componentName": str,
        "latestVersion": ComponentLatestVersionTypeDef,
    },
    total=False,
)

ComponentDeploymentSpecificationTypeDef = TypedDict(
    "ComponentDeploymentSpecificationTypeDef",
    {
        "componentVersion": str,
        "configurationUpdate": ComponentConfigurationUpdateTypeDef,
        "runWith": ComponentRunWithTypeDef,
    },
    total=False,
)

ListEffectiveDeploymentsResponseTypeDef = TypedDict(
    "ListEffectiveDeploymentsResponseTypeDef",
    {
        "effectiveDeployments": List[EffectiveDeploymentTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

IoTJobExecutionsRolloutConfigTypeDef = TypedDict(
    "IoTJobExecutionsRolloutConfigTypeDef",
    {
        "exponentialRate": IoTJobExponentialRolloutRateTypeDef,
        "maximumPerMinute": int,
    },
    total=False,
)

LambdaLinuxProcessParamsTypeDef = TypedDict(
    "LambdaLinuxProcessParamsTypeDef",
    {
        "isolationMode": LambdaIsolationModeType,
        "containerParams": LambdaContainerParamsTypeDef,
    },
    total=False,
)

ListComponentsResponseTypeDef = TypedDict(
    "ListComponentsResponseTypeDef",
    {
        "components": List[ComponentTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeploymentIoTJobConfigurationTypeDef = TypedDict(
    "DeploymentIoTJobConfigurationTypeDef",
    {
        "jobExecutionsRolloutConfig": IoTJobExecutionsRolloutConfigTypeDef,
        "abortConfig": IoTJobAbortConfigTypeDef,
        "timeoutConfig": IoTJobTimeoutConfigTypeDef,
    },
    total=False,
)

LambdaExecutionParametersTypeDef = TypedDict(
    "LambdaExecutionParametersTypeDef",
    {
        "eventSources": Sequence[LambdaEventSourceTypeDef],
        "maxQueueSize": int,
        "maxInstancesCount": int,
        "maxIdleTimeInSeconds": int,
        "timeoutInSeconds": int,
        "statusTimeoutInSeconds": int,
        "pinned": bool,
        "inputPayloadEncodingType": LambdaInputPayloadEncodingTypeType,
        "execArgs": Sequence[str],
        "environmentVariables": Mapping[str, str],
        "linuxProcessParams": LambdaLinuxProcessParamsTypeDef,
    },
    total=False,
)

_RequiredCreateDeploymentRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDeploymentRequestRequestTypeDef",
    {
        "targetArn": str,
    },
)
_OptionalCreateDeploymentRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDeploymentRequestRequestTypeDef",
    {
        "deploymentName": str,
        "components": Mapping[str, ComponentDeploymentSpecificationTypeDef],
        "iotJobConfiguration": DeploymentIoTJobConfigurationTypeDef,
        "deploymentPolicies": DeploymentPoliciesTypeDef,
        "parentTargetArn": str,
        "tags": Mapping[str, str],
        "clientToken": str,
    },
    total=False,
)

class CreateDeploymentRequestRequestTypeDef(
    _RequiredCreateDeploymentRequestRequestTypeDef, _OptionalCreateDeploymentRequestRequestTypeDef
):
    pass

GetDeploymentResponseTypeDef = TypedDict(
    "GetDeploymentResponseTypeDef",
    {
        "targetArn": str,
        "revisionId": str,
        "deploymentId": str,
        "deploymentName": str,
        "deploymentStatus": DeploymentStatusType,
        "iotJobId": str,
        "iotJobArn": str,
        "components": Dict[str, ComponentDeploymentSpecificationTypeDef],
        "deploymentPolicies": DeploymentPoliciesTypeDef,
        "iotJobConfiguration": DeploymentIoTJobConfigurationTypeDef,
        "creationTimestamp": datetime,
        "isLatestForTarget": bool,
        "parentTargetArn": str,
        "tags": Dict[str, str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredLambdaFunctionRecipeSourceTypeDef = TypedDict(
    "_RequiredLambdaFunctionRecipeSourceTypeDef",
    {
        "lambdaArn": str,
    },
)
_OptionalLambdaFunctionRecipeSourceTypeDef = TypedDict(
    "_OptionalLambdaFunctionRecipeSourceTypeDef",
    {
        "componentName": str,
        "componentVersion": str,
        "componentPlatforms": Sequence[ComponentPlatformTypeDef],
        "componentDependencies": Mapping[str, ComponentDependencyRequirementTypeDef],
        "componentLambdaParameters": LambdaExecutionParametersTypeDef,
    },
    total=False,
)

class LambdaFunctionRecipeSourceTypeDef(
    _RequiredLambdaFunctionRecipeSourceTypeDef, _OptionalLambdaFunctionRecipeSourceTypeDef
):
    pass

CreateComponentVersionRequestRequestTypeDef = TypedDict(
    "CreateComponentVersionRequestRequestTypeDef",
    {
        "inlineRecipe": Union[str, bytes, IO[Any], StreamingBody],
        "lambdaFunction": LambdaFunctionRecipeSourceTypeDef,
        "tags": Mapping[str, str],
        "clientToken": str,
    },
    total=False,
)
