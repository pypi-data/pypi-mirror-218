"""
Type annotations for resource-groups service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resource_groups/type_defs/)

Usage::

    ```python
    from mypy_boto3_resource_groups.type_defs import AccountSettingsTypeDef

    data: AccountSettingsTypeDef = {...}
    ```
"""
import sys
from typing import Dict, List, Mapping, Sequence

from .literals import (
    GroupConfigurationStatusType,
    GroupFilterNameType,
    GroupLifecycleEventsDesiredStatusType,
    GroupLifecycleEventsStatusType,
    QueryErrorCodeType,
    QueryTypeType,
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
    "AccountSettingsTypeDef",
    "ResourceQueryTypeDef",
    "GroupTypeDef",
    "DeleteGroupInputRequestTypeDef",
    "FailedResourceTypeDef",
    "GetGroupConfigurationInputRequestTypeDef",
    "GetGroupInputRequestTypeDef",
    "GetGroupQueryInputRequestTypeDef",
    "GetTagsInputRequestTypeDef",
    "GetTagsOutputTypeDef",
    "GroupConfigurationParameterTypeDef",
    "GroupFilterTypeDef",
    "GroupIdentifierTypeDef",
    "GroupResourcesInputRequestTypeDef",
    "PendingResourceTypeDef",
    "ResourceFilterTypeDef",
    "ResourceIdentifierTypeDef",
    "ResourceStatusTypeDef",
    "QueryErrorTypeDef",
    "PaginatorConfigTypeDef",
    "ResponseMetadataTypeDef",
    "TagInputRequestTypeDef",
    "TagOutputTypeDef",
    "UngroupResourcesInputRequestTypeDef",
    "UntagInputRequestTypeDef",
    "UntagOutputTypeDef",
    "UpdateAccountSettingsInputRequestTypeDef",
    "UpdateGroupInputRequestTypeDef",
    "GetAccountSettingsOutputTypeDef",
    "UpdateAccountSettingsOutputTypeDef",
    "GroupQueryTypeDef",
    "SearchResourcesInputRequestTypeDef",
    "SearchResourcesInputSearchResourcesPaginateTypeDef",
    "UpdateGroupQueryInputRequestTypeDef",
    "DeleteGroupOutputTypeDef",
    "GetGroupOutputTypeDef",
    "UpdateGroupOutputTypeDef",
    "GroupConfigurationItemTypeDef",
    "ListGroupsInputListGroupsPaginateTypeDef",
    "ListGroupsInputRequestTypeDef",
    "ListGroupsOutputTypeDef",
    "GroupResourcesOutputTypeDef",
    "UngroupResourcesOutputTypeDef",
    "ListGroupResourcesInputListGroupResourcesPaginateTypeDef",
    "ListGroupResourcesInputRequestTypeDef",
    "ListGroupResourcesItemTypeDef",
    "SearchResourcesOutputTypeDef",
    "GetGroupQueryOutputTypeDef",
    "UpdateGroupQueryOutputTypeDef",
    "CreateGroupInputRequestTypeDef",
    "GroupConfigurationTypeDef",
    "PutGroupConfigurationInputRequestTypeDef",
    "ListGroupResourcesOutputTypeDef",
    "CreateGroupOutputTypeDef",
    "GetGroupConfigurationOutputTypeDef",
)

AccountSettingsTypeDef = TypedDict(
    "AccountSettingsTypeDef",
    {
        "GroupLifecycleEventsDesiredStatus": GroupLifecycleEventsDesiredStatusType,
        "GroupLifecycleEventsStatus": GroupLifecycleEventsStatusType,
        "GroupLifecycleEventsStatusMessage": str,
    },
    total=False,
)

ResourceQueryTypeDef = TypedDict(
    "ResourceQueryTypeDef",
    {
        "Type": QueryTypeType,
        "Query": str,
    },
)

_RequiredGroupTypeDef = TypedDict(
    "_RequiredGroupTypeDef",
    {
        "GroupArn": str,
        "Name": str,
    },
)
_OptionalGroupTypeDef = TypedDict(
    "_OptionalGroupTypeDef",
    {
        "Description": str,
    },
    total=False,
)


