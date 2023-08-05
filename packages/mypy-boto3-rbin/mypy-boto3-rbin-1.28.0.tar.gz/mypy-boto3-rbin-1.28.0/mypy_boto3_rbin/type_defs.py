"""
Type annotations for rbin service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rbin/type_defs/)

Usage::

    ```python
    from mypy_boto3_rbin.type_defs import ResourceTagTypeDef

    data: ResourceTagTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence

from .literals import LockStateType, ResourceTypeType, RuleStatusType

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "ResourceTagTypeDef",
    "RetentionPeriodTypeDef",
    "TagTypeDef",
    "DeleteRuleRequestRequestTypeDef",
    "GetRuleRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "UnlockDelayTypeDef",
    "PaginatorConfigTypeDef",
    "ResponseMetadataTypeDef",
    "UnlockRuleRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "ListRulesRequestListRulesPaginateTypeDef",
    "ListRulesRequestRequestTypeDef",
    "RuleSummaryTypeDef",
    "UpdateRuleRequestRequestTypeDef",
    "UpdateRuleResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "LockConfigurationTypeDef",
    "ListRulesResponseTypeDef",
    "CreateRuleRequestRequestTypeDef",
    "CreateRuleResponseTypeDef",
    "GetRuleResponseTypeDef",
    "LockRuleRequestRequestTypeDef",
    "LockRuleResponseTypeDef",
    "UnlockRuleResponseTypeDef",
)

_RequiredResourceTagTypeDef = TypedDict(
    "_RequiredResourceTagTypeDef",
    {
        "ResourceTagKey": str,
    },
)
_OptionalResourceTagTypeDef = TypedDict(
    "_OptionalResourceTagTypeDef",
    {
        "ResourceTagValue": str,
    },
    total=False,
)


class ResourceTagTypeDef(_RequiredResourceTagTypeDef, _OptionalResourceTagTypeDef):
    pass


RetentionPeriodTypeDef = TypedDict(
    "RetentionPeriodTypeDef",
    {
        "RetentionPeriodValue": int,
        "RetentionPeriodUnit": Literal["DAYS"],
    },
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

DeleteRuleRequestRequestTypeDef = TypedDict(
    "DeleteRuleRequestRequestTypeDef",
    {
        "Identifier": str,
    },
)

GetRuleRequestRequestTypeDef = TypedDict(
    "GetRuleRequestRequestTypeDef",
    {
        "Identifier": str,
    },
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

UnlockDelayTypeDef = TypedDict(
    "UnlockDelayTypeDef",
    {
        "UnlockDelayValue": int,
        "UnlockDelayUnit": Literal["DAYS"],
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

UnlockRuleRequestRequestTypeDef = TypedDict(
    "UnlockRuleRequestRequestTypeDef",
    {
        "Identifier": str,
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)

_RequiredListRulesRequestListRulesPaginateTypeDef = TypedDict(
    "_RequiredListRulesRequestListRulesPaginateTypeDef",
    {
        "ResourceType": ResourceTypeType,
    },
)
_OptionalListRulesRequestListRulesPaginateTypeDef = TypedDict(
    "_OptionalListRulesRequestListRulesPaginateTypeDef",
    {
        "ResourceTags": Sequence[ResourceTagTypeDef],
        "LockState": LockStateType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListRulesRequestListRulesPaginateTypeDef(
    _RequiredListRulesRequestListRulesPaginateTypeDef,
    _OptionalListRulesRequestListRulesPaginateTypeDef,
):
    pass


_RequiredListRulesRequestRequestTypeDef = TypedDict(
    "_RequiredListRulesRequestRequestTypeDef",
    {
        "ResourceType": ResourceTypeType,
    },
)
_OptionalListRulesRequestRequestTypeDef = TypedDict(
    "_OptionalListRulesRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
        "ResourceTags": Sequence[ResourceTagTypeDef],
        "LockState": LockStateType,
    },
    total=False,
)


class ListRulesRequestRequestTypeDef(
    _RequiredListRulesRequestRequestTypeDef, _OptionalListRulesRequestRequestTypeDef
):
    pass


RuleSummaryTypeDef = TypedDict(
    "RuleSummaryTypeDef",
    {
        "Identifier": str,
        "Description": str,
        "RetentionPeriod": RetentionPeriodTypeDef,
        "LockState": LockStateType,
    },
    total=False,
)

_RequiredUpdateRuleRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateRuleRequestRequestTypeDef",
    {
        "Identifier": str,
    },
)
_OptionalUpdateRuleRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateRuleRequestRequestTypeDef",
    {
        "RetentionPeriod": RetentionPeriodTypeDef,
        "Description": str,
        "ResourceType": ResourceTypeType,
        "ResourceTags": Sequence[ResourceTagTypeDef],
    },
    total=False,
)


class UpdateRuleRequestRequestTypeDef(
    _RequiredUpdateRuleRequestRequestTypeDef, _OptionalUpdateRuleRequestRequestTypeDef
):
    pass


UpdateRuleResponseTypeDef = TypedDict(
    "UpdateRuleResponseTypeDef",
    {
        "Identifier": str,
        "RetentionPeriod": RetentionPeriodTypeDef,
        "Description": str,
        "ResourceType": ResourceTypeType,
        "ResourceTags": List[ResourceTagTypeDef],
        "Status": RuleStatusType,
        "LockState": LockStateType,
        "LockEndTime": datetime,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "Tags": List[TagTypeDef],
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

LockConfigurationTypeDef = TypedDict(
    "LockConfigurationTypeDef",
    {
        "UnlockDelay": UnlockDelayTypeDef,
    },
)

ListRulesResponseTypeDef = TypedDict(
    "ListRulesResponseTypeDef",
    {
        "Rules": List[RuleSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateRuleRequestRequestTypeDef = TypedDict(
    "_RequiredCreateRuleRequestRequestTypeDef",
    {
        "RetentionPeriod": RetentionPeriodTypeDef,
        "ResourceType": ResourceTypeType,
    },
)
_OptionalCreateRuleRequestRequestTypeDef = TypedDict(
    "_OptionalCreateRuleRequestRequestTypeDef",
    {
        "Description": str,
        "Tags": Sequence[TagTypeDef],
        "ResourceTags": Sequence[ResourceTagTypeDef],
        "LockConfiguration": LockConfigurationTypeDef,
    },
    total=False,
)


class CreateRuleRequestRequestTypeDef(
    _RequiredCreateRuleRequestRequestTypeDef, _OptionalCreateRuleRequestRequestTypeDef
):
    pass


CreateRuleResponseTypeDef = TypedDict(
    "CreateRuleResponseTypeDef",
    {
        "Identifier": str,
        "RetentionPeriod": RetentionPeriodTypeDef,
        "Description": str,
        "Tags": List[TagTypeDef],
        "ResourceType": ResourceTypeType,
        "ResourceTags": List[ResourceTagTypeDef],
        "Status": RuleStatusType,
        "LockConfiguration": LockConfigurationTypeDef,
        "LockState": LockStateType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetRuleResponseTypeDef = TypedDict(
    "GetRuleResponseTypeDef",
    {
        "Identifier": str,
        "Description": str,
        "ResourceType": ResourceTypeType,
        "RetentionPeriod": RetentionPeriodTypeDef,
        "ResourceTags": List[ResourceTagTypeDef],
        "Status": RuleStatusType,
        "LockConfiguration": LockConfigurationTypeDef,
        "LockState": LockStateType,
        "LockEndTime": datetime,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

LockRuleRequestRequestTypeDef = TypedDict(
    "LockRuleRequestRequestTypeDef",
    {
        "Identifier": str,
        "LockConfiguration": LockConfigurationTypeDef,
    },
)

LockRuleResponseTypeDef = TypedDict(
    "LockRuleResponseTypeDef",
    {
        "Identifier": str,
        "Description": str,
        "ResourceType": ResourceTypeType,
        "RetentionPeriod": RetentionPeriodTypeDef,
        "ResourceTags": List[ResourceTagTypeDef],
        "Status": RuleStatusType,
        "LockConfiguration": LockConfigurationTypeDef,
        "LockState": LockStateType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UnlockRuleResponseTypeDef = TypedDict(
    "UnlockRuleResponseTypeDef",
    {
        "Identifier": str,
        "Description": str,
        "ResourceType": ResourceTypeType,
        "RetentionPeriod": RetentionPeriodTypeDef,
        "ResourceTags": List[ResourceTagTypeDef],
        "Status": RuleStatusType,
        "LockConfiguration": LockConfigurationTypeDef,
        "LockState": LockStateType,
        "LockEndTime": datetime,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)
