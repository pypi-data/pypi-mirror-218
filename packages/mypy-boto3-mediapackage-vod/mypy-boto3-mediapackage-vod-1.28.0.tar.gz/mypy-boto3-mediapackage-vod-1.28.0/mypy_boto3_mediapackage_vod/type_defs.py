"""
Type annotations for mediapackage-vod service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediapackage_vod/type_defs/)

Usage::

    ```python
    from mypy_boto3_mediapackage_vod.type_defs import AssetShallowTypeDef

    data: AssetShallowTypeDef = {...}
    ```
"""
import sys
from typing import Dict, List, Mapping, Sequence

from .literals import (
    AdMarkersType,
    EncryptionMethodType,
    ManifestLayoutType,
    PresetSpeke20AudioType,
    PresetSpeke20VideoType,
    ProfileType,
    ScteMarkersSourceType,
    SegmentTemplateFormatType,
    StreamOrderType,
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
    "AssetShallowTypeDef",
    "AuthorizationTypeDef",
    "EgressAccessLogsTypeDef",
    "CreateAssetRequestRequestTypeDef",
    "EgressEndpointTypeDef",
    "StreamSelectionTypeDef",
    "DeleteAssetRequestRequestTypeDef",
    "DeletePackagingConfigurationRequestRequestTypeDef",
    "DeletePackagingGroupRequestRequestTypeDef",
    "DescribeAssetRequestRequestTypeDef",
    "DescribePackagingConfigurationRequestRequestTypeDef",
    "DescribePackagingGroupRequestRequestTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EncryptionContractConfigurationTypeDef",
    "ListAssetsRequestListAssetsPaginateTypeDef",
    "ListAssetsRequestRequestTypeDef",
    "ListPackagingConfigurationsRequestListPackagingConfigurationsPaginateTypeDef",
    "ListPackagingConfigurationsRequestRequestTypeDef",
    "ListPackagingGroupsRequestListPackagingGroupsPaginateTypeDef",
    "ListPackagingGroupsRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PaginatorConfigTypeDef",
    "ResponseMetadataTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "ListAssetsResponseTypeDef",
    "UpdatePackagingGroupRequestRequestTypeDef",
    "ConfigureLogsRequestRequestTypeDef",
    "ConfigureLogsResponseTypeDef",
    "CreatePackagingGroupRequestRequestTypeDef",
    "CreatePackagingGroupResponseTypeDef",
    "DescribePackagingGroupResponseTypeDef",
    "PackagingGroupTypeDef",
    "UpdatePackagingGroupResponseTypeDef",
    "CreateAssetResponseTypeDef",
    "DescribeAssetResponseTypeDef",
    "DashManifestTypeDef",
    "HlsManifestTypeDef",
    "MssManifestTypeDef",
    "SpekeKeyProviderTypeDef",
    "ListPackagingGroupsResponseTypeDef",
    "CmafEncryptionTypeDef",
    "DashEncryptionTypeDef",
    "HlsEncryptionTypeDef",
    "MssEncryptionTypeDef",
    "CmafPackageTypeDef",
    "DashPackageTypeDef",
    "HlsPackageTypeDef",
    "MssPackageTypeDef",
    "CreatePackagingConfigurationRequestRequestTypeDef",
    "CreatePackagingConfigurationResponseTypeDef",
    "DescribePackagingConfigurationResponseTypeDef",
    "PackagingConfigurationTypeDef",
    "ListPackagingConfigurationsResponseTypeDef",
)

AssetShallowTypeDef = TypedDict(
    "AssetShallowTypeDef",
    {
        "Arn": str,
        "CreatedAt": str,
        "Id": str,
        "PackagingGroupId": str,
        "ResourceId": str,
        "SourceArn": str,
        "SourceRoleArn": str,
        "Tags": Dict[str, str],
    },
    total=False,
)

AuthorizationTypeDef = TypedDict(
    "AuthorizationTypeDef",
    {
        "CdnIdentifierSecret": str,
        "SecretsRoleArn": str,
    },
)

EgressAccessLogsTypeDef = TypedDict(
    "EgressAccessLogsTypeDef",
    {
        "LogGroupName": str,
    },
    total=False,
)