class GroupTypeDef(_RequiredGroupTypeDef, _OptionalGroupTypeDef):
    pass


DeleteGroupInputRequestTypeDef = TypedDict(
    "DeleteGroupInputRequestTypeDef",
    {
        "GroupName": str,
        "Group": str,
    },
    total=False,
)

FailedResourceTypeDef = TypedDict(
    "FailedResourceTypeDef",
    {
        "ResourceArn": str,
        "ErrorMessage": str,
        "ErrorCode": str,
    },
    total=False,
)

GetGroupConfigurationInputRequestTypeDef = TypedDict(
    "GetGroupConfigurationInputRequestTypeDef",
    {
        "Group": str,
    },
    total=False,
)

GetGroupInputRequestTypeDef = TypedDict(
    "GetGroupInputRequestTypeDef",
    {
        "GroupName": str,
        "Group": str,
    },
    total=False,
)

GetGroupQueryInputRequestTypeDef = TypedDict(
    "GetGroupQueryInputRequestTypeDef",
    {
        "GroupName": str,
        "Group": str,
    },
    total=False,
)

GetTagsInputRequestTypeDef = TypedDict(
    "GetTagsInputRequestTypeDef",
    {
        "Arn": str,
    },
)

GetTagsOutputTypeDef = TypedDict(
    "GetTagsOutputTypeDef",
    {
        "Arn": str,
        "Tags": Dict[str, str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredGroupConfigurationParameterTypeDef = TypedDict(
    "_RequiredGroupConfigurationParameterTypeDef",
    {
        "Name": str,
    },
)
_OptionalGroupConfigurationParameterTypeDef = TypedDict(
    "_OptionalGroupConfigurationParameterTypeDef",
    {
        "Values": Sequence[str],
    },
    total=False,
)


class GroupConfigurationParameterTypeDef(
    _RequiredGroupConfigurationParameterTypeDef, _OptionalGroupConfigurationParameterTypeDef
):
    pass


GroupFilterTypeDef = TypedDict(
    "GroupFilterTypeDef",
    {
        "Name": GroupFilterNameType,
        "Values": Sequence[str],
    },
)

GroupIdentifierTypeDef = TypedDict(
    "GroupIdentifierTypeDef",
    {
        "GroupName": str,
        "GroupArn": str,
    },
    total=False,
)

GroupResourcesInputRequestTypeDef = TypedDict(
    "GroupResourcesInputRequestTypeDef",
    {
        "Group": str,
        "ResourceArns": Sequence[str],
    },
)

PendingResourceTypeDef = TypedDict(
    "PendingResourceTypeDef",
    {
        "ResourceArn": str,
    },
    total=False,
)

ResourceFilterTypeDef = TypedDict(
    "ResourceFilterTypeDef",
    {
        "Name": Literal["resource-type"],
        "Values": Sequence[str],
    },
)

ResourceIdentifierTypeDef = TypedDict(
    "ResourceIdentifierTypeDef",
    {
        "ResourceArn": str,
        "ResourceType": str,
    },
    total=False,
)

ResourceStatusTypeDef = TypedDict(
    "ResourceStatusTypeDef",
    {
        "Name": Literal["PENDING"],
    },
    total=False,
)

QueryErrorTypeDef = TypedDict(
    "QueryErrorTypeDef",
    {
        "ErrorCode": QueryErrorCodeType,
        "Message": str,
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

TagInputRequestTypeDef = TypedDict(
    "TagInputRequestTypeDef",
    {
        "Arn": str,
        "Tags": Mapping[str, str],
    },
)

TagOutputTypeDef = TypedDict(
    "TagOutputTypeDef",
    {
        "Arn": str,
        "Tags": Dict[str, str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UngroupResourcesInputRequestTypeDef = TypedDict(
    "UngroupResourcesInputRequestTypeDef",
    {
        "Group": str,
        "ResourceArns": Sequence[str],
    },
)

UntagInputRequestTypeDef = TypedDict(
    "UntagInputRequestTypeDef",
    {
        "Arn": str,
        "Keys": Sequence[str],
    },
)

UntagOutputTypeDef = TypedDict(
    "UntagOutputTypeDef",
    {
        "Arn": str,
        "Keys": List[str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateAccountSettingsInputRequestTypeDef = TypedDict(
    "UpdateAccountSettingsInputRequestTypeDef",
    {
        "GroupLifecycleEventsDesiredStatus": GroupLifecycleEventsDesiredStatusType,
    },
    total=False,
)

UpdateGroupInputRequestTypeDef = TypedDict(
    "UpdateGroupInputRequestTypeDef",
    {
        "GroupName": str,
        "Group": str,
        "Description": str,
    },
    total=False,
)

GetAccountSettingsOutputTypeDef = TypedDict(
    "GetAccountSettingsOutputTypeDef",
    {
        "AccountSettings": AccountSettingsTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateAccountSettingsOutputTypeDef = TypedDict(
    "UpdateAccountSettingsOutputTypeDef",
    {
        "AccountSettings": AccountSettingsTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GroupQueryTypeDef = TypedDict(
    "GroupQueryTypeDef",
    {
        "GroupName": str,
        "ResourceQuery": ResourceQueryTypeDef,
    },
)

_RequiredSearchResourcesInputRequestTypeDef = TypedDict(
    "_RequiredSearchResourcesInputRequestTypeDef",
    {
        "ResourceQuery": ResourceQueryTypeDef,
    },
)
_OptionalSearchResourcesInputRequestTypeDef = TypedDict(
    "_OptionalSearchResourcesInputRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class SearchResourcesInputRequestTypeDef(
    _RequiredSearchResourcesInputRequestTypeDef, _OptionalSearchResourcesInputRequestTypeDef
):
    pass


_RequiredSearchResourcesInputSearchResourcesPaginateTypeDef = TypedDict(
    "_RequiredSearchResourcesInputSearchResourcesPaginateTypeDef",
    {
        "ResourceQuery": ResourceQueryTypeDef,
    },
)
_OptionalSearchResourcesInputSearchResourcesPaginateTypeDef = TypedDict(
    "_OptionalSearchResourcesInputSearchResourcesPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class SearchResourcesInputSearchResourcesPaginateTypeDef(
    _RequiredSearchResourcesInputSearchResourcesPaginateTypeDef,
    _OptionalSearchResourcesInputSearchResourcesPaginateTypeDef,
):
    pass


_RequiredUpdateGroupQueryInputRequestTypeDef = TypedDict(
    "_RequiredUpdateGroupQueryInputRequestTypeDef",
    {
        "ResourceQuery": ResourceQueryTypeDef,
    },
)
_OptionalUpdateGroupQueryInputRequestTypeDef = TypedDict(
    "_OptionalUpdateGroupQueryInputRequestTypeDef",
    {
        "GroupName": str,
        "Group": str,
    },
    total=False,
)


class UpdateGroupQueryInputRequestTypeDef(
    _RequiredUpdateGroupQueryInputRequestTypeDef, _OptionalUpdateGroupQueryInputRequestTypeDef
):
    pass


DeleteGroupOutputTypeDef = TypedDict(
    "DeleteGroupOutputTypeDef",
    {
        "Group": GroupTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetGroupOutputTypeDef = TypedDict(
    "GetGroupOutputTypeDef",
    {
        "Group": GroupTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateGroupOutputTypeDef = TypedDict(
    "UpdateGroupOutputTypeDef",
    {
        "Group": GroupTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredGroupConfigurationItemTypeDef = TypedDict(
    "_RequiredGroupConfigurationItemTypeDef",
    {
        "Type": str,
    },
)
_OptionalGroupConfigurationItemTypeDef = TypedDict(
    "_OptionalGroupConfigurationItemTypeDef",
    {
        "Parameters": Sequence[GroupConfigurationParameterTypeDef],
    },
    total=False,
)


class GroupConfigurationItemTypeDef(
    _RequiredGroupConfigurationItemTypeDef, _OptionalGroupConfigurationItemTypeDef
):
    pass


ListGroupsInputListGroupsPaginateTypeDef = TypedDict(
    "ListGroupsInputListGroupsPaginateTypeDef",
    {
        "Filters": Sequence[GroupFilterTypeDef],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListGroupsInputRequestTypeDef = TypedDict(
    "ListGroupsInputRequestTypeDef",
    {
        "Filters": Sequence[GroupFilterTypeDef],
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListGroupsOutputTypeDef = TypedDict(
    "ListGroupsOutputTypeDef",
    {
        "GroupIdentifiers": List[GroupIdentifierTypeDef],
        "Groups": List[GroupTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GroupResourcesOutputTypeDef = TypedDict(
    "GroupResourcesOutputTypeDef",
    {
        "Succeeded": List[str],
        "Failed": List[FailedResourceTypeDef],
        "Pending": List[PendingResourceTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UngroupResourcesOutputTypeDef = TypedDict(
    "UngroupResourcesOutputTypeDef",
    {
        "Succeeded": List[str],
        "Failed": List[FailedResourceTypeDef],
        "Pending": List[PendingResourceTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListGroupResourcesInputListGroupResourcesPaginateTypeDef = TypedDict(
    "ListGroupResourcesInputListGroupResourcesPaginateTypeDef",
    {
        "GroupName": str,
        "Group": str,
        "Filters": Sequence[ResourceFilterTypeDef],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListGroupResourcesInputRequestTypeDef = TypedDict(
    "ListGroupResourcesInputRequestTypeDef",
    {
        "GroupName": str,
        "Group": str,
        "Filters": Sequence[ResourceFilterTypeDef],
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListGroupResourcesItemTypeDef = TypedDict(
    "ListGroupResourcesItemTypeDef",
    {
        "Identifier": ResourceIdentifierTypeDef,
        "Status": ResourceStatusTypeDef,
    },
    total=False,
)

SearchResourcesOutputTypeDef = TypedDict(
    "SearchResourcesOutputTypeDef",
    {
        "ResourceIdentifiers": List[ResourceIdentifierTypeDef],
        "NextToken": str,
        "QueryErrors": List[QueryErrorTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetGroupQueryOutputTypeDef = TypedDict(
    "GetGroupQueryOutputTypeDef",
    {
        "GroupQuery": GroupQueryTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateGroupQueryOutputTypeDef = TypedDict(
    "UpdateGroupQueryOutputTypeDef",
    {
        "GroupQuery": GroupQueryTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateGroupInputRequestTypeDef = TypedDict(
    "_RequiredCreateGroupInputRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalCreateGroupInputRequestTypeDef = TypedDict(
    "_OptionalCreateGroupInputRequestTypeDef",
    {
        "Description": str,
        "ResourceQuery": ResourceQueryTypeDef,
        "Tags": Mapping[str, str],
        "Configuration": Sequence[GroupConfigurationItemTypeDef],
    },
    total=False,
)


class CreateGroupInputRequestTypeDef(
    _RequiredCreateGroupInputRequestTypeDef, _OptionalCreateGroupInputRequestTypeDef
):
    pass


GroupConfigurationTypeDef = TypedDict(
    "GroupConfigurationTypeDef",
    {
        "Configuration": List[GroupConfigurationItemTypeDef],
        "ProposedConfiguration": List[GroupConfigurationItemTypeDef],
        "Status": GroupConfigurationStatusType,
        "FailureReason": str,
    },
    total=False,
)

PutGroupConfigurationInputRequestTypeDef = TypedDict(
    "PutGroupConfigurationInputRequestTypeDef",
    {
        "Group": str,
        "Configuration": Sequence[GroupConfigurationItemTypeDef],
    },
    total=False,
)

ListGroupResourcesOutputTypeDef = TypedDict(
    "ListGroupResourcesOutputTypeDef",
    {
        "Resources": List[ListGroupResourcesItemTypeDef],
        "ResourceIdentifiers": List[ResourceIdentifierTypeDef],
        "NextToken": str,
        "QueryErrors": List[QueryErrorTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateGroupOutputTypeDef = TypedDict(
    "CreateGroupOutputTypeDef",
    {
        "Group": GroupTypeDef,
        "ResourceQuery": ResourceQueryTypeDef,
        "Tags": Dict[str, str],
        "GroupConfiguration": GroupConfigurationTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetGroupConfigurationOutputTypeDef = TypedDict(
    "GetGroupConfigurationOutputTypeDef",
    {
        "GroupConfiguration": GroupConfigurationTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)
