"""
Type annotations for wafv2 service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wafv2/type_defs/)

Usage::

    ```python
    from mypy_boto3_wafv2.type_defs import APIKeySummaryTypeDef

    data: APIKeySummaryTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    ActionValueType,
    BodyParsingFallbackBehaviorType,
    ComparisonOperatorType,
    CountryCodeType,
    FailureReasonType,
    FallbackBehaviorType,
    FilterBehaviorType,
    FilterRequirementType,
    ForwardedIPPositionType,
    InspectionLevelType,
    IPAddressVersionType,
    JsonMatchScopeType,
    LabelMatchScopeType,
    MapMatchScopeType,
    OversizeHandlingType,
    PayloadTypeType,
    PlatformType,
    PositionalConstraintType,
    RateBasedStatementAggregateKeyTypeType,
    ResourceTypeType,
    ResponseContentTypeType,
    ScopeType,
    SensitivityLevelType,
    SizeInspectionLimitType,
    TextTransformationTypeType,
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
    "APIKeySummaryTypeDef",
    "AWSManagedRulesBotControlRuleSetTypeDef",
    "ActionConditionTypeDef",
    "AddressFieldTypeDef",
    "AndStatementTypeDef",
    "AssociateWebACLRequestRequestTypeDef",
    "RequestBodyAssociatedResourceTypeConfigTypeDef",
    "BodyTypeDef",
    "TextTransformationTypeDef",
    "ImmunityTimePropertyTypeDef",
    "CaptchaResponseTypeDef",
    "ChallengeResponseTypeDef",
    "CheckCapacityResponseTypeDef",
    "LabelNameConditionTypeDef",
    "CookieMatchPatternTypeDef",
    "CreateAPIKeyRequestRequestTypeDef",
    "CreateAPIKeyResponseTypeDef",
    "TagTypeDef",
    "IPSetSummaryTypeDef",
    "RegexTypeDef",
    "RegexPatternSetSummaryTypeDef",
    "CustomResponseBodyTypeDef",
    "VisibilityConfigTypeDef",
    "RuleGroupSummaryTypeDef",
    "WebACLSummaryTypeDef",
    "CustomHTTPHeaderTypeDef",
    "DeleteFirewallManagerRuleGroupsRequestRequestTypeDef",
    "DeleteFirewallManagerRuleGroupsResponseTypeDef",
    "DeleteIPSetRequestRequestTypeDef",
    "DeleteLoggingConfigurationRequestRequestTypeDef",
    "DeletePermissionPolicyRequestRequestTypeDef",
    "DeleteRegexPatternSetRequestRequestTypeDef",
    "DeleteRuleGroupRequestRequestTypeDef",
    "DeleteWebACLRequestRequestTypeDef",
    "DescribeAllManagedProductsRequestRequestTypeDef",
    "ManagedProductDescriptorTypeDef",
    "DescribeManagedProductsByVendorRequestRequestTypeDef",
    "DescribeManagedRuleGroupRequestRequestTypeDef",
    "LabelSummaryTypeDef",
    "DisassociateWebACLRequestRequestTypeDef",
    "EmailFieldTypeDef",
    "ExcludedRuleTypeDef",
    "HeaderOrderTypeDef",
    "SingleHeaderTypeDef",
    "SingleQueryArgumentTypeDef",
    "ForwardedIPConfigTypeDef",
    "GenerateMobileSdkReleaseUrlRequestRequestTypeDef",
    "GenerateMobileSdkReleaseUrlResponseTypeDef",
    "GetDecryptedAPIKeyRequestRequestTypeDef",
    "GetDecryptedAPIKeyResponseTypeDef",
    "GetIPSetRequestRequestTypeDef",
    "IPSetTypeDef",
    "GetLoggingConfigurationRequestRequestTypeDef",
    "GetManagedRuleSetRequestRequestTypeDef",
    "GetMobileSdkReleaseRequestRequestTypeDef",
    "GetPermissionPolicyRequestRequestTypeDef",
    "GetPermissionPolicyResponseTypeDef",
    "GetRateBasedStatementManagedKeysRequestRequestTypeDef",
    "RateBasedStatementManagedKeysIPSetTypeDef",
    "GetRegexPatternSetRequestRequestTypeDef",
    "GetRuleGroupRequestRequestTypeDef",
    "TimeWindowTypeDef",
    "GetWebACLForResourceRequestRequestTypeDef",
    "GetWebACLRequestRequestTypeDef",
    "HTTPHeaderTypeDef",
    "HeaderMatchPatternTypeDef",
    "IPSetForwardedIPConfigTypeDef",
    "JsonMatchPatternTypeDef",
    "LabelMatchStatementTypeDef",
    "LabelTypeDef",
    "ListAPIKeysRequestRequestTypeDef",
    "ListAvailableManagedRuleGroupVersionsRequestRequestTypeDef",
    "ManagedRuleGroupVersionTypeDef",
    "ListAvailableManagedRuleGroupsRequestRequestTypeDef",
    "ManagedRuleGroupSummaryTypeDef",
    "ListIPSetsRequestRequestTypeDef",
    "ListLoggingConfigurationsRequestRequestTypeDef",
    "ListManagedRuleSetsRequestRequestTypeDef",
    "ManagedRuleSetSummaryTypeDef",
    "ListMobileSdkReleasesRequestRequestTypeDef",
    "ReleaseSummaryTypeDef",
    "ListRegexPatternSetsRequestRequestTypeDef",
    "ListResourcesForWebACLRequestRequestTypeDef",
    "ListResourcesForWebACLResponseTypeDef",
    "ListRuleGroupsRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListWebACLsRequestRequestTypeDef",
    "PasswordFieldTypeDef",
    "UsernameFieldTypeDef",
    "ManagedRuleSetVersionTypeDef",
    "NotStatementTypeDef",
    "OrStatementTypeDef",
    "PhoneNumberFieldTypeDef",
    "VersionToPublishTypeDef",
    "PutManagedRuleSetVersionsResponseTypeDef",
    "PutPermissionPolicyRequestRequestTypeDef",
    "RateLimitLabelNamespaceTypeDef",
    "ResponseInspectionBodyContainsTypeDef",
    "ResponseInspectionHeaderTypeDef",
    "ResponseInspectionJsonTypeDef",
    "ResponseInspectionStatusCodeTypeDef",
    "ResponseMetadataTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateIPSetRequestRequestTypeDef",
    "UpdateIPSetResponseTypeDef",
    "UpdateManagedRuleSetVersionExpiryDateRequestRequestTypeDef",
    "UpdateManagedRuleSetVersionExpiryDateResponseTypeDef",
    "UpdateRegexPatternSetResponseTypeDef",
    "UpdateRuleGroupResponseTypeDef",
    "UpdateWebACLResponseTypeDef",
    "ListAPIKeysResponseTypeDef",
    "AssociationConfigTypeDef",
    "RateLimitCookieTypeDef",
    "RateLimitHeaderTypeDef",
    "RateLimitQueryArgumentTypeDef",
    "RateLimitQueryStringTypeDef",
    "CaptchaConfigTypeDef",
    "ChallengeConfigTypeDef",
    "ConditionTypeDef",
    "CookiesTypeDef",
    "CreateIPSetRequestRequestTypeDef",
    "MobileSdkReleaseTypeDef",
    "TagInfoForResourceTypeDef",
    "TagResourceRequestRequestTypeDef",
    "CreateIPSetResponseTypeDef",
    "ListIPSetsResponseTypeDef",
    "CreateRegexPatternSetRequestRequestTypeDef",
    "RegexPatternSetTypeDef",
    "UpdateRegexPatternSetRequestRequestTypeDef",
    "CreateRegexPatternSetResponseTypeDef",
    "ListRegexPatternSetsResponseTypeDef",
    "CreateRuleGroupResponseTypeDef",
    "ListRuleGroupsResponseTypeDef",
    "CreateWebACLResponseTypeDef",
    "ListWebACLsResponseTypeDef",
    "CustomRequestHandlingTypeDef",
    "CustomResponseTypeDef",
    "DescribeAllManagedProductsResponseTypeDef",
    "DescribeManagedProductsByVendorResponseTypeDef",
    "GeoMatchStatementTypeDef",
    "GetIPSetResponseTypeDef",
    "GetRateBasedStatementManagedKeysResponseTypeDef",
    "GetSampledRequestsRequestRequestTypeDef",
    "HTTPRequestTypeDef",
    "HeadersTypeDef",
    "IPSetReferenceStatementTypeDef",
    "JsonBodyTypeDef",
    "ListAvailableManagedRuleGroupVersionsResponseTypeDef",
    "ListAvailableManagedRuleGroupsResponseTypeDef",
    "ListManagedRuleSetsResponseTypeDef",
    "ListMobileSdkReleasesResponseTypeDef",
    "RequestInspectionTypeDef",
    "ManagedRuleSetTypeDef",
    "RequestInspectionACFPTypeDef",
    "PutManagedRuleSetVersionsRequestRequestTypeDef",
    "ResponseInspectionTypeDef",
    "RateBasedStatementCustomKeyTypeDef",
    "FilterTypeDef",
    "GetMobileSdkReleaseResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "GetRegexPatternSetResponseTypeDef",
    "AllowActionTypeDef",
    "CaptchaActionTypeDef",
    "ChallengeActionTypeDef",
    "CountActionTypeDef",
    "BlockActionTypeDef",
    "SampledHTTPRequestTypeDef",
    "FieldToMatchTypeDef",
    "GetManagedRuleSetResponseTypeDef",
    "AWSManagedRulesACFPRuleSetTypeDef",
    "AWSManagedRulesATPRuleSetTypeDef",
    "RateBasedStatementTypeDef",
    "LoggingFilterTypeDef",
    "OverrideActionTypeDef",
    "DefaultActionTypeDef",
    "RuleActionTypeDef",
    "GetSampledRequestsResponseTypeDef",
    "ByteMatchStatementTypeDef",
    "RegexMatchStatementTypeDef",
    "RegexPatternSetReferenceStatementTypeDef",
    "SizeConstraintStatementTypeDef",
    "SqliMatchStatementTypeDef",
    "XssMatchStatementTypeDef",
    "ManagedRuleGroupConfigTypeDef",
    "LoggingConfigurationTypeDef",
    "RuleActionOverrideTypeDef",
    "RuleSummaryTypeDef",
    "RuleTypeDef",
    "GetLoggingConfigurationResponseTypeDef",
    "ListLoggingConfigurationsResponseTypeDef",
    "PutLoggingConfigurationRequestRequestTypeDef",
    "PutLoggingConfigurationResponseTypeDef",
    "ManagedRuleGroupStatementTypeDef",
    "RuleGroupReferenceStatementTypeDef",
    "DescribeManagedRuleGroupResponseTypeDef",
    "CheckCapacityRequestRequestTypeDef",
    "CreateRuleGroupRequestRequestTypeDef",
    "CreateWebACLRequestRequestTypeDef",
    "RuleGroupTypeDef",
    "UpdateRuleGroupRequestRequestTypeDef",
    "UpdateWebACLRequestRequestTypeDef",
    "FirewallManagerStatementTypeDef",
    "StatementTypeDef",
    "GetRuleGroupResponseTypeDef",
    "FirewallManagerRuleGroupTypeDef",
    "WebACLTypeDef",
    "GetWebACLForResourceResponseTypeDef",
    "GetWebACLResponseTypeDef",
)

APIKeySummaryTypeDef = TypedDict(
    "APIKeySummaryTypeDef",
    {
        "TokenDomains": List[str],
        "APIKey": str,
        "CreationTimestamp": datetime,
        "Version": int,
    },
    total=False,
)

AWSManagedRulesBotControlRuleSetTypeDef = TypedDict(
    "AWSManagedRulesBotControlRuleSetTypeDef",
    {
        "InspectionLevel": InspectionLevelType,
    },
)

ActionConditionTypeDef = TypedDict(
    "ActionConditionTypeDef",
    {
        "Action": ActionValueType,
    },
)

AddressFieldTypeDef = TypedDict(
    "AddressFieldTypeDef",
    {
        "Identifier": str,
    },
)

AndStatementTypeDef = TypedDict(
    "AndStatementTypeDef",
    {
        "Statements": Sequence["StatementTypeDef"],
    },
)

AssociateWebACLRequestRequestTypeDef = TypedDict(
    "AssociateWebACLRequestRequestTypeDef",
    {
        "WebACLArn": str,
        "ResourceArn": str,
    },
)

RequestBodyAssociatedResourceTypeConfigTypeDef = TypedDict(
    "RequestBodyAssociatedResourceTypeConfigTypeDef",
    {
        "DefaultSizeInspectionLimit": SizeInspectionLimitType,
    },
)

BodyTypeDef = TypedDict(
    "BodyTypeDef",
    {
        "OversizeHandling": OversizeHandlingType,
    },
    total=False,
)

TextTransformationTypeDef = TypedDict(
    "TextTransformationTypeDef",
    {
        "Priority": int,
        "Type": TextTransformationTypeType,
    },
)

ImmunityTimePropertyTypeDef = TypedDict(
    "ImmunityTimePropertyTypeDef",
    {
        "ImmunityTime": int,
    },
)

CaptchaResponseTypeDef = TypedDict(
    "CaptchaResponseTypeDef",
    {
        "ResponseCode": int,
        "SolveTimestamp": int,
        "FailureReason": FailureReasonType,
    },
    total=False,
)

ChallengeResponseTypeDef = TypedDict(
    "ChallengeResponseTypeDef",
    {
        "ResponseCode": int,
        "SolveTimestamp": int,
        "FailureReason": FailureReasonType,
    },
    total=False,
)

CheckCapacityResponseTypeDef = TypedDict(
    "CheckCapacityResponseTypeDef",
    {
        "Capacity": int,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

LabelNameConditionTypeDef = TypedDict(
    "LabelNameConditionTypeDef",
    {
        "LabelName": str,
    },
)

CookieMatchPatternTypeDef = TypedDict(
    "CookieMatchPatternTypeDef",
    {
        "All": Mapping[str, Any],
        "IncludedCookies": Sequence[str],
        "ExcludedCookies": Sequence[str],
    },
    total=False,
)

CreateAPIKeyRequestRequestTypeDef = TypedDict(
    "CreateAPIKeyRequestRequestTypeDef",
    {
        "Scope": ScopeType,
        "TokenDomains": Sequence[str],
    },
)

CreateAPIKeyResponseTypeDef = TypedDict(
    "CreateAPIKeyResponseTypeDef",
    {
        "APIKey": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

IPSetSummaryTypeDef = TypedDict(
    "IPSetSummaryTypeDef",
    {
        "Name": str,
        "Id": str,
        "Description": str,
        "LockToken": str,
        "ARN": str,
    },
    total=False,
)

RegexTypeDef = TypedDict(
    "RegexTypeDef",
    {
        "RegexString": str,
    },
    total=False,
)

RegexPatternSetSummaryTypeDef = TypedDict(
    "RegexPatternSetSummaryTypeDef",
    {
        "Name": str,
        "Id": str,
        "Description": str,
        "LockToken": str,
        "ARN": str,
    },
    total=False,
)

CustomResponseBodyTypeDef = TypedDict(
    "CustomResponseBodyTypeDef",
    {
        "ContentType": ResponseContentTypeType,
        "Content": str,
    },
)

VisibilityConfigTypeDef = TypedDict(
    "VisibilityConfigTypeDef",
    {
        "SampledRequestsEnabled": bool,
        "CloudWatchMetricsEnabled": bool,
        "MetricName": str,
    },
)

RuleGroupSummaryTypeDef = TypedDict(
    "RuleGroupSummaryTypeDef",
    {
        "Name": str,
        "Id": str,
        "Description": str,
        "LockToken": str,
        "ARN": str,
    },
    total=False,
)

WebACLSummaryTypeDef = TypedDict(
    "WebACLSummaryTypeDef",
    {
        "Name": str,
        "Id": str,
        "Description": str,
        "LockToken": str,
        "ARN": str,
    },
    total=False,
)

CustomHTTPHeaderTypeDef = TypedDict(
    "CustomHTTPHeaderTypeDef",
    {
        "Name": str,
        "Value": str,
    },
)

DeleteFirewallManagerRuleGroupsRequestRequestTypeDef = TypedDict(
    "DeleteFirewallManagerRuleGroupsRequestRequestTypeDef",
    {
        "WebACLArn": str,
        "WebACLLockToken": str,
    },
)

DeleteFirewallManagerRuleGroupsResponseTypeDef = TypedDict(
    "DeleteFirewallManagerRuleGroupsResponseTypeDef",
    {
        "NextWebACLLockToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteIPSetRequestRequestTypeDef = TypedDict(
    "DeleteIPSetRequestRequestTypeDef",
    {
        "Name": str,
        "Scope": ScopeType,
        "Id": str,
        "LockToken": str,
    },
)

DeleteLoggingConfigurationRequestRequestTypeDef = TypedDict(
    "DeleteLoggingConfigurationRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

DeletePermissionPolicyRequestRequestTypeDef = TypedDict(
    "DeletePermissionPolicyRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

DeleteRegexPatternSetRequestRequestTypeDef = TypedDict(
    "DeleteRegexPatternSetRequestRequestTypeDef",
    {
        "Name": str,
        "Scope": ScopeType,
        "Id": str,
        "LockToken": str,
    },
)

DeleteRuleGroupRequestRequestTypeDef = TypedDict(
    "DeleteRuleGroupRequestRequestTypeDef",
    {
        "Name": str,
        "Scope": ScopeType,
        "Id": str,
        "LockToken": str,
    },
)

DeleteWebACLRequestRequestTypeDef = TypedDict(
    "DeleteWebACLRequestRequestTypeDef",
    {
        "Name": str,
        "Scope": ScopeType,
        "Id": str,
        "LockToken": str,
    },
)

DescribeAllManagedProductsRequestRequestTypeDef = TypedDict(
    "DescribeAllManagedProductsRequestRequestTypeDef",
    {
        "Scope": ScopeType,
    },
)

ManagedProductDescriptorTypeDef = TypedDict(
    "ManagedProductDescriptorTypeDef",
    {
        "VendorName": str,
        "ManagedRuleSetName": str,
        "ProductId": str,
        "ProductLink": str,
        "ProductTitle": str,
        "ProductDescription": str,
        "SnsTopicArn": str,
        "IsVersioningSupported": bool,
        "IsAdvancedManagedRuleSet": bool,
    },
    total=False,
)

DescribeManagedProductsByVendorRequestRequestTypeDef = TypedDict(
    "DescribeManagedProductsByVendorRequestRequestTypeDef",
    {
        "VendorName": str,
        "Scope": ScopeType,
    },
)

_RequiredDescribeManagedRuleGroupRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeManagedRuleGroupRequestRequestTypeDef",
    {
        "VendorName": str,
        "Name": str,
        "Scope": ScopeType,
    },
)
_OptionalDescribeManagedRuleGroupRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeManagedRuleGroupRequestRequestTypeDef",
    {
        "VersionName": str,
    },
    total=False,
)

class DescribeManagedRuleGroupRequestRequestTypeDef(
    _RequiredDescribeManagedRuleGroupRequestRequestTypeDef,
    _OptionalDescribeManagedRuleGroupRequestRequestTypeDef,
):
    pass

LabelSummaryTypeDef = TypedDict(
    "LabelSummaryTypeDef",
    {
        "Name": str,
    },
    total=False,
)

DisassociateWebACLRequestRequestTypeDef = TypedDict(
    "DisassociateWebACLRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

EmailFieldTypeDef = TypedDict(
    "EmailFieldTypeDef",
    {
        "Identifier": str,
    },
)

ExcludedRuleTypeDef = TypedDict(
    "ExcludedRuleTypeDef",
    {
        "Name": str,
    },
)

HeaderOrderTypeDef = TypedDict(
    "HeaderOrderTypeDef",
    {
        "OversizeHandling": OversizeHandlingType,
    },
)

SingleHeaderTypeDef = TypedDict(
    "SingleHeaderTypeDef",
    {
        "Name": str,
    },
)

SingleQueryArgumentTypeDef = TypedDict(
    "SingleQueryArgumentTypeDef",
    {
        "Name": str,
    },
)

ForwardedIPConfigTypeDef = TypedDict(
    "ForwardedIPConfigTypeDef",
    {
        "HeaderName": str,
        "FallbackBehavior": FallbackBehaviorType,
    },
)

GenerateMobileSdkReleaseUrlRequestRequestTypeDef = TypedDict(
    "GenerateMobileSdkReleaseUrlRequestRequestTypeDef",
    {
        "Platform": PlatformType,
        "ReleaseVersion": str,
    },
)

GenerateMobileSdkReleaseUrlResponseTypeDef = TypedDict(
    "GenerateMobileSdkReleaseUrlResponseTypeDef",
    {
        "Url": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetDecryptedAPIKeyRequestRequestTypeDef = TypedDict(
    "GetDecryptedAPIKeyRequestRequestTypeDef",
    {
        "Scope": ScopeType,
        "APIKey": str,
    },
)

GetDecryptedAPIKeyResponseTypeDef = TypedDict(
    "GetDecryptedAPIKeyResponseTypeDef",
    {
        "TokenDomains": List[str],
        "CreationTimestamp": datetime,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetIPSetRequestRequestTypeDef = TypedDict(
    "GetIPSetRequestRequestTypeDef",
    {
        "Name": str,
        "Scope": ScopeType,
        "Id": str,
    },
)

_RequiredIPSetTypeDef = TypedDict(
    "_RequiredIPSetTypeDef",
    {
        "Name": str,
        "Id": str,
        "ARN": str,
        "IPAddressVersion": IPAddressVersionType,
        "Addresses": List[str],
    },
)
_OptionalIPSetTypeDef = TypedDict(
    "_OptionalIPSetTypeDef",
    {
        "Description": str,
    },
    total=False,
)

class IPSetTypeDef(_RequiredIPSetTypeDef, _OptionalIPSetTypeDef):
    pass

GetLoggingConfigurationRequestRequestTypeDef = TypedDict(
    "GetLoggingConfigurationRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

GetManagedRuleSetRequestRequestTypeDef = TypedDict(
    "GetManagedRuleSetRequestRequestTypeDef",
    {
        "Name": str,
        "Scope": ScopeType,
        "Id": str,
    },
)

GetMobileSdkReleaseRequestRequestTypeDef = TypedDict(
    "GetMobileSdkReleaseRequestRequestTypeDef",
    {
        "Platform": PlatformType,
        "ReleaseVersion": str,
    },
)

GetPermissionPolicyRequestRequestTypeDef = TypedDict(
    "GetPermissionPolicyRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

GetPermissionPolicyResponseTypeDef = TypedDict(
    "GetPermissionPolicyResponseTypeDef",
    {
        "Policy": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredGetRateBasedStatementManagedKeysRequestRequestTypeDef = TypedDict(
    "_RequiredGetRateBasedStatementManagedKeysRequestRequestTypeDef",
    {
        "Scope": ScopeType,
        "WebACLName": str,
        "WebACLId": str,
        "RuleName": str,
    },
)
_OptionalGetRateBasedStatementManagedKeysRequestRequestTypeDef = TypedDict(
    "_OptionalGetRateBasedStatementManagedKeysRequestRequestTypeDef",
    {
        "RuleGroupRuleName": str,
    },
    total=False,
)

class GetRateBasedStatementManagedKeysRequestRequestTypeDef(
    _RequiredGetRateBasedStatementManagedKeysRequestRequestTypeDef,
    _OptionalGetRateBasedStatementManagedKeysRequestRequestTypeDef,
):
    pass

RateBasedStatementManagedKeysIPSetTypeDef = TypedDict(
    "RateBasedStatementManagedKeysIPSetTypeDef",
    {
        "IPAddressVersion": IPAddressVersionType,
        "Addresses": List[str],
    },
    total=False,
)

GetRegexPatternSetRequestRequestTypeDef = TypedDict(
    "GetRegexPatternSetRequestRequestTypeDef",
    {
        "Name": str,
        "Scope": ScopeType,
        "Id": str,
    },
)

GetRuleGroupRequestRequestTypeDef = TypedDict(
    "GetRuleGroupRequestRequestTypeDef",
    {
        "Name": str,
        "Scope": ScopeType,
        "Id": str,
        "ARN": str,
    },
    total=False,
)

TimeWindowTypeDef = TypedDict(
    "TimeWindowTypeDef",
    {
        "StartTime": Union[datetime, str],
        "EndTime": Union[datetime, str],
    },
)

GetWebACLForResourceRequestRequestTypeDef = TypedDict(
    "GetWebACLForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

GetWebACLRequestRequestTypeDef = TypedDict(
    "GetWebACLRequestRequestTypeDef",
    {
        "Name": str,
        "Scope": ScopeType,
        "Id": str,
    },
)

HTTPHeaderTypeDef = TypedDict(
    "HTTPHeaderTypeDef",
    {
        "Name": str,
        "Value": str,
    },
    total=False,
)

HeaderMatchPatternTypeDef = TypedDict(
    "HeaderMatchPatternTypeDef",
    {
        "All": Mapping[str, Any],
        "IncludedHeaders": Sequence[str],
        "ExcludedHeaders": Sequence[str],
    },
    total=False,
)

IPSetForwardedIPConfigTypeDef = TypedDict(
    "IPSetForwardedIPConfigTypeDef",
    {
        "HeaderName": str,
        "FallbackBehavior": FallbackBehaviorType,
        "Position": ForwardedIPPositionType,
    },
)

JsonMatchPatternTypeDef = TypedDict(
    "JsonMatchPatternTypeDef",
    {
        "All": Mapping[str, Any],
        "IncludedPaths": Sequence[str],
    },
    total=False,
)

LabelMatchStatementTypeDef = TypedDict(
    "LabelMatchStatementTypeDef",
    {
        "Scope": LabelMatchScopeType,
        "Key": str,
    },
)

LabelTypeDef = TypedDict(
    "LabelTypeDef",
    {
        "Name": str,
    },
)

_RequiredListAPIKeysRequestRequestTypeDef = TypedDict(
    "_RequiredListAPIKeysRequestRequestTypeDef",
    {
        "Scope": ScopeType,
    },
)
_OptionalListAPIKeysRequestRequestTypeDef = TypedDict(
    "_OptionalListAPIKeysRequestRequestTypeDef",
    {
        "NextMarker": str,
        "Limit": int,
    },
    total=False,
)

class ListAPIKeysRequestRequestTypeDef(
    _RequiredListAPIKeysRequestRequestTypeDef, _OptionalListAPIKeysRequestRequestTypeDef
):
    pass

_RequiredListAvailableManagedRuleGroupVersionsRequestRequestTypeDef = TypedDict(
    "_RequiredListAvailableManagedRuleGroupVersionsRequestRequestTypeDef",
    {
        "VendorName": str,
        "Name": str,
        "Scope": ScopeType,
    },
)
_OptionalListAvailableManagedRuleGroupVersionsRequestRequestTypeDef = TypedDict(
    "_OptionalListAvailableManagedRuleGroupVersionsRequestRequestTypeDef",
    {
        "NextMarker": str,
        "Limit": int,
    },
    total=False,
)

class ListAvailableManagedRuleGroupVersionsRequestRequestTypeDef(
    _RequiredListAvailableManagedRuleGroupVersionsRequestRequestTypeDef,
    _OptionalListAvailableManagedRuleGroupVersionsRequestRequestTypeDef,
):
    pass

ManagedRuleGroupVersionTypeDef = TypedDict(
    "ManagedRuleGroupVersionTypeDef",
    {
        "Name": str,
        "LastUpdateTimestamp": datetime,
    },
    total=False,
)

_RequiredListAvailableManagedRuleGroupsRequestRequestTypeDef = TypedDict(
    "_RequiredListAvailableManagedRuleGroupsRequestRequestTypeDef",
    {
        "Scope": ScopeType,
    },
)
_OptionalListAvailableManagedRuleGroupsRequestRequestTypeDef = TypedDict(
    "_OptionalListAvailableManagedRuleGroupsRequestRequestTypeDef",
    {
        "NextMarker": str,
        "Limit": int,
    },
    total=False,
)

class ListAvailableManagedRuleGroupsRequestRequestTypeDef(
    _RequiredListAvailableManagedRuleGroupsRequestRequestTypeDef,
    _OptionalListAvailableManagedRuleGroupsRequestRequestTypeDef,
):
    pass

ManagedRuleGroupSummaryTypeDef = TypedDict(
    "ManagedRuleGroupSummaryTypeDef",
    {
        "VendorName": str,
        "Name": str,
        "VersioningSupported": bool,
        "Description": str,
    },
    total=False,
)

_RequiredListIPSetsRequestRequestTypeDef = TypedDict(
    "_RequiredListIPSetsRequestRequestTypeDef",
    {
        "Scope": ScopeType,
    },
)
_OptionalListIPSetsRequestRequestTypeDef = TypedDict(
    "_OptionalListIPSetsRequestRequestTypeDef",
    {
        "NextMarker": str,
        "Limit": int,
    },
    total=False,
)

class ListIPSetsRequestRequestTypeDef(
    _RequiredListIPSetsRequestRequestTypeDef, _OptionalListIPSetsRequestRequestTypeDef
):
    pass

_RequiredListLoggingConfigurationsRequestRequestTypeDef = TypedDict(
    "_RequiredListLoggingConfigurationsRequestRequestTypeDef",
    {
        "Scope": ScopeType,
    },
)
_OptionalListLoggingConfigurationsRequestRequestTypeDef = TypedDict(
    "_OptionalListLoggingConfigurationsRequestRequestTypeDef",
    {
        "NextMarker": str,
        "Limit": int,
    },
    total=False,
)

class ListLoggingConfigurationsRequestRequestTypeDef(
    _RequiredListLoggingConfigurationsRequestRequestTypeDef,
    _OptionalListLoggingConfigurationsRequestRequestTypeDef,
):
    pass

_RequiredListManagedRuleSetsRequestRequestTypeDef = TypedDict(
    "_RequiredListManagedRuleSetsRequestRequestTypeDef",
    {
        "Scope": ScopeType,
    },
)
_OptionalListManagedRuleSetsRequestRequestTypeDef = TypedDict(
    "_OptionalListManagedRuleSetsRequestRequestTypeDef",
    {
        "NextMarker": str,
        "Limit": int,
    },
    total=False,
)

class ListManagedRuleSetsRequestRequestTypeDef(
    _RequiredListManagedRuleSetsRequestRequestTypeDef,
    _OptionalListManagedRuleSetsRequestRequestTypeDef,
):
    pass

ManagedRuleSetSummaryTypeDef = TypedDict(
    "ManagedRuleSetSummaryTypeDef",
    {
        "Name": str,
        "Id": str,
        "Description": str,
        "LockToken": str,
        "ARN": str,
        "LabelNamespace": str,
    },
    total=False,
)

_RequiredListMobileSdkReleasesRequestRequestTypeDef = TypedDict(
    "_RequiredListMobileSdkReleasesRequestRequestTypeDef",
    {
        "Platform": PlatformType,
    },
)
_OptionalListMobileSdkReleasesRequestRequestTypeDef = TypedDict(
    "_OptionalListMobileSdkReleasesRequestRequestTypeDef",
    {
        "NextMarker": str,
        "Limit": int,
    },
    total=False,
)

class ListMobileSdkReleasesRequestRequestTypeDef(
    _RequiredListMobileSdkReleasesRequestRequestTypeDef,
    _OptionalListMobileSdkReleasesRequestRequestTypeDef,
):
    pass

ReleaseSummaryTypeDef = TypedDict(
    "ReleaseSummaryTypeDef",
    {
        "ReleaseVersion": str,
        "Timestamp": datetime,
    },
    total=False,
)

_RequiredListRegexPatternSetsRequestRequestTypeDef = TypedDict(
    "_RequiredListRegexPatternSetsRequestRequestTypeDef",
    {
        "Scope": ScopeType,
    },
)
_OptionalListRegexPatternSetsRequestRequestTypeDef = TypedDict(
    "_OptionalListRegexPatternSetsRequestRequestTypeDef",
    {
        "NextMarker": str,
        "Limit": int,
    },
    total=False,
)

class ListRegexPatternSetsRequestRequestTypeDef(
    _RequiredListRegexPatternSetsRequestRequestTypeDef,
    _OptionalListRegexPatternSetsRequestRequestTypeDef,
):
    pass

_RequiredListResourcesForWebACLRequestRequestTypeDef = TypedDict(
    "_RequiredListResourcesForWebACLRequestRequestTypeDef",
    {
        "WebACLArn": str,
    },
)
_OptionalListResourcesForWebACLRequestRequestTypeDef = TypedDict(
    "_OptionalListResourcesForWebACLRequestRequestTypeDef",
    {
        "ResourceType": ResourceTypeType,
    },
    total=False,
)

class ListResourcesForWebACLRequestRequestTypeDef(
    _RequiredListResourcesForWebACLRequestRequestTypeDef,
    _OptionalListResourcesForWebACLRequestRequestTypeDef,
):
    pass

ListResourcesForWebACLResponseTypeDef = TypedDict(
    "ListResourcesForWebACLResponseTypeDef",
    {
        "ResourceArns": List[str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListRuleGroupsRequestRequestTypeDef = TypedDict(
    "_RequiredListRuleGroupsRequestRequestTypeDef",
    {
        "Scope": ScopeType,
    },
)
_OptionalListRuleGroupsRequestRequestTypeDef = TypedDict(
    "_OptionalListRuleGroupsRequestRequestTypeDef",
    {
        "NextMarker": str,
        "Limit": int,
    },
    total=False,
)

class ListRuleGroupsRequestRequestTypeDef(
    _RequiredListRuleGroupsRequestRequestTypeDef, _OptionalListRuleGroupsRequestRequestTypeDef
):
    pass

_RequiredListTagsForResourceRequestRequestTypeDef = TypedDict(
    "_RequiredListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceARN": str,
    },
)
_OptionalListTagsForResourceRequestRequestTypeDef = TypedDict(
    "_OptionalListTagsForResourceRequestRequestTypeDef",
    {
        "NextMarker": str,
        "Limit": int,
    },
    total=False,
)

class ListTagsForResourceRequestRequestTypeDef(
    _RequiredListTagsForResourceRequestRequestTypeDef,
    _OptionalListTagsForResourceRequestRequestTypeDef,
):
    pass

_RequiredListWebACLsRequestRequestTypeDef = TypedDict(
    "_RequiredListWebACLsRequestRequestTypeDef",
    {
        "Scope": ScopeType,
    },
)
_OptionalListWebACLsRequestRequestTypeDef = TypedDict(
    "_OptionalListWebACLsRequestRequestTypeDef",
    {
        "NextMarker": str,
        "Limit": int,
    },
    total=False,
)

class ListWebACLsRequestRequestTypeDef(
    _RequiredListWebACLsRequestRequestTypeDef, _OptionalListWebACLsRequestRequestTypeDef
):
    pass

PasswordFieldTypeDef = TypedDict(
    "PasswordFieldTypeDef",
    {
        "Identifier": str,
    },
)

UsernameFieldTypeDef = TypedDict(
    "UsernameFieldTypeDef",
    {
        "Identifier": str,
    },
)

ManagedRuleSetVersionTypeDef = TypedDict(
    "ManagedRuleSetVersionTypeDef",
    {
        "AssociatedRuleGroupArn": str,
        "Capacity": int,
        "ForecastedLifetime": int,
        "PublishTimestamp": datetime,
        "LastUpdateTimestamp": datetime,
        "ExpiryTimestamp": datetime,
    },
    total=False,
)

NotStatementTypeDef = TypedDict(
    "NotStatementTypeDef",
    {
        "Statement": "StatementTypeDef",
    },
)

OrStatementTypeDef = TypedDict(
    "OrStatementTypeDef",
    {
        "Statements": Sequence[Dict[str, Any]],
    },
)

PhoneNumberFieldTypeDef = TypedDict(
    "PhoneNumberFieldTypeDef",
    {
        "Identifier": str,
    },
)

VersionToPublishTypeDef = TypedDict(
    "VersionToPublishTypeDef",
    {
        "AssociatedRuleGroupArn": str,
        "ForecastedLifetime": int,
    },
    total=False,
)

PutManagedRuleSetVersionsResponseTypeDef = TypedDict(
    "PutManagedRuleSetVersionsResponseTypeDef",
    {
        "NextLockToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

PutPermissionPolicyRequestRequestTypeDef = TypedDict(
    "PutPermissionPolicyRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "Policy": str,
    },
)

RateLimitLabelNamespaceTypeDef = TypedDict(
    "RateLimitLabelNamespaceTypeDef",
    {
        "Namespace": str,
    },
)

ResponseInspectionBodyContainsTypeDef = TypedDict(
    "ResponseInspectionBodyContainsTypeDef",
    {
        "SuccessStrings": Sequence[str],
        "FailureStrings": Sequence[str],
    },
)

ResponseInspectionHeaderTypeDef = TypedDict(
    "ResponseInspectionHeaderTypeDef",
    {
        "Name": str,
        "SuccessValues": Sequence[str],
        "FailureValues": Sequence[str],
    },
)

ResponseInspectionJsonTypeDef = TypedDict(
    "ResponseInspectionJsonTypeDef",
    {
        "Identifier": str,
        "SuccessValues": Sequence[str],
        "FailureValues": Sequence[str],
    },
)

ResponseInspectionStatusCodeTypeDef = TypedDict(
    "ResponseInspectionStatusCodeTypeDef",
    {
        "SuccessCodes": Sequence[int],
        "FailureCodes": Sequence[int],
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

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceARN": str,
        "TagKeys": Sequence[str],
    },
)

_RequiredUpdateIPSetRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateIPSetRequestRequestTypeDef",
    {
        "Name": str,
        "Scope": ScopeType,
        "Id": str,
        "Addresses": Sequence[str],
        "LockToken": str,
    },
)
_OptionalUpdateIPSetRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateIPSetRequestRequestTypeDef",
    {
        "Description": str,
    },
    total=False,
)

class UpdateIPSetRequestRequestTypeDef(
    _RequiredUpdateIPSetRequestRequestTypeDef, _OptionalUpdateIPSetRequestRequestTypeDef
):
    pass

UpdateIPSetResponseTypeDef = TypedDict(
    "UpdateIPSetResponseTypeDef",
    {
        "NextLockToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateManagedRuleSetVersionExpiryDateRequestRequestTypeDef = TypedDict(
    "UpdateManagedRuleSetVersionExpiryDateRequestRequestTypeDef",
    {
        "Name": str,
        "Scope": ScopeType,
        "Id": str,
        "LockToken": str,
        "VersionToExpire": str,
        "ExpiryTimestamp": Union[datetime, str],
    },
)

UpdateManagedRuleSetVersionExpiryDateResponseTypeDef = TypedDict(
    "UpdateManagedRuleSetVersionExpiryDateResponseTypeDef",
    {
        "ExpiringVersion": str,
        "ExpiryTimestamp": datetime,
        "NextLockToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateRegexPatternSetResponseTypeDef = TypedDict(
    "UpdateRegexPatternSetResponseTypeDef",
    {
        "NextLockToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateRuleGroupResponseTypeDef = TypedDict(
    "UpdateRuleGroupResponseTypeDef",
    {
        "NextLockToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateWebACLResponseTypeDef = TypedDict(
    "UpdateWebACLResponseTypeDef",
    {
        "NextLockToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListAPIKeysResponseTypeDef = TypedDict(
    "ListAPIKeysResponseTypeDef",
    {
        "NextMarker": str,
        "APIKeySummaries": List[APIKeySummaryTypeDef],
        "ApplicationIntegrationURL": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

AssociationConfigTypeDef = TypedDict(
    "AssociationConfigTypeDef",
    {
        "RequestBody": Mapping[
            Literal["CLOUDFRONT"], RequestBodyAssociatedResourceTypeConfigTypeDef
        ],
    },
    total=False,
)

RateLimitCookieTypeDef = TypedDict(
    "RateLimitCookieTypeDef",
    {
        "Name": str,
        "TextTransformations": Sequence[TextTransformationTypeDef],
    },
)

RateLimitHeaderTypeDef = TypedDict(
    "RateLimitHeaderTypeDef",
    {
        "Name": str,
        "TextTransformations": Sequence[TextTransformationTypeDef],
    },
)

RateLimitQueryArgumentTypeDef = TypedDict(
    "RateLimitQueryArgumentTypeDef",
    {
        "Name": str,
        "TextTransformations": Sequence[TextTransformationTypeDef],
    },
)

RateLimitQueryStringTypeDef = TypedDict(
    "RateLimitQueryStringTypeDef",
    {
        "TextTransformations": Sequence[TextTransformationTypeDef],
    },
)

CaptchaConfigTypeDef = TypedDict(
    "CaptchaConfigTypeDef",
    {
        "ImmunityTimeProperty": ImmunityTimePropertyTypeDef,
    },
    total=False,
)

ChallengeConfigTypeDef = TypedDict(
    "ChallengeConfigTypeDef",
    {
        "ImmunityTimeProperty": ImmunityTimePropertyTypeDef,
    },
    total=False,
)

ConditionTypeDef = TypedDict(
    "ConditionTypeDef",
    {
        "ActionCondition": ActionConditionTypeDef,
        "LabelNameCondition": LabelNameConditionTypeDef,
    },
    total=False,
)

CookiesTypeDef = TypedDict(
    "CookiesTypeDef",
    {
        "MatchPattern": CookieMatchPatternTypeDef,
        "MatchScope": MapMatchScopeType,
        "OversizeHandling": OversizeHandlingType,
    },
)

_RequiredCreateIPSetRequestRequestTypeDef = TypedDict(
    "_RequiredCreateIPSetRequestRequestTypeDef",
    {
        "Name": str,
        "Scope": ScopeType,
        "IPAddressVersion": IPAddressVersionType,
        "Addresses": Sequence[str],
    },
)
_OptionalCreateIPSetRequestRequestTypeDef = TypedDict(
    "_OptionalCreateIPSetRequestRequestTypeDef",
    {
        "Description": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)

class CreateIPSetRequestRequestTypeDef(
    _RequiredCreateIPSetRequestRequestTypeDef, _OptionalCreateIPSetRequestRequestTypeDef
):
    pass

MobileSdkReleaseTypeDef = TypedDict(
    "MobileSdkReleaseTypeDef",
    {
        "ReleaseVersion": str,
        "Timestamp": datetime,
        "ReleaseNotes": str,
        "Tags": List[TagTypeDef],
    },
    total=False,
)

TagInfoForResourceTypeDef = TypedDict(
    "TagInfoForResourceTypeDef",
    {
        "ResourceARN": str,
        "TagList": List[TagTypeDef],
    },
    total=False,
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceARN": str,
        "Tags": Sequence[TagTypeDef],
    },
)

CreateIPSetResponseTypeDef = TypedDict(
    "CreateIPSetResponseTypeDef",
    {
        "Summary": IPSetSummaryTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListIPSetsResponseTypeDef = TypedDict(
    "ListIPSetsResponseTypeDef",
    {
        "NextMarker": str,
        "IPSets": List[IPSetSummaryTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateRegexPatternSetRequestRequestTypeDef = TypedDict(
    "_RequiredCreateRegexPatternSetRequestRequestTypeDef",
    {
        "Name": str,
        "Scope": ScopeType,
        "RegularExpressionList": Sequence[RegexTypeDef],
    },
)
_OptionalCreateRegexPatternSetRequestRequestTypeDef = TypedDict(
    "_OptionalCreateRegexPatternSetRequestRequestTypeDef",
    {
        "Description": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)

class CreateRegexPatternSetRequestRequestTypeDef(
    _RequiredCreateRegexPatternSetRequestRequestTypeDef,
    _OptionalCreateRegexPatternSetRequestRequestTypeDef,
):
    pass

RegexPatternSetTypeDef = TypedDict(
    "RegexPatternSetTypeDef",
    {
        "Name": str,
        "Id": str,
        "ARN": str,
        "Description": str,
        "RegularExpressionList": List[RegexTypeDef],
    },
    total=False,
)

_RequiredUpdateRegexPatternSetRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateRegexPatternSetRequestRequestTypeDef",
    {
        "Name": str,
        "Scope": ScopeType,
        "Id": str,
        "RegularExpressionList": Sequence[RegexTypeDef],
        "LockToken": str,
    },
)
_OptionalUpdateRegexPatternSetRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateRegexPatternSetRequestRequestTypeDef",
    {
        "Description": str,
    },
    total=False,
)

class UpdateRegexPatternSetRequestRequestTypeDef(
    _RequiredUpdateRegexPatternSetRequestRequestTypeDef,
    _OptionalUpdateRegexPatternSetRequestRequestTypeDef,
):
    pass

CreateRegexPatternSetResponseTypeDef = TypedDict(
    "CreateRegexPatternSetResponseTypeDef",
    {
        "Summary": RegexPatternSetSummaryTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListRegexPatternSetsResponseTypeDef = TypedDict(
    "ListRegexPatternSetsResponseTypeDef",
    {
        "NextMarker": str,
        "RegexPatternSets": List[RegexPatternSetSummaryTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateRuleGroupResponseTypeDef = TypedDict(
    "CreateRuleGroupResponseTypeDef",
    {
        "Summary": RuleGroupSummaryTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListRuleGroupsResponseTypeDef = TypedDict(
    "ListRuleGroupsResponseTypeDef",
    {
        "NextMarker": str,
        "RuleGroups": List[RuleGroupSummaryTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateWebACLResponseTypeDef = TypedDict(
    "CreateWebACLResponseTypeDef",
    {
        "Summary": WebACLSummaryTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListWebACLsResponseTypeDef = TypedDict(
    "ListWebACLsResponseTypeDef",
    {
        "NextMarker": str,
        "WebACLs": List[WebACLSummaryTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CustomRequestHandlingTypeDef = TypedDict(
    "CustomRequestHandlingTypeDef",
    {
        "InsertHeaders": Sequence[CustomHTTPHeaderTypeDef],
    },
)

_RequiredCustomResponseTypeDef = TypedDict(
    "_RequiredCustomResponseTypeDef",
    {
        "ResponseCode": int,
    },
)
_OptionalCustomResponseTypeDef = TypedDict(
    "_OptionalCustomResponseTypeDef",
    {
        "CustomResponseBodyKey": str,
        "ResponseHeaders": Sequence[CustomHTTPHeaderTypeDef],
    },
    total=False,
)

class CustomResponseTypeDef(_RequiredCustomResponseTypeDef, _OptionalCustomResponseTypeDef):
    pass

DescribeAllManagedProductsResponseTypeDef = TypedDict(
    "DescribeAllManagedProductsResponseTypeDef",
    {
        "ManagedProducts": List[ManagedProductDescriptorTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeManagedProductsByVendorResponseTypeDef = TypedDict(
    "DescribeManagedProductsByVendorResponseTypeDef",
    {
        "ManagedProducts": List[ManagedProductDescriptorTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GeoMatchStatementTypeDef = TypedDict(
    "GeoMatchStatementTypeDef",
    {
        "CountryCodes": Sequence[CountryCodeType],
        "ForwardedIPConfig": ForwardedIPConfigTypeDef,
    },
    total=False,
)

GetIPSetResponseTypeDef = TypedDict(
    "GetIPSetResponseTypeDef",
    {
        "IPSet": IPSetTypeDef,
        "LockToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetRateBasedStatementManagedKeysResponseTypeDef = TypedDict(
    "GetRateBasedStatementManagedKeysResponseTypeDef",
    {
        "ManagedKeysIPV4": RateBasedStatementManagedKeysIPSetTypeDef,
        "ManagedKeysIPV6": RateBasedStatementManagedKeysIPSetTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetSampledRequestsRequestRequestTypeDef = TypedDict(
    "GetSampledRequestsRequestRequestTypeDef",
    {
        "WebAclArn": str,
        "RuleMetricName": str,
        "Scope": ScopeType,
        "TimeWindow": TimeWindowTypeDef,
        "MaxItems": int,
    },
)

HTTPRequestTypeDef = TypedDict(
    "HTTPRequestTypeDef",
    {
        "ClientIP": str,
        "Country": str,
        "URI": str,
        "Method": str,
        "HTTPVersion": str,
        "Headers": List[HTTPHeaderTypeDef],
    },
    total=False,
)

HeadersTypeDef = TypedDict(
    "HeadersTypeDef",
    {
        "MatchPattern": HeaderMatchPatternTypeDef,
        "MatchScope": MapMatchScopeType,
        "OversizeHandling": OversizeHandlingType,
    },
)

_RequiredIPSetReferenceStatementTypeDef = TypedDict(
    "_RequiredIPSetReferenceStatementTypeDef",
    {
        "ARN": str,
    },
)
_OptionalIPSetReferenceStatementTypeDef = TypedDict(
    "_OptionalIPSetReferenceStatementTypeDef",
    {
        "IPSetForwardedIPConfig": IPSetForwardedIPConfigTypeDef,
    },
    total=False,
)

class IPSetReferenceStatementTypeDef(
    _RequiredIPSetReferenceStatementTypeDef, _OptionalIPSetReferenceStatementTypeDef
):
    pass

_RequiredJsonBodyTypeDef = TypedDict(
    "_RequiredJsonBodyTypeDef",
    {
        "MatchPattern": JsonMatchPatternTypeDef,
        "MatchScope": JsonMatchScopeType,
    },
)
_OptionalJsonBodyTypeDef = TypedDict(
    "_OptionalJsonBodyTypeDef",
    {
        "InvalidFallbackBehavior": BodyParsingFallbackBehaviorType,
        "OversizeHandling": OversizeHandlingType,
    },
    total=False,
)

class JsonBodyTypeDef(_RequiredJsonBodyTypeDef, _OptionalJsonBodyTypeDef):
    pass

ListAvailableManagedRuleGroupVersionsResponseTypeDef = TypedDict(
    "ListAvailableManagedRuleGroupVersionsResponseTypeDef",
    {
        "NextMarker": str,
        "Versions": List[ManagedRuleGroupVersionTypeDef],
        "CurrentDefaultVersion": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListAvailableManagedRuleGroupsResponseTypeDef = TypedDict(
    "ListAvailableManagedRuleGroupsResponseTypeDef",
    {
        "NextMarker": str,
        "ManagedRuleGroups": List[ManagedRuleGroupSummaryTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListManagedRuleSetsResponseTypeDef = TypedDict(
    "ListManagedRuleSetsResponseTypeDef",
    {
        "NextMarker": str,
        "ManagedRuleSets": List[ManagedRuleSetSummaryTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListMobileSdkReleasesResponseTypeDef = TypedDict(
    "ListMobileSdkReleasesResponseTypeDef",
    {
        "ReleaseSummaries": List[ReleaseSummaryTypeDef],
        "NextMarker": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

RequestInspectionTypeDef = TypedDict(
    "RequestInspectionTypeDef",
    {
        "PayloadType": PayloadTypeType,
        "UsernameField": UsernameFieldTypeDef,
        "PasswordField": PasswordFieldTypeDef,
    },
)

_RequiredManagedRuleSetTypeDef = TypedDict(
    "_RequiredManagedRuleSetTypeDef",
    {
        "Name": str,
        "Id": str,
        "ARN": str,
    },
)
_OptionalManagedRuleSetTypeDef = TypedDict(
    "_OptionalManagedRuleSetTypeDef",
    {
        "Description": str,
        "PublishedVersions": Dict[str, ManagedRuleSetVersionTypeDef],
        "RecommendedVersion": str,
        "LabelNamespace": str,
    },
    total=False,
)

class ManagedRuleSetTypeDef(_RequiredManagedRuleSetTypeDef, _OptionalManagedRuleSetTypeDef):
    pass

_RequiredRequestInspectionACFPTypeDef = TypedDict(
    "_RequiredRequestInspectionACFPTypeDef",
    {
        "PayloadType": PayloadTypeType,
    },
)
_OptionalRequestInspectionACFPTypeDef = TypedDict(
    "_OptionalRequestInspectionACFPTypeDef",
    {
        "UsernameField": UsernameFieldTypeDef,
        "PasswordField": PasswordFieldTypeDef,
        "EmailField": EmailFieldTypeDef,
        "PhoneNumberFields": Sequence[PhoneNumberFieldTypeDef],
        "AddressFields": Sequence[AddressFieldTypeDef],
    },
    total=False,
)

class RequestInspectionACFPTypeDef(
    _RequiredRequestInspectionACFPTypeDef, _OptionalRequestInspectionACFPTypeDef
):
    pass

_RequiredPutManagedRuleSetVersionsRequestRequestTypeDef = TypedDict(
    "_RequiredPutManagedRuleSetVersionsRequestRequestTypeDef",
    {
        "Name": str,
        "Scope": ScopeType,
        "Id": str,
        "LockToken": str,
    },
)
_OptionalPutManagedRuleSetVersionsRequestRequestTypeDef = TypedDict(
    "_OptionalPutManagedRuleSetVersionsRequestRequestTypeDef",
    {
        "RecommendedVersion": str,
        "VersionsToPublish": Mapping[str, VersionToPublishTypeDef],
    },
    total=False,
)

class PutManagedRuleSetVersionsRequestRequestTypeDef(
    _RequiredPutManagedRuleSetVersionsRequestRequestTypeDef,
    _OptionalPutManagedRuleSetVersionsRequestRequestTypeDef,
):
    pass

ResponseInspectionTypeDef = TypedDict(
    "ResponseInspectionTypeDef",
    {
        "StatusCode": ResponseInspectionStatusCodeTypeDef,
        "Header": ResponseInspectionHeaderTypeDef,
        "BodyContains": ResponseInspectionBodyContainsTypeDef,
        "Json": ResponseInspectionJsonTypeDef,
    },
    total=False,
)

RateBasedStatementCustomKeyTypeDef = TypedDict(
    "RateBasedStatementCustomKeyTypeDef",
    {
        "Header": RateLimitHeaderTypeDef,
        "Cookie": RateLimitCookieTypeDef,
        "QueryArgument": RateLimitQueryArgumentTypeDef,
        "QueryString": RateLimitQueryStringTypeDef,
        "HTTPMethod": Mapping[str, Any],
        "ForwardedIP": Mapping[str, Any],
        "IP": Mapping[str, Any],
        "LabelNamespace": RateLimitLabelNamespaceTypeDef,
    },
    total=False,
)

FilterTypeDef = TypedDict(
    "FilterTypeDef",
    {
        "Behavior": FilterBehaviorType,
        "Requirement": FilterRequirementType,
        "Conditions": List[ConditionTypeDef],
    },
)

GetMobileSdkReleaseResponseTypeDef = TypedDict(
    "GetMobileSdkReleaseResponseTypeDef",
    {
        "MobileSdkRelease": MobileSdkReleaseTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "NextMarker": str,
        "TagInfoForResource": TagInfoForResourceTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetRegexPatternSetResponseTypeDef = TypedDict(
    "GetRegexPatternSetResponseTypeDef",
    {
        "RegexPatternSet": RegexPatternSetTypeDef,
        "LockToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

AllowActionTypeDef = TypedDict(
    "AllowActionTypeDef",
    {
        "CustomRequestHandling": CustomRequestHandlingTypeDef,
    },
    total=False,
)

CaptchaActionTypeDef = TypedDict(
    "CaptchaActionTypeDef",
    {
        "CustomRequestHandling": CustomRequestHandlingTypeDef,
    },
    total=False,
)

ChallengeActionTypeDef = TypedDict(
    "ChallengeActionTypeDef",
    {
        "CustomRequestHandling": CustomRequestHandlingTypeDef,
    },
    total=False,
)

CountActionTypeDef = TypedDict(
    "CountActionTypeDef",
    {
        "CustomRequestHandling": CustomRequestHandlingTypeDef,
    },
    total=False,
)

BlockActionTypeDef = TypedDict(
    "BlockActionTypeDef",
    {
        "CustomResponse": CustomResponseTypeDef,
    },
    total=False,
)

_RequiredSampledHTTPRequestTypeDef = TypedDict(
    "_RequiredSampledHTTPRequestTypeDef",
    {
        "Request": HTTPRequestTypeDef,
        "Weight": int,
    },
)
_OptionalSampledHTTPRequestTypeDef = TypedDict(
    "_OptionalSampledHTTPRequestTypeDef",
    {
        "Timestamp": datetime,
        "Action": str,
        "RuleNameWithinRuleGroup": str,
        "RequestHeadersInserted": List[HTTPHeaderTypeDef],
        "ResponseCodeSent": int,
        "Labels": List[LabelTypeDef],
        "CaptchaResponse": CaptchaResponseTypeDef,
        "ChallengeResponse": ChallengeResponseTypeDef,
        "OverriddenAction": str,
    },
    total=False,
)

class SampledHTTPRequestTypeDef(
    _RequiredSampledHTTPRequestTypeDef, _OptionalSampledHTTPRequestTypeDef
):
    pass

FieldToMatchTypeDef = TypedDict(
    "FieldToMatchTypeDef",
    {
        "SingleHeader": SingleHeaderTypeDef,
        "SingleQueryArgument": SingleQueryArgumentTypeDef,
        "AllQueryArguments": Mapping[str, Any],
        "UriPath": Mapping[str, Any],
        "QueryString": Mapping[str, Any],
        "Body": BodyTypeDef,
        "Method": Mapping[str, Any],
        "JsonBody": JsonBodyTypeDef,
        "Headers": HeadersTypeDef,
        "Cookies": CookiesTypeDef,
        "HeaderOrder": HeaderOrderTypeDef,
    },
    total=False,
)

GetManagedRuleSetResponseTypeDef = TypedDict(
    "GetManagedRuleSetResponseTypeDef",
    {
        "ManagedRuleSet": ManagedRuleSetTypeDef,
        "LockToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredAWSManagedRulesACFPRuleSetTypeDef = TypedDict(
    "_RequiredAWSManagedRulesACFPRuleSetTypeDef",
    {
        "CreationPath": str,
        "RegistrationPagePath": str,
        "RequestInspection": RequestInspectionACFPTypeDef,
    },
)
_OptionalAWSManagedRulesACFPRuleSetTypeDef = TypedDict(
    "_OptionalAWSManagedRulesACFPRuleSetTypeDef",
    {
        "ResponseInspection": ResponseInspectionTypeDef,
        "EnableRegexInPath": bool,
    },
    total=False,
)

class AWSManagedRulesACFPRuleSetTypeDef(
    _RequiredAWSManagedRulesACFPRuleSetTypeDef, _OptionalAWSManagedRulesACFPRuleSetTypeDef
):
    pass

_RequiredAWSManagedRulesATPRuleSetTypeDef = TypedDict(
    "_RequiredAWSManagedRulesATPRuleSetTypeDef",
    {
        "LoginPath": str,
    },
)
_OptionalAWSManagedRulesATPRuleSetTypeDef = TypedDict(
    "_OptionalAWSManagedRulesATPRuleSetTypeDef",
    {
        "RequestInspection": RequestInspectionTypeDef,
        "ResponseInspection": ResponseInspectionTypeDef,
        "EnableRegexInPath": bool,
    },
    total=False,
)

class AWSManagedRulesATPRuleSetTypeDef(
    _RequiredAWSManagedRulesATPRuleSetTypeDef, _OptionalAWSManagedRulesATPRuleSetTypeDef
):
    pass

_RequiredRateBasedStatementTypeDef = TypedDict(
    "_RequiredRateBasedStatementTypeDef",
    {
        "Limit": int,
        "AggregateKeyType": RateBasedStatementAggregateKeyTypeType,
    },
)
_OptionalRateBasedStatementTypeDef = TypedDict(
    "_OptionalRateBasedStatementTypeDef",
    {
        "ScopeDownStatement": "StatementTypeDef",
        "ForwardedIPConfig": ForwardedIPConfigTypeDef,
        "CustomKeys": Sequence[RateBasedStatementCustomKeyTypeDef],
    },
    total=False,
)

class RateBasedStatementTypeDef(
    _RequiredRateBasedStatementTypeDef, _OptionalRateBasedStatementTypeDef
):
    pass

LoggingFilterTypeDef = TypedDict(
    "LoggingFilterTypeDef",
    {
        "Filters": List[FilterTypeDef],
        "DefaultBehavior": FilterBehaviorType,
    },
)

OverrideActionTypeDef = TypedDict(
    "OverrideActionTypeDef",
    {
        "Count": CountActionTypeDef,
        "None": Mapping[str, Any],
    },
    total=False,
)

DefaultActionTypeDef = TypedDict(
    "DefaultActionTypeDef",
    {
        "Block": BlockActionTypeDef,
        "Allow": AllowActionTypeDef,
    },
    total=False,
)

RuleActionTypeDef = TypedDict(
    "RuleActionTypeDef",
    {
        "Block": BlockActionTypeDef,
        "Allow": AllowActionTypeDef,
        "Count": CountActionTypeDef,
        "Captcha": CaptchaActionTypeDef,
        "Challenge": ChallengeActionTypeDef,
    },
    total=False,
)

GetSampledRequestsResponseTypeDef = TypedDict(
    "GetSampledRequestsResponseTypeDef",
    {
        "SampledRequests": List[SampledHTTPRequestTypeDef],
        "PopulationSize": int,
        "TimeWindow": TimeWindowTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ByteMatchStatementTypeDef = TypedDict(
    "ByteMatchStatementTypeDef",
    {
        "SearchString": Union[str, bytes, IO[Any], StreamingBody],
        "FieldToMatch": FieldToMatchTypeDef,
        "TextTransformations": Sequence[TextTransformationTypeDef],
        "PositionalConstraint": PositionalConstraintType,
    },
)

RegexMatchStatementTypeDef = TypedDict(
    "RegexMatchStatementTypeDef",
    {
        "RegexString": str,
        "FieldToMatch": FieldToMatchTypeDef,
        "TextTransformations": Sequence[TextTransformationTypeDef],
    },
)

RegexPatternSetReferenceStatementTypeDef = TypedDict(
    "RegexPatternSetReferenceStatementTypeDef",
    {
        "ARN": str,
        "FieldToMatch": FieldToMatchTypeDef,
        "TextTransformations": Sequence[TextTransformationTypeDef],
    },
)

SizeConstraintStatementTypeDef = TypedDict(
    "SizeConstraintStatementTypeDef",
    {
        "FieldToMatch": FieldToMatchTypeDef,
        "ComparisonOperator": ComparisonOperatorType,
        "Size": int,
        "TextTransformations": Sequence[TextTransformationTypeDef],
    },
)

_RequiredSqliMatchStatementTypeDef = TypedDict(
    "_RequiredSqliMatchStatementTypeDef",
    {
        "FieldToMatch": FieldToMatchTypeDef,
        "TextTransformations": Sequence[TextTransformationTypeDef],
    },
)
_OptionalSqliMatchStatementTypeDef = TypedDict(
    "_OptionalSqliMatchStatementTypeDef",
    {
        "SensitivityLevel": SensitivityLevelType,
    },
    total=False,
)

class SqliMatchStatementTypeDef(
    _RequiredSqliMatchStatementTypeDef, _OptionalSqliMatchStatementTypeDef
):
    pass

XssMatchStatementTypeDef = TypedDict(
    "XssMatchStatementTypeDef",
    {
        "FieldToMatch": FieldToMatchTypeDef,
        "TextTransformations": Sequence[TextTransformationTypeDef],
    },
)

ManagedRuleGroupConfigTypeDef = TypedDict(
    "ManagedRuleGroupConfigTypeDef",
    {
        "LoginPath": str,
        "PayloadType": PayloadTypeType,
        "UsernameField": UsernameFieldTypeDef,
        "PasswordField": PasswordFieldTypeDef,
        "AWSManagedRulesBotControlRuleSet": AWSManagedRulesBotControlRuleSetTypeDef,
        "AWSManagedRulesATPRuleSet": AWSManagedRulesATPRuleSetTypeDef,
        "AWSManagedRulesACFPRuleSet": AWSManagedRulesACFPRuleSetTypeDef,
    },
    total=False,
)

_RequiredLoggingConfigurationTypeDef = TypedDict(
    "_RequiredLoggingConfigurationTypeDef",
    {
        "ResourceArn": str,
        "LogDestinationConfigs": List[str],
    },
)
_OptionalLoggingConfigurationTypeDef = TypedDict(
    "_OptionalLoggingConfigurationTypeDef",
    {
        "RedactedFields": List[FieldToMatchTypeDef],
        "ManagedByFirewallManager": bool,
        "LoggingFilter": LoggingFilterTypeDef,
    },
    total=False,
)

class LoggingConfigurationTypeDef(
    _RequiredLoggingConfigurationTypeDef, _OptionalLoggingConfigurationTypeDef
):
    pass

RuleActionOverrideTypeDef = TypedDict(
    "RuleActionOverrideTypeDef",
    {
        "Name": str,
        "ActionToUse": RuleActionTypeDef,
    },
)

RuleSummaryTypeDef = TypedDict(
    "RuleSummaryTypeDef",
    {
        "Name": str,
        "Action": RuleActionTypeDef,
    },
    total=False,
)

_RequiredRuleTypeDef = TypedDict(
    "_RequiredRuleTypeDef",
    {
        "Name": str,
        "Priority": int,
        "Statement": "StatementTypeDef",
        "VisibilityConfig": VisibilityConfigTypeDef,
    },
)
_OptionalRuleTypeDef = TypedDict(
    "_OptionalRuleTypeDef",
    {
        "Action": RuleActionTypeDef,
        "OverrideAction": OverrideActionTypeDef,
        "RuleLabels": Sequence[LabelTypeDef],
        "CaptchaConfig": CaptchaConfigTypeDef,
        "ChallengeConfig": ChallengeConfigTypeDef,
    },
    total=False,
)

class RuleTypeDef(_RequiredRuleTypeDef, _OptionalRuleTypeDef):
    pass

GetLoggingConfigurationResponseTypeDef = TypedDict(
    "GetLoggingConfigurationResponseTypeDef",
    {
        "LoggingConfiguration": LoggingConfigurationTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListLoggingConfigurationsResponseTypeDef = TypedDict(
    "ListLoggingConfigurationsResponseTypeDef",
    {
        "LoggingConfigurations": List[LoggingConfigurationTypeDef],
        "NextMarker": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

PutLoggingConfigurationRequestRequestTypeDef = TypedDict(
    "PutLoggingConfigurationRequestRequestTypeDef",
    {
        "LoggingConfiguration": LoggingConfigurationTypeDef,
    },
)

PutLoggingConfigurationResponseTypeDef = TypedDict(
    "PutLoggingConfigurationResponseTypeDef",
    {
        "LoggingConfiguration": LoggingConfigurationTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredManagedRuleGroupStatementTypeDef = TypedDict(
    "_RequiredManagedRuleGroupStatementTypeDef",
    {
        "VendorName": str,
        "Name": str,
    },
)
_OptionalManagedRuleGroupStatementTypeDef = TypedDict(
    "_OptionalManagedRuleGroupStatementTypeDef",
    {
        "Version": str,
        "ExcludedRules": Sequence[ExcludedRuleTypeDef],
        "ScopeDownStatement": "StatementTypeDef",
        "ManagedRuleGroupConfigs": Sequence[ManagedRuleGroupConfigTypeDef],
        "RuleActionOverrides": Sequence[RuleActionOverrideTypeDef],
    },
    total=False,
)

class ManagedRuleGroupStatementTypeDef(
    _RequiredManagedRuleGroupStatementTypeDef, _OptionalManagedRuleGroupStatementTypeDef
):
    pass

_RequiredRuleGroupReferenceStatementTypeDef = TypedDict(
    "_RequiredRuleGroupReferenceStatementTypeDef",
    {
        "ARN": str,
    },
)
_OptionalRuleGroupReferenceStatementTypeDef = TypedDict(
    "_OptionalRuleGroupReferenceStatementTypeDef",
    {
        "ExcludedRules": Sequence[ExcludedRuleTypeDef],
        "RuleActionOverrides": Sequence[RuleActionOverrideTypeDef],
    },
    total=False,
)

class RuleGroupReferenceStatementTypeDef(
    _RequiredRuleGroupReferenceStatementTypeDef, _OptionalRuleGroupReferenceStatementTypeDef
):
    pass

DescribeManagedRuleGroupResponseTypeDef = TypedDict(
    "DescribeManagedRuleGroupResponseTypeDef",
    {
        "VersionName": str,
        "SnsTopicArn": str,
        "Capacity": int,
        "Rules": List[RuleSummaryTypeDef],
        "LabelNamespace": str,
        "AvailableLabels": List[LabelSummaryTypeDef],
        "ConsumedLabels": List[LabelSummaryTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CheckCapacityRequestRequestTypeDef = TypedDict(
    "CheckCapacityRequestRequestTypeDef",
    {
        "Scope": ScopeType,
        "Rules": Sequence[RuleTypeDef],
    },
)

_RequiredCreateRuleGroupRequestRequestTypeDef = TypedDict(
    "_RequiredCreateRuleGroupRequestRequestTypeDef",
    {
        "Name": str,
        "Scope": ScopeType,
        "Capacity": int,
        "VisibilityConfig": VisibilityConfigTypeDef,
    },
)
_OptionalCreateRuleGroupRequestRequestTypeDef = TypedDict(
    "_OptionalCreateRuleGroupRequestRequestTypeDef",
    {
        "Description": str,
        "Rules": Sequence[RuleTypeDef],
        "Tags": Sequence[TagTypeDef],
        "CustomResponseBodies": Mapping[str, CustomResponseBodyTypeDef],
    },
    total=False,
)

class CreateRuleGroupRequestRequestTypeDef(
    _RequiredCreateRuleGroupRequestRequestTypeDef, _OptionalCreateRuleGroupRequestRequestTypeDef
):
    pass

_RequiredCreateWebACLRequestRequestTypeDef = TypedDict(
    "_RequiredCreateWebACLRequestRequestTypeDef",
    {
        "Name": str,
        "Scope": ScopeType,
        "DefaultAction": DefaultActionTypeDef,
        "VisibilityConfig": VisibilityConfigTypeDef,
    },
)
_OptionalCreateWebACLRequestRequestTypeDef = TypedDict(
    "_OptionalCreateWebACLRequestRequestTypeDef",
    {
        "Description": str,
        "Rules": Sequence[RuleTypeDef],
        "Tags": Sequence[TagTypeDef],
        "CustomResponseBodies": Mapping[str, CustomResponseBodyTypeDef],
        "CaptchaConfig": CaptchaConfigTypeDef,
        "ChallengeConfig": ChallengeConfigTypeDef,
        "TokenDomains": Sequence[str],
        "AssociationConfig": AssociationConfigTypeDef,
    },
    total=False,
)

class CreateWebACLRequestRequestTypeDef(
    _RequiredCreateWebACLRequestRequestTypeDef, _OptionalCreateWebACLRequestRequestTypeDef
):
    pass

_RequiredRuleGroupTypeDef = TypedDict(
    "_RequiredRuleGroupTypeDef",
    {
        "Name": str,
        "Id": str,
        "Capacity": int,
        "ARN": str,
        "VisibilityConfig": VisibilityConfigTypeDef,
    },
)
_OptionalRuleGroupTypeDef = TypedDict(
    "_OptionalRuleGroupTypeDef",
    {
        "Description": str,
        "Rules": List[RuleTypeDef],
        "LabelNamespace": str,
        "CustomResponseBodies": Dict[str, CustomResponseBodyTypeDef],
        "AvailableLabels": List[LabelSummaryTypeDef],
        "ConsumedLabels": List[LabelSummaryTypeDef],
    },
    total=False,
)

class RuleGroupTypeDef(_RequiredRuleGroupTypeDef, _OptionalRuleGroupTypeDef):
    pass

_RequiredUpdateRuleGroupRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateRuleGroupRequestRequestTypeDef",
    {
        "Name": str,
        "Scope": ScopeType,
        "Id": str,
        "VisibilityConfig": VisibilityConfigTypeDef,
        "LockToken": str,
    },
)
_OptionalUpdateRuleGroupRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateRuleGroupRequestRequestTypeDef",
    {
        "Description": str,
        "Rules": Sequence[RuleTypeDef],
        "CustomResponseBodies": Mapping[str, CustomResponseBodyTypeDef],
    },
    total=False,
)

class UpdateRuleGroupRequestRequestTypeDef(
    _RequiredUpdateRuleGroupRequestRequestTypeDef, _OptionalUpdateRuleGroupRequestRequestTypeDef
):
    pass

_RequiredUpdateWebACLRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateWebACLRequestRequestTypeDef",
    {
        "Name": str,
        "Scope": ScopeType,
        "Id": str,
        "DefaultAction": DefaultActionTypeDef,
        "VisibilityConfig": VisibilityConfigTypeDef,
        "LockToken": str,
    },
)
_OptionalUpdateWebACLRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateWebACLRequestRequestTypeDef",
    {
        "Description": str,
        "Rules": Sequence[RuleTypeDef],
        "CustomResponseBodies": Mapping[str, CustomResponseBodyTypeDef],
        "CaptchaConfig": CaptchaConfigTypeDef,
        "ChallengeConfig": ChallengeConfigTypeDef,
        "TokenDomains": Sequence[str],
        "AssociationConfig": AssociationConfigTypeDef,
    },
    total=False,
)

class UpdateWebACLRequestRequestTypeDef(
    _RequiredUpdateWebACLRequestRequestTypeDef, _OptionalUpdateWebACLRequestRequestTypeDef
):
    pass

FirewallManagerStatementTypeDef = TypedDict(
    "FirewallManagerStatementTypeDef",
    {
        "ManagedRuleGroupStatement": ManagedRuleGroupStatementTypeDef,
        "RuleGroupReferenceStatement": RuleGroupReferenceStatementTypeDef,
    },
    total=False,
)

StatementTypeDef = TypedDict(
    "StatementTypeDef",
    {
        "ByteMatchStatement": ByteMatchStatementTypeDef,
        "SqliMatchStatement": SqliMatchStatementTypeDef,
        "XssMatchStatement": XssMatchStatementTypeDef,
        "SizeConstraintStatement": SizeConstraintStatementTypeDef,
        "GeoMatchStatement": GeoMatchStatementTypeDef,
        "RuleGroupReferenceStatement": RuleGroupReferenceStatementTypeDef,
        "IPSetReferenceStatement": IPSetReferenceStatementTypeDef,
        "RegexPatternSetReferenceStatement": RegexPatternSetReferenceStatementTypeDef,
        "RateBasedStatement": Dict[str, Any],
        "AndStatement": Dict[str, Any],
        "OrStatement": Dict[str, Any],
        "NotStatement": Dict[str, Any],
        "ManagedRuleGroupStatement": Dict[str, Any],
        "LabelMatchStatement": LabelMatchStatementTypeDef,
        "RegexMatchStatement": RegexMatchStatementTypeDef,
    },
    total=False,
)

GetRuleGroupResponseTypeDef = TypedDict(
    "GetRuleGroupResponseTypeDef",
    {
        "RuleGroup": RuleGroupTypeDef,
        "LockToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

FirewallManagerRuleGroupTypeDef = TypedDict(
    "FirewallManagerRuleGroupTypeDef",
    {
        "Name": str,
        "Priority": int,
        "FirewallManagerStatement": FirewallManagerStatementTypeDef,
        "OverrideAction": OverrideActionTypeDef,
        "VisibilityConfig": VisibilityConfigTypeDef,
    },
)

_RequiredWebACLTypeDef = TypedDict(
    "_RequiredWebACLTypeDef",
    {
        "Name": str,
        "Id": str,
        "ARN": str,
        "DefaultAction": DefaultActionTypeDef,
        "VisibilityConfig": VisibilityConfigTypeDef,
    },
)
_OptionalWebACLTypeDef = TypedDict(
    "_OptionalWebACLTypeDef",
    {
        "Description": str,
        "Rules": List[RuleTypeDef],
        "Capacity": int,
        "PreProcessFirewallManagerRuleGroups": List[FirewallManagerRuleGroupTypeDef],
        "PostProcessFirewallManagerRuleGroups": List[FirewallManagerRuleGroupTypeDef],
        "ManagedByFirewallManager": bool,
        "LabelNamespace": str,
        "CustomResponseBodies": Dict[str, CustomResponseBodyTypeDef],
        "CaptchaConfig": CaptchaConfigTypeDef,
        "ChallengeConfig": ChallengeConfigTypeDef,
        "TokenDomains": List[str],
        "AssociationConfig": AssociationConfigTypeDef,
    },
    total=False,
)

class WebACLTypeDef(_RequiredWebACLTypeDef, _OptionalWebACLTypeDef):
    pass

GetWebACLForResourceResponseTypeDef = TypedDict(
    "GetWebACLForResourceResponseTypeDef",
    {
        "WebACL": WebACLTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetWebACLResponseTypeDef = TypedDict(
    "GetWebACLResponseTypeDef",
    {
        "WebACL": WebACLTypeDef,
        "LockToken": str,
        "ApplicationIntegrationURL": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)