_RequiredCreateAssetRequestRequestTypeDef = TypedDict(
    "_RequiredCreateAssetRequestRequestTypeDef",
    {
        "Id": str,
        "PackagingGroupId": str,
        "SourceArn": str,
        "SourceRoleArn": str,
    },
)
_OptionalCreateAssetRequestRequestTypeDef = TypedDict(
    "_OptionalCreateAssetRequestRequestTypeDef",
    {
        "ResourceId": str,
        "Tags": Mapping[str, str],
    },
    total=False,
)


class CreateAssetRequestRequestTypeDef(
    _RequiredCreateAssetRequestRequestTypeDef, _OptionalCreateAssetRequestRequestTypeDef
):
    pass


EgressEndpointTypeDef = TypedDict(
    "EgressEndpointTypeDef",
    {
        "PackagingConfigurationId": str,
        "Status": str,
        "Url": str,
    },
    total=False,
)

StreamSelectionTypeDef = TypedDict(
    "StreamSelectionTypeDef",
    {
        "MaxVideoBitsPerSecond": int,
        "MinVideoBitsPerSecond": int,
        "StreamOrder": StreamOrderType,
    },
    total=False,
)

DeleteAssetRequestRequestTypeDef = TypedDict(
    "DeleteAssetRequestRequestTypeDef",
    {
        "Id": str,
    },
)

DeletePackagingConfigurationRequestRequestTypeDef = TypedDict(
    "DeletePackagingConfigurationRequestRequestTypeDef",
    {
        "Id": str,
    },
)

DeletePackagingGroupRequestRequestTypeDef = TypedDict(
    "DeletePackagingGroupRequestRequestTypeDef",
    {
        "Id": str,
    },
)

DescribeAssetRequestRequestTypeDef = TypedDict(
    "DescribeAssetRequestRequestTypeDef",
    {
        "Id": str,
    },
)

DescribePackagingConfigurationRequestRequestTypeDef = TypedDict(
    "DescribePackagingConfigurationRequestRequestTypeDef",
    {
        "Id": str,
    },
)

