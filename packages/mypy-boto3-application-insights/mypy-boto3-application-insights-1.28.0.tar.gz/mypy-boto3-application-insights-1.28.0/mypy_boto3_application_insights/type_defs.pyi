"""
Type annotations for application-insights service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_insights/type_defs/)

Usage::

    ```python
    from mypy_boto3_application_insights.type_defs import ApplicationComponentTypeDef

    data: ApplicationComponentTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence, Union

from .literals import (
    CloudWatchEventSourceType,
    ConfigurationEventResourceTypeType,
    ConfigurationEventStatusType,
    DiscoveryTypeType,
    FeedbackValueType,
    LogFilterType,
    OsTypeType,
    SeverityLevelType,
    StatusType,
    TierType,
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
    "ApplicationComponentTypeDef",
    "ApplicationInfoTypeDef",
    "ConfigurationEventTypeDef",
    "TagTypeDef",
    "CreateComponentRequestRequestTypeDef",
    "CreateLogPatternRequestRequestTypeDef",
    "LogPatternTypeDef",
    "DeleteApplicationRequestRequestTypeDef",
    "DeleteComponentRequestRequestTypeDef",
    "DeleteLogPatternRequestRequestTypeDef",
    "DescribeApplicationRequestRequestTypeDef",
    "DescribeComponentConfigurationRecommendationRequestRequestTypeDef",
    "DescribeComponentConfigurationRecommendationResponseTypeDef",
    "DescribeComponentConfigurationRequestRequestTypeDef",
    "DescribeComponentConfigurationResponseTypeDef",
    "DescribeComponentRequestRequestTypeDef",
    "DescribeLogPatternRequestRequestTypeDef",
    "DescribeObservationRequestRequestTypeDef",
    "ObservationTypeDef",
    "DescribeProblemObservationsRequestRequestTypeDef",
    "DescribeProblemRequestRequestTypeDef",
    "ProblemTypeDef",
    "ListApplicationsRequestRequestTypeDef",
    "ListComponentsRequestRequestTypeDef",
    "ListConfigurationHistoryRequestRequestTypeDef",
    "ListLogPatternSetsRequestRequestTypeDef",
    "ListLogPatternSetsResponseTypeDef",
    "ListLogPatternsRequestRequestTypeDef",
    "ListProblemsRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateApplicationRequestRequestTypeDef",
    "UpdateComponentConfigurationRequestRequestTypeDef",
    "UpdateComponentRequestRequestTypeDef",
    "UpdateLogPatternRequestRequestTypeDef",
    "DescribeComponentResponseTypeDef",
    "ListComponentsResponseTypeDef",
    "CreateApplicationResponseTypeDef",
    "DescribeApplicationResponseTypeDef",
    "ListApplicationsResponseTypeDef",
    "UpdateApplicationResponseTypeDef",
    "ListConfigurationHistoryResponseTypeDef",
    "CreateApplicationRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "CreateLogPatternResponseTypeDef",
    "DescribeLogPatternResponseTypeDef",
    "ListLogPatternsResponseTypeDef",
    "UpdateLogPatternResponseTypeDef",
    "DescribeObservationResponseTypeDef",
    "RelatedObservationsTypeDef",
    "DescribeProblemResponseTypeDef",
    "ListProblemsResponseTypeDef",
    "DescribeProblemObservationsResponseTypeDef",
)

ApplicationComponentTypeDef = TypedDict(
    "ApplicationComponentTypeDef",
    {
        "ComponentName": str,
        "ComponentRemarks": str,
        "ResourceType": str,
        "OsType": OsTypeType,
        "Tier": TierType,
        "Monitor": bool,
        "DetectedWorkload": Dict[TierType, Dict[str, str]],
    },
    total=False,
)

ApplicationInfoTypeDef = TypedDict(
    "ApplicationInfoTypeDef",
    {
        "ResourceGroupName": str,
        "LifeCycle": str,
        "OpsItemSNSTopicArn": str,
        "OpsCenterEnabled": bool,
        "CWEMonitorEnabled": bool,
        "Remarks": str,
        "AutoConfigEnabled": bool,
        "DiscoveryType": DiscoveryTypeType,
    },
    total=False,
)

ConfigurationEventTypeDef = TypedDict(
    "ConfigurationEventTypeDef",
    {
        "MonitoredResourceARN": str,
        "EventStatus": ConfigurationEventStatusType,
        "EventResourceType": ConfigurationEventResourceTypeType,
        "EventTime": datetime,
        "EventDetail": str,
        "EventResourceName": str,
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

CreateComponentRequestRequestTypeDef = TypedDict(
    "CreateComponentRequestRequestTypeDef",
    {
        "ResourceGroupName": str,
        "ComponentName": str,
        "ResourceList": Sequence[str],
    },
)

CreateLogPatternRequestRequestTypeDef = TypedDict(
    "CreateLogPatternRequestRequestTypeDef",
    {
        "ResourceGroupName": str,
        "PatternSetName": str,
        "PatternName": str,
        "Pattern": str,
        "Rank": int,
    },
)

LogPatternTypeDef = TypedDict(
    "LogPatternTypeDef",
    {
        "PatternSetName": str,
        "PatternName": str,
        "Pattern": str,
        "Rank": int,
    },
    total=False,
)

DeleteApplicationRequestRequestTypeDef = TypedDict(
    "DeleteApplicationRequestRequestTypeDef",
    {
        "ResourceGroupName": str,
    },
)

DeleteComponentRequestRequestTypeDef = TypedDict(
    "DeleteComponentRequestRequestTypeDef",
    {
        "ResourceGroupName": str,
        "ComponentName": str,
    },
)

DeleteLogPatternRequestRequestTypeDef = TypedDict(
    "DeleteLogPatternRequestRequestTypeDef",
    {
        "ResourceGroupName": str,
        "PatternSetName": str,
        "PatternName": str,
    },
)

DescribeApplicationRequestRequestTypeDef = TypedDict(
    "DescribeApplicationRequestRequestTypeDef",
    {
        "ResourceGroupName": str,
    },
)

DescribeComponentConfigurationRecommendationRequestRequestTypeDef = TypedDict(
    "DescribeComponentConfigurationRecommendationRequestRequestTypeDef",
    {
        "ResourceGroupName": str,
        "ComponentName": str,
        "Tier": TierType,
    },
)

DescribeComponentConfigurationRecommendationResponseTypeDef = TypedDict(
    "DescribeComponentConfigurationRecommendationResponseTypeDef",
    {
        "ComponentConfiguration": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeComponentConfigurationRequestRequestTypeDef = TypedDict(
    "DescribeComponentConfigurationRequestRequestTypeDef",
    {
        "ResourceGroupName": str,
        "ComponentName": str,
    },
)

DescribeComponentConfigurationResponseTypeDef = TypedDict(
    "DescribeComponentConfigurationResponseTypeDef",
    {
        "Monitor": bool,
        "Tier": TierType,
        "ComponentConfiguration": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeComponentRequestRequestTypeDef = TypedDict(
    "DescribeComponentRequestRequestTypeDef",
    {
        "ResourceGroupName": str,
        "ComponentName": str,
    },
)

DescribeLogPatternRequestRequestTypeDef = TypedDict(
    "DescribeLogPatternRequestRequestTypeDef",
    {
        "ResourceGroupName": str,
        "PatternSetName": str,
        "PatternName": str,
    },
)

DescribeObservationRequestRequestTypeDef = TypedDict(
    "DescribeObservationRequestRequestTypeDef",
    {
        "ObservationId": str,
    },
)

ObservationTypeDef = TypedDict(
    "ObservationTypeDef",
    {
        "Id": str,
        "StartTime": datetime,
        "EndTime": datetime,
        "SourceType": str,
        "SourceARN": str,
        "LogGroup": str,
        "LineTime": datetime,
        "LogText": str,
        "LogFilter": LogFilterType,
        "MetricNamespace": str,
        "MetricName": str,
        "Unit": str,
        "Value": float,
        "CloudWatchEventId": str,
        "CloudWatchEventSource": CloudWatchEventSourceType,
        "CloudWatchEventDetailType": str,
        "HealthEventArn": str,
        "HealthService": str,
        "HealthEventTypeCode": str,
        "HealthEventTypeCategory": str,
        "HealthEventDescription": str,
        "CodeDeployDeploymentId": str,
        "CodeDeployDeploymentGroup": str,
        "CodeDeployState": str,
        "CodeDeployApplication": str,
        "CodeDeployInstanceGroupId": str,
        "Ec2State": str,
        "RdsEventCategories": str,
        "RdsEventMessage": str,
        "S3EventName": str,
        "StatesExecutionArn": str,
        "StatesArn": str,
        "StatesStatus": str,
        "StatesInput": str,
        "EbsEvent": str,
        "EbsResult": str,
        "EbsCause": str,
        "EbsRequestId": str,
        "XRayFaultPercent": int,
        "XRayThrottlePercent": int,
        "XRayErrorPercent": int,
        "XRayRequestCount": int,
        "XRayRequestAverageLatency": int,
        "XRayNodeName": str,
        "XRayNodeType": str,
    },
    total=False,
)

DescribeProblemObservationsRequestRequestTypeDef = TypedDict(
    "DescribeProblemObservationsRequestRequestTypeDef",
    {
        "ProblemId": str,
    },
)

DescribeProblemRequestRequestTypeDef = TypedDict(
    "DescribeProblemRequestRequestTypeDef",
    {
        "ProblemId": str,
    },
)

ProblemTypeDef = TypedDict(
    "ProblemTypeDef",
    {
        "Id": str,
        "Title": str,
        "Insights": str,
        "Status": StatusType,
        "AffectedResource": str,
        "StartTime": datetime,
        "EndTime": datetime,
        "SeverityLevel": SeverityLevelType,
        "ResourceGroupName": str,
        "Feedback": Dict[Literal["INSIGHTS_FEEDBACK"], FeedbackValueType],
        "RecurringCount": int,
        "LastRecurrenceTime": datetime,
    },
    total=False,
)

ListApplicationsRequestRequestTypeDef = TypedDict(
    "ListApplicationsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

_RequiredListComponentsRequestRequestTypeDef = TypedDict(
    "_RequiredListComponentsRequestRequestTypeDef",
    {
        "ResourceGroupName": str,
    },
)
_OptionalListComponentsRequestRequestTypeDef = TypedDict(
    "_OptionalListComponentsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

class ListComponentsRequestRequestTypeDef(
    _RequiredListComponentsRequestRequestTypeDef, _OptionalListComponentsRequestRequestTypeDef
):
    pass

ListConfigurationHistoryRequestRequestTypeDef = TypedDict(
    "ListConfigurationHistoryRequestRequestTypeDef",
    {
        "ResourceGroupName": str,
        "StartTime": Union[datetime, str],
        "EndTime": Union[datetime, str],
        "EventStatus": ConfigurationEventStatusType,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

_RequiredListLogPatternSetsRequestRequestTypeDef = TypedDict(
    "_RequiredListLogPatternSetsRequestRequestTypeDef",
    {
        "ResourceGroupName": str,
    },
)
_OptionalListLogPatternSetsRequestRequestTypeDef = TypedDict(
    "_OptionalListLogPatternSetsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

class ListLogPatternSetsRequestRequestTypeDef(
    _RequiredListLogPatternSetsRequestRequestTypeDef,
    _OptionalListLogPatternSetsRequestRequestTypeDef,
):
    pass

ListLogPatternSetsResponseTypeDef = TypedDict(
    "ListLogPatternSetsResponseTypeDef",
    {
        "ResourceGroupName": str,
        "LogPatternSets": List[str],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListLogPatternsRequestRequestTypeDef = TypedDict(
    "_RequiredListLogPatternsRequestRequestTypeDef",
    {
        "ResourceGroupName": str,
    },
)
_OptionalListLogPatternsRequestRequestTypeDef = TypedDict(
    "_OptionalListLogPatternsRequestRequestTypeDef",
    {
        "PatternSetName": str,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

class ListLogPatternsRequestRequestTypeDef(
    _RequiredListLogPatternsRequestRequestTypeDef, _OptionalListLogPatternsRequestRequestTypeDef
):
    pass

ListProblemsRequestRequestTypeDef = TypedDict(
    "ListProblemsRequestRequestTypeDef",
    {
        "ResourceGroupName": str,
        "StartTime": Union[datetime, str],
        "EndTime": Union[datetime, str],
        "MaxResults": int,
        "NextToken": str,
        "ComponentName": str,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceARN": str,
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

_RequiredUpdateApplicationRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateApplicationRequestRequestTypeDef",
    {
        "ResourceGroupName": str,
    },
)
_OptionalUpdateApplicationRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateApplicationRequestRequestTypeDef",
    {
        "OpsCenterEnabled": bool,
        "CWEMonitorEnabled": bool,
        "OpsItemSNSTopicArn": str,
        "RemoveSNSTopic": bool,
        "AutoConfigEnabled": bool,
    },
    total=False,
)

class UpdateApplicationRequestRequestTypeDef(
    _RequiredUpdateApplicationRequestRequestTypeDef, _OptionalUpdateApplicationRequestRequestTypeDef
):
    pass

_RequiredUpdateComponentConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateComponentConfigurationRequestRequestTypeDef",
    {
        "ResourceGroupName": str,
        "ComponentName": str,
    },
)
_OptionalUpdateComponentConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateComponentConfigurationRequestRequestTypeDef",
    {
        "Monitor": bool,
        "Tier": TierType,
        "ComponentConfiguration": str,
        "AutoConfigEnabled": bool,
    },
    total=False,
)

class UpdateComponentConfigurationRequestRequestTypeDef(
    _RequiredUpdateComponentConfigurationRequestRequestTypeDef,
    _OptionalUpdateComponentConfigurationRequestRequestTypeDef,
):
    pass

_RequiredUpdateComponentRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateComponentRequestRequestTypeDef",
    {
        "ResourceGroupName": str,
        "ComponentName": str,
    },
)
_OptionalUpdateComponentRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateComponentRequestRequestTypeDef",
    {
        "NewComponentName": str,
        "ResourceList": Sequence[str],
    },
    total=False,
)

class UpdateComponentRequestRequestTypeDef(
    _RequiredUpdateComponentRequestRequestTypeDef, _OptionalUpdateComponentRequestRequestTypeDef
):
    pass

_RequiredUpdateLogPatternRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateLogPatternRequestRequestTypeDef",
    {
        "ResourceGroupName": str,
        "PatternSetName": str,
        "PatternName": str,
    },
)
_OptionalUpdateLogPatternRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateLogPatternRequestRequestTypeDef",
    {
        "Pattern": str,
        "Rank": int,
    },
    total=False,
)

class UpdateLogPatternRequestRequestTypeDef(
    _RequiredUpdateLogPatternRequestRequestTypeDef, _OptionalUpdateLogPatternRequestRequestTypeDef
):
    pass

DescribeComponentResponseTypeDef = TypedDict(
    "DescribeComponentResponseTypeDef",
    {
        "ApplicationComponent": ApplicationComponentTypeDef,
        "ResourceList": List[str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListComponentsResponseTypeDef = TypedDict(
    "ListComponentsResponseTypeDef",
    {
        "ApplicationComponentList": List[ApplicationComponentTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateApplicationResponseTypeDef = TypedDict(
    "CreateApplicationResponseTypeDef",
    {
        "ApplicationInfo": ApplicationInfoTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeApplicationResponseTypeDef = TypedDict(
    "DescribeApplicationResponseTypeDef",
    {
        "ApplicationInfo": ApplicationInfoTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListApplicationsResponseTypeDef = TypedDict(
    "ListApplicationsResponseTypeDef",
    {
        "ApplicationInfoList": List[ApplicationInfoTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateApplicationResponseTypeDef = TypedDict(
    "UpdateApplicationResponseTypeDef",
    {
        "ApplicationInfo": ApplicationInfoTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListConfigurationHistoryResponseTypeDef = TypedDict(
    "ListConfigurationHistoryResponseTypeDef",
    {
        "EventList": List[ConfigurationEventTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateApplicationRequestRequestTypeDef = TypedDict(
    "CreateApplicationRequestRequestTypeDef",
    {
        "ResourceGroupName": str,
        "OpsCenterEnabled": bool,
        "CWEMonitorEnabled": bool,
        "OpsItemSNSTopicArn": str,
        "Tags": Sequence[TagTypeDef],
        "AutoConfigEnabled": bool,
        "AutoCreate": bool,
        "GroupingType": Literal["ACCOUNT_BASED"],
    },
    total=False,
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
        "ResourceARN": str,
        "Tags": Sequence[TagTypeDef],
    },
)

CreateLogPatternResponseTypeDef = TypedDict(
    "CreateLogPatternResponseTypeDef",
    {
        "LogPattern": LogPatternTypeDef,
        "ResourceGroupName": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeLogPatternResponseTypeDef = TypedDict(
    "DescribeLogPatternResponseTypeDef",
    {
        "ResourceGroupName": str,
        "LogPattern": LogPatternTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListLogPatternsResponseTypeDef = TypedDict(
    "ListLogPatternsResponseTypeDef",
    {
        "ResourceGroupName": str,
        "LogPatterns": List[LogPatternTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateLogPatternResponseTypeDef = TypedDict(
    "UpdateLogPatternResponseTypeDef",
    {
        "ResourceGroupName": str,
        "LogPattern": LogPatternTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeObservationResponseTypeDef = TypedDict(
    "DescribeObservationResponseTypeDef",
    {
        "Observation": ObservationTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

RelatedObservationsTypeDef = TypedDict(
    "RelatedObservationsTypeDef",
    {
        "ObservationList": List[ObservationTypeDef],
    },
    total=False,
)

DescribeProblemResponseTypeDef = TypedDict(
    "DescribeProblemResponseTypeDef",
    {
        "Problem": ProblemTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListProblemsResponseTypeDef = TypedDict(
    "ListProblemsResponseTypeDef",
    {
        "ProblemList": List[ProblemTypeDef],
        "NextToken": str,
        "ResourceGroupName": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeProblemObservationsResponseTypeDef = TypedDict(
    "DescribeProblemObservationsResponseTypeDef",
    {
        "RelatedObservations": RelatedObservationsTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)