DescribePackagingGroupRequestRequestTypeDef = TypedDict(
    "DescribePackagingGroupRequestRequestTypeDef",
    {
        "Id": str,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

EncryptionContractConfigurationTypeDef = TypedDict(
    "EncryptionContractConfigurationTypeDef",
    {
        "PresetSpeke20Audio": PresetSpeke20AudioType,
        "PresetSpeke20Video": PresetSpeke20VideoType,
    },
)

ListAssetsRequestListAssetsPaginateTypeDef = TypedDict(
    "ListAssetsRequestListAssetsPaginateTypeDef",
    {
        "PackagingGroupId": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListAssetsRequestRequestTypeDef = TypedDict(
    "ListAssetsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
        "PackagingGroupId": str,
    },
    total=False,
)

ListPackagingConfigurationsRequestListPackagingConfigurationsPaginateTypeDef = TypedDict(
    "ListPackagingConfigurationsRequestListPackagingConfigurationsPaginateTypeDef",
    {
        "PackagingGroupId": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListPackagingConfigurationsRequestRequestTypeDef = TypedDict(
    "ListPackagingConfigurationsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
        "PackagingGroupId": str,
    },
    total=False,
)

ListPackagingGroupsRequestListPackagingGroupsPaginateTypeDef = TypedDict(
    "ListPackagingGroupsRequestListPackagingGroupsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListPackagingGroupsRequestRequestTypeDef = TypedDict(
    "ListPackagingGroupsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
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
        "ResourceArn": str,
        "Tags": Mapping[str, str],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)

ListAssetsResponseTypeDef = TypedDict(
    "ListAssetsResponseTypeDef",
    {
        "Assets": List[AssetShallowTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredUpdatePackagingGroupRequestRequestTypeDef = TypedDict(
    "_RequiredUpdatePackagingGroupRequestRequestTypeDef",
    {
        "Id": str,
    },
)
_OptionalUpdatePackagingGroupRequestRequestTypeDef = TypedDict(
    "_OptionalUpdatePackagingGroupRequestRequestTypeDef",
    {
        "Authorization": AuthorizationTypeDef,
    },
    total=False,
)


class UpdatePackagingGroupRequestRequestTypeDef(
    _RequiredUpdatePackagingGroupRequestRequestTypeDef,
    _OptionalUpdatePackagingGroupRequestRequestTypeDef,
):
    pass


_RequiredConfigureLogsRequestRequestTypeDef = TypedDict(
    "_RequiredConfigureLogsRequestRequestTypeDef",
    {
        "Id": str,
    },
)
_OptionalConfigureLogsRequestRequestTypeDef = TypedDict(
    "_OptionalConfigureLogsRequestRequestTypeDef",
    {
        "EgressAccessLogs": EgressAccessLogsTypeDef,
    },
    total=False,
)


class ConfigureLogsRequestRequestTypeDef(
    _RequiredConfigureLogsRequestRequestTypeDef, _OptionalConfigureLogsRequestRequestTypeDef
):
    pass


ConfigureLogsResponseTypeDef = TypedDict(
    "ConfigureLogsResponseTypeDef",
    {
        "Arn": str,
        "Authorization": AuthorizationTypeDef,
        "CreatedAt": str,
        "DomainName": str,
        "EgressAccessLogs": EgressAccessLogsTypeDef,
        "Id": str,
        "Tags": Dict[str, str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreatePackagingGroupRequestRequestTypeDef = TypedDict(
    "_RequiredCreatePackagingGroupRequestRequestTypeDef",
    {
        "Id": str,
    },
)
_OptionalCreatePackagingGroupRequestRequestTypeDef = TypedDict(
    "_OptionalCreatePackagingGroupRequestRequestTypeDef",
    {
        "Authorization": AuthorizationTypeDef,
        "EgressAccessLogs": EgressAccessLogsTypeDef,
        "Tags": Mapping[str, str],
    },
    total=False,
)


class CreatePackagingGroupRequestRequestTypeDef(
    _RequiredCreatePackagingGroupRequestRequestTypeDef,
    _OptionalCreatePackagingGroupRequestRequestTypeDef,
):
    pass


CreatePackagingGroupResponseTypeDef = TypedDict(
    "CreatePackagingGroupResponseTypeDef",
    {
        "Arn": str,
        "Authorization": AuthorizationTypeDef,
        "CreatedAt": str,
        "DomainName": str,
        "EgressAccessLogs": EgressAccessLogsTypeDef,
        "Id": str,
        "Tags": Dict[str, str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribePackagingGroupResponseTypeDef = TypedDict(
    "DescribePackagingGroupResponseTypeDef",
    {
        "ApproximateAssetCount": int,
        "Arn": str,
        "Authorization": AuthorizationTypeDef,
        "CreatedAt": str,
        "DomainName": str,
        "EgressAccessLogs": EgressAccessLogsTypeDef,
        "Id": str,
        "Tags": Dict[str, str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

PackagingGroupTypeDef = TypedDict(
    "PackagingGroupTypeDef",
    {
        "ApproximateAssetCount": int,
        "Arn": str,
        "Authorization": AuthorizationTypeDef,
        "CreatedAt": str,
        "DomainName": str,
        "EgressAccessLogs": EgressAccessLogsTypeDef,
        "Id": str,
        "Tags": Dict[str, str],
    },
    total=False,
)

UpdatePackagingGroupResponseTypeDef = TypedDict(
    "UpdatePackagingGroupResponseTypeDef",
    {
        "ApproximateAssetCount": int,
        "Arn": str,
        "Authorization": AuthorizationTypeDef,
        "CreatedAt": str,
        "DomainName": str,
        "EgressAccessLogs": EgressAccessLogsTypeDef,
        "Id": str,
        "Tags": Dict[str, str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateAssetResponseTypeDef = TypedDict(
    "CreateAssetResponseTypeDef",
    {
        "Arn": str,
        "CreatedAt": str,
        "EgressEndpoints": List[EgressEndpointTypeDef],
        "Id": str,
        "PackagingGroupId": str,
        "ResourceId": str,
        "SourceArn": str,
        "SourceRoleArn": str,
        "Tags": Dict[str, str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeAssetResponseTypeDef = TypedDict(
    "DescribeAssetResponseTypeDef",
    {
        "Arn": str,
        "CreatedAt": str,
        "EgressEndpoints": List[EgressEndpointTypeDef],
        "Id": str,
        "PackagingGroupId": str,
        "ResourceId": str,
        "SourceArn": str,
        "SourceRoleArn": str,
        "Tags": Dict[str, str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DashManifestTypeDef = TypedDict(
    "DashManifestTypeDef",
    {
        "ManifestLayout": ManifestLayoutType,
        "ManifestName": str,
        "MinBufferTimeSeconds": int,
        "Profile": ProfileType,
        "ScteMarkersSource": ScteMarkersSourceType,
        "StreamSelection": StreamSelectionTypeDef,
    },
    total=False,
)

HlsManifestTypeDef = TypedDict(
    "HlsManifestTypeDef",
    {
        "AdMarkers": AdMarkersType,
        "IncludeIframeOnlyStream": bool,
        "ManifestName": str,
        "ProgramDateTimeIntervalSeconds": int,
        "RepeatExtXKey": bool,
        "StreamSelection": StreamSelectionTypeDef,
    },
    total=False,
)

MssManifestTypeDef = TypedDict(
    "MssManifestTypeDef",
    {
        "ManifestName": str,
        "StreamSelection": StreamSelectionTypeDef,
    },
    total=False,
)

_RequiredSpekeKeyProviderTypeDef = TypedDict(
    "_RequiredSpekeKeyProviderTypeDef",
    {
        "RoleArn": str,
        "SystemIds": Sequence[str],
        "Url": str,
    },
)
_OptionalSpekeKeyProviderTypeDef = TypedDict(
    "_OptionalSpekeKeyProviderTypeDef",
    {
        "EncryptionContractConfiguration": EncryptionContractConfigurationTypeDef,
    },
    total=False,
)


class SpekeKeyProviderTypeDef(_RequiredSpekeKeyProviderTypeDef, _OptionalSpekeKeyProviderTypeDef):
    pass


ListPackagingGroupsResponseTypeDef = TypedDict(
    "ListPackagingGroupsResponseTypeDef",
    {
        "NextToken": str,
        "PackagingGroups": List[PackagingGroupTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCmafEncryptionTypeDef = TypedDict(
    "_RequiredCmafEncryptionTypeDef",
    {
        "SpekeKeyProvider": SpekeKeyProviderTypeDef,
    },
)
_OptionalCmafEncryptionTypeDef = TypedDict(
    "_OptionalCmafEncryptionTypeDef",
    {
        "ConstantInitializationVector": str,
    },
    total=False,
)


class CmafEncryptionTypeDef(_RequiredCmafEncryptionTypeDef, _OptionalCmafEncryptionTypeDef):
    pass


DashEncryptionTypeDef = TypedDict(
    "DashEncryptionTypeDef",
    {
        "SpekeKeyProvider": SpekeKeyProviderTypeDef,
    },
)

_RequiredHlsEncryptionTypeDef = TypedDict(
    "_RequiredHlsEncryptionTypeDef",
    {
        "SpekeKeyProvider": SpekeKeyProviderTypeDef,
    },
)
_OptionalHlsEncryptionTypeDef = TypedDict(
    "_OptionalHlsEncryptionTypeDef",
    {
        "ConstantInitializationVector": str,
        "EncryptionMethod": EncryptionMethodType,
    },
    total=False,
)


class HlsEncryptionTypeDef(_RequiredHlsEncryptionTypeDef, _OptionalHlsEncryptionTypeDef):
    pass


MssEncryptionTypeDef = TypedDict(
    "MssEncryptionTypeDef",
    {
        "SpekeKeyProvider": SpekeKeyProviderTypeDef,
    },
)

_RequiredCmafPackageTypeDef = TypedDict(
    "_RequiredCmafPackageTypeDef",
    {
        "HlsManifests": Sequence[HlsManifestTypeDef],
    },
)
_OptionalCmafPackageTypeDef = TypedDict(
    "_OptionalCmafPackageTypeDef",
    {
        "Encryption": CmafEncryptionTypeDef,
        "IncludeEncoderConfigurationInSegments": bool,
        "SegmentDurationSeconds": int,
    },
    total=False,
)


class CmafPackageTypeDef(_RequiredCmafPackageTypeDef, _OptionalCmafPackageTypeDef):
    pass


_RequiredDashPackageTypeDef = TypedDict(
    "_RequiredDashPackageTypeDef",
    {
        "DashManifests": Sequence[DashManifestTypeDef],
    },
)
_OptionalDashPackageTypeDef = TypedDict(
    "_OptionalDashPackageTypeDef",
    {
        "Encryption": DashEncryptionTypeDef,
        "IncludeEncoderConfigurationInSegments": bool,
        "IncludeIframeOnlyStream": bool,
        "PeriodTriggers": Sequence[Literal["ADS"]],
        "SegmentDurationSeconds": int,
        "SegmentTemplateFormat": SegmentTemplateFormatType,
    },
    total=False,
)


class DashPackageTypeDef(_RequiredDashPackageTypeDef, _OptionalDashPackageTypeDef):
    pass


_RequiredHlsPackageTypeDef = TypedDict(
    "_RequiredHlsPackageTypeDef",
    {
        "HlsManifests": Sequence[HlsManifestTypeDef],
    },
)
_OptionalHlsPackageTypeDef = TypedDict(
    "_OptionalHlsPackageTypeDef",
    {
        "Encryption": HlsEncryptionTypeDef,
        "IncludeDvbSubtitles": bool,
        "SegmentDurationSeconds": int,
        "UseAudioRenditionGroup": bool,
    },
    total=False,
)


class HlsPackageTypeDef(_RequiredHlsPackageTypeDef, _OptionalHlsPackageTypeDef):
    pass


_RequiredMssPackageTypeDef = TypedDict(
    "_RequiredMssPackageTypeDef",
    {
        "MssManifests": Sequence[MssManifestTypeDef],
    },
)
_OptionalMssPackageTypeDef = TypedDict(
    "_OptionalMssPackageTypeDef",
    {
        "Encryption": MssEncryptionTypeDef,
        "SegmentDurationSeconds": int,
    },
    total=False,
)


class MssPackageTypeDef(_RequiredMssPackageTypeDef, _OptionalMssPackageTypeDef):
    pass


_RequiredCreatePackagingConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredCreatePackagingConfigurationRequestRequestTypeDef",
    {
        "Id": str,
        "PackagingGroupId": str,
    },
)
_OptionalCreatePackagingConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalCreatePackagingConfigurationRequestRequestTypeDef",
    {
        "CmafPackage": CmafPackageTypeDef,
        "DashPackage": DashPackageTypeDef,
        "HlsPackage": HlsPackageTypeDef,
        "MssPackage": MssPackageTypeDef,
        "Tags": Mapping[str, str],
    },
    total=False,
)


class CreatePackagingConfigurationRequestRequestTypeDef(
    _RequiredCreatePackagingConfigurationRequestRequestTypeDef,
    _OptionalCreatePackagingConfigurationRequestRequestTypeDef,
):
    pass


CreatePackagingConfigurationResponseTypeDef = TypedDict(
    "CreatePackagingConfigurationResponseTypeDef",
    {
        "Arn": str,
        "CmafPackage": CmafPackageTypeDef,
        "CreatedAt": str,
        "DashPackage": DashPackageTypeDef,
        "HlsPackage": HlsPackageTypeDef,
        "Id": str,
        "MssPackage": MssPackageTypeDef,
        "PackagingGroupId": str,
        "Tags": Dict[str, str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribePackagingConfigurationResponseTypeDef = TypedDict(
    "DescribePackagingConfigurationResponseTypeDef",
    {
        "Arn": str,
        "CmafPackage": CmafPackageTypeDef,
        "CreatedAt": str,
        "DashPackage": DashPackageTypeDef,
        "HlsPackage": HlsPackageTypeDef,
        "Id": str,
        "MssPackage": MssPackageTypeDef,
        "PackagingGroupId": str,
        "Tags": Dict[str, str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

PackagingConfigurationTypeDef = TypedDict(
    "PackagingConfigurationTypeDef",
    {
        "Arn": str,
        "CmafPackage": CmafPackageTypeDef,
        "CreatedAt": str,
        "DashPackage": DashPackageTypeDef,
        "HlsPackage": HlsPackageTypeDef,
        "Id": str,
        "MssPackage": MssPackageTypeDef,
        "PackagingGroupId": str,
        "Tags": Dict[str, str],
    },
    total=False,
)

ListPackagingConfigurationsResponseTypeDef = TypedDict(
    "ListPackagingConfigurationsResponseTypeDef",
    {
        "NextToken": str,
        "PackagingConfigurations": List[PackagingConfigurationTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)
