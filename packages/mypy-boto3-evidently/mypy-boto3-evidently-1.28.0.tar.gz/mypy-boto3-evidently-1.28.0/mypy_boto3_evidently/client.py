"""
Type annotations for evidently service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evidently/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_evidently.client import CloudWatchEvidentlyClient

    session = Session()
    client: CloudWatchEvidentlyClient = session.client("evidently")
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, Mapping, Sequence, Type, Union, overload

from botocore.client import BaseClient, ClientMeta

from .literals import (
    ExperimentResultRequestTypeType,
    ExperimentStatusType,
    ExperimentStopDesiredStateType,
    FeatureEvaluationStrategyType,
    LaunchStatusType,
    LaunchStopDesiredStateType,
    SegmentReferenceResourceTypeType,
)
from .paginator import (
    ListExperimentsPaginator,
    ListFeaturesPaginator,
    ListLaunchesPaginator,
    ListProjectsPaginator,
    ListSegmentReferencesPaginator,
    ListSegmentsPaginator,
)
from .type_defs import (
    BatchEvaluateFeatureResponseTypeDef,
    CloudWatchLogsDestinationConfigTypeDef,
    CreateExperimentResponseTypeDef,
    CreateFeatureResponseTypeDef,
    CreateLaunchResponseTypeDef,
    CreateProjectResponseTypeDef,
    CreateSegmentResponseTypeDef,
    EvaluateFeatureResponseTypeDef,
    EvaluationRequestTypeDef,
    EventTypeDef,
    GetExperimentResponseTypeDef,
    GetExperimentResultsResponseTypeDef,
    GetFeatureResponseTypeDef,
    GetLaunchResponseTypeDef,
    GetProjectResponseTypeDef,
    GetSegmentResponseTypeDef,
    LaunchGroupConfigTypeDef,
    ListExperimentsResponseTypeDef,
    ListFeaturesResponseTypeDef,
    ListLaunchesResponseTypeDef,
    ListProjectsResponseTypeDef,
    ListSegmentReferencesResponseTypeDef,
    ListSegmentsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    MetricGoalConfigTypeDef,
    MetricMonitorConfigTypeDef,
    OnlineAbConfigTypeDef,
    ProjectAppConfigResourceConfigTypeDef,
    ProjectDataDeliveryConfigTypeDef,
    PutProjectEventsResponseTypeDef,
    S3DestinationConfigTypeDef,
    ScheduledSplitsLaunchConfigTypeDef,
    StartExperimentResponseTypeDef,
    StartLaunchResponseTypeDef,
    StopExperimentResponseTypeDef,
    StopLaunchResponseTypeDef,
    TestSegmentPatternResponseTypeDef,
    TreatmentConfigTypeDef,
    UpdateExperimentResponseTypeDef,
    UpdateFeatureResponseTypeDef,
    UpdateLaunchResponseTypeDef,
    UpdateProjectDataDeliveryResponseTypeDef,
    UpdateProjectResponseTypeDef,
    VariationConfigTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("CloudWatchEvidentlyClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class CloudWatchEvidentlyClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evidently/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CloudWatchEvidentlyClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evidently/client/#exceptions)
        """

    def batch_evaluate_feature(
        self, *, project: str, requests: Sequence[EvaluationRequestTypeDef]
    ) -> BatchEvaluateFeatureResponseTypeDef:
        """
        This operation assigns feature variation to user sessions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Client.batch_evaluate_feature)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evidently/client/#batch_evaluate_feature)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evidently/client/#can_paginate)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Client.close)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evidently/client/#close)
        """

    def create_experiment(
        self,
        *,
        metricGoals: Sequence[MetricGoalConfigTypeDef],
        name: str,
        project: str,
        treatments: Sequence[TreatmentConfigTypeDef],
        description: str = ...,
        onlineAbConfig: OnlineAbConfigTypeDef = ...,
        randomizationSalt: str = ...,
        samplingRate: int = ...,
        segment: str = ...,
        tags: Mapping[str, str] = ...
    ) -> CreateExperimentResponseTypeDef:
        """
        Creates an Evidently *experiment*.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Client.create_experiment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evidently/client/#create_experiment)
        """

    def create_feature(
        self,
        *,
        name: str,
        project: str,
        variations: Sequence[VariationConfigTypeDef],
        defaultVariation: str = ...,
        description: str = ...,
        entityOverrides: Mapping[str, str] = ...,
        evaluationStrategy: FeatureEvaluationStrategyType = ...,
        tags: Mapping[str, str] = ...
    ) -> CreateFeatureResponseTypeDef:
        """
        Creates an Evidently *feature* that you want to launch or test.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Client.create_feature)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evidently/client/#create_feature)
        """

    def create_launch(
        self,
        *,
        groups: Sequence[LaunchGroupConfigTypeDef],
        name: str,
        project: str,
        description: str = ...,
        metricMonitors: Sequence[MetricMonitorConfigTypeDef] = ...,
        randomizationSalt: str = ...,
        scheduledSplitsConfig: ScheduledSplitsLaunchConfigTypeDef = ...,
        tags: Mapping[str, str] = ...
    ) -> CreateLaunchResponseTypeDef:
        """
        Creates a *launch* of a given feature.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Client.create_launch)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evidently/client/#create_launch)
        """

    def create_project(
        self,
        *,
        name: str,
        appConfigResource: ProjectAppConfigResourceConfigTypeDef = ...,
        dataDelivery: ProjectDataDeliveryConfigTypeDef = ...,
        description: str = ...,
        tags: Mapping[str, str] = ...
    ) -> CreateProjectResponseTypeDef:
        """
        Creates a project, which is the logical object in Evidently that can contain
        features, launches, and experiments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Client.create_project)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evidently/client/#create_project)
        """

    def create_segment(
        self, *, name: str, pattern: str, description: str = ..., tags: Mapping[str, str] = ...
    ) -> CreateSegmentResponseTypeDef:
        """
        Use this operation to define a *segment* of your audience.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Client.create_segment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evidently/client/#create_segment)
        """

    def delete_experiment(self, *, experiment: str, project: str) -> Dict[str, Any]:
        """
        Deletes an Evidently experiment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Client.delete_experiment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evidently/client/#delete_experiment)
        """

    def delete_feature(self, *, feature: str, project: str) -> Dict[str, Any]:
        """
        Deletes an Evidently feature.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Client.delete_feature)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evidently/client/#delete_feature)
        """

    def delete_launch(self, *, launch: str, project: str) -> Dict[str, Any]:
        """
        Deletes an Evidently launch.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Client.delete_launch)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evidently/client/#delete_launch)
        """

    def delete_project(self, *, project: str) -> Dict[str, Any]:
        """
        Deletes an Evidently project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Client.delete_project)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evidently/client/#delete_project)
        """

    def delete_segment(self, *, segment: str) -> Dict[str, Any]:
        """
        Deletes a segment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Client.delete_segment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evidently/client/#delete_segment)
        """

    def evaluate_feature(
        self, *, entityId: str, feature: str, project: str, evaluationContext: str = ...
    ) -> EvaluateFeatureResponseTypeDef:
        """
        This operation assigns a feature variation to one given user session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Client.evaluate_feature)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evidently/client/#evaluate_feature)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evidently/client/#generate_presigned_url)
        """

    def get_experiment(self, *, experiment: str, project: str) -> GetExperimentResponseTypeDef:
        """
        Returns the details about one experiment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Client.get_experiment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evidently/client/#get_experiment)
        """

    def get_experiment_results(
        self,
        *,
        experiment: str,
        metricNames: Sequence[str],
        project: str,
        treatmentNames: Sequence[str],
        baseStat: Literal["Mean"] = ...,
        endTime: Union[datetime, str] = ...,
        period: int = ...,
        reportNames: Sequence[Literal["BayesianInference"]] = ...,
        resultStats: Sequence[ExperimentResultRequestTypeType] = ...,
        startTime: Union[datetime, str] = ...
    ) -> GetExperimentResultsResponseTypeDef:
        """
        Retrieves the results of a running or completed experiment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Client.get_experiment_results)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evidently/client/#get_experiment_results)
        """

    def get_feature(self, *, feature: str, project: str) -> GetFeatureResponseTypeDef:
        """
        Returns the details about one feature.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Client.get_feature)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evidently/client/#get_feature)
        """

    def get_launch(self, *, launch: str, project: str) -> GetLaunchResponseTypeDef:
        """
        Returns the details about one launch.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Client.get_launch)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evidently/client/#get_launch)
        """

    def get_project(self, *, project: str) -> GetProjectResponseTypeDef:
        """
        Returns the details about one launch.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Client.get_project)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evidently/client/#get_project)
        """

    def get_segment(self, *, segment: str) -> GetSegmentResponseTypeDef:
        """
        Returns information about the specified segment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Client.get_segment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evidently/client/#get_segment)
        """

    def list_experiments(
        self,
        *,
        project: str,
        maxResults: int = ...,
        nextToken: str = ...,
        status: ExperimentStatusType = ...
    ) -> ListExperimentsResponseTypeDef:
        """
        Returns configuration details about all the experiments in the specified
        project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Client.list_experiments)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evidently/client/#list_experiments)
        """

    def list_features(
        self, *, project: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListFeaturesResponseTypeDef:
        """
        Returns configuration details about all the features in the specified project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Client.list_features)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evidently/client/#list_features)
        """

    def list_launches(
        self,
        *,
        project: str,
        maxResults: int = ...,
        nextToken: str = ...,
        status: LaunchStatusType = ...
    ) -> ListLaunchesResponseTypeDef:
        """
        Returns configuration details about all the launches in the specified project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Client.list_launches)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evidently/client/#list_launches)
        """

    def list_projects(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListProjectsResponseTypeDef:
        """
        Returns configuration details about all the projects in the current Region in
        your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Client.list_projects)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evidently/client/#list_projects)
        """

    def list_segment_references(
        self,
        *,
        segment: str,
        type: SegmentReferenceResourceTypeType,
        maxResults: int = ...,
        nextToken: str = ...
    ) -> ListSegmentReferencesResponseTypeDef:
        """
        Use this operation to find which experiments or launches are using a specified
        segment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Client.list_segment_references)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evidently/client/#list_segment_references)
        """

    def list_segments(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListSegmentsResponseTypeDef:
        """
        Returns a list of audience segments that you have created in your account in
        this Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Client.list_segments)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evidently/client/#list_segments)
        """

    def list_tags_for_resource(self, *, resourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        Displays the tags associated with an Evidently resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evidently/client/#list_tags_for_resource)
        """

    def put_project_events(
        self, *, events: Sequence[EventTypeDef], project: str
    ) -> PutProjectEventsResponseTypeDef:
        """
        Sends performance events to Evidently.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Client.put_project_events)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evidently/client/#put_project_events)
        """

    def start_experiment(
        self, *, analysisCompleteTime: Union[datetime, str], experiment: str, project: str
    ) -> StartExperimentResponseTypeDef:
        """
        Starts an existing experiment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Client.start_experiment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evidently/client/#start_experiment)
        """

    def start_launch(self, *, launch: str, project: str) -> StartLaunchResponseTypeDef:
        """
        Starts an existing launch.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Client.start_launch)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evidently/client/#start_launch)
        """

    def stop_experiment(
        self,
        *,
        experiment: str,
        project: str,
        desiredState: ExperimentStopDesiredStateType = ...,
        reason: str = ...
    ) -> StopExperimentResponseTypeDef:
        """
        Stops an experiment that is currently running.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Client.stop_experiment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evidently/client/#stop_experiment)
        """

    def stop_launch(
        self,
        *,
        launch: str,
        project: str,
        desiredState: LaunchStopDesiredStateType = ...,
        reason: str = ...
    ) -> StopLaunchResponseTypeDef:
        """
        Stops a launch that is currently running.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Client.stop_launch)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evidently/client/#stop_launch)
        """

    def tag_resource(self, *, resourceArn: str, tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Assigns one or more tags (key-value pairs) to the specified CloudWatch Evidently
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evidently/client/#tag_resource)
        """

    def test_segment_pattern(
        self, *, pattern: str, payload: str
    ) -> TestSegmentPatternResponseTypeDef:
        """
        Use this operation to test a rules pattern that you plan to use to create an
        audience segment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Client.test_segment_pattern)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evidently/client/#test_segment_pattern)
        """

    def untag_resource(self, *, resourceArn: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes one or more tags from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evidently/client/#untag_resource)
        """

    def update_experiment(
        self,
        *,
        experiment: str,
        project: str,
        description: str = ...,
        metricGoals: Sequence[MetricGoalConfigTypeDef] = ...,
        onlineAbConfig: OnlineAbConfigTypeDef = ...,
        randomizationSalt: str = ...,
        removeSegment: bool = ...,
        samplingRate: int = ...,
        segment: str = ...,
        treatments: Sequence[TreatmentConfigTypeDef] = ...
    ) -> UpdateExperimentResponseTypeDef:
        """
        Updates an Evidently experiment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Client.update_experiment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evidently/client/#update_experiment)
        """

    def update_feature(
        self,
        *,
        feature: str,
        project: str,
        addOrUpdateVariations: Sequence[VariationConfigTypeDef] = ...,
        defaultVariation: str = ...,
        description: str = ...,
        entityOverrides: Mapping[str, str] = ...,
        evaluationStrategy: FeatureEvaluationStrategyType = ...,
        removeVariations: Sequence[str] = ...
    ) -> UpdateFeatureResponseTypeDef:
        """
        Updates an existing feature.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Client.update_feature)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evidently/client/#update_feature)
        """

    def update_launch(
        self,
        *,
        launch: str,
        project: str,
        description: str = ...,
        groups: Sequence[LaunchGroupConfigTypeDef] = ...,
        metricMonitors: Sequence[MetricMonitorConfigTypeDef] = ...,
        randomizationSalt: str = ...,
        scheduledSplitsConfig: ScheduledSplitsLaunchConfigTypeDef = ...
    ) -> UpdateLaunchResponseTypeDef:
        """
        Updates a launch of a given feature.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Client.update_launch)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evidently/client/#update_launch)
        """

    def update_project(
        self,
        *,
        project: str,
        appConfigResource: ProjectAppConfigResourceConfigTypeDef = ...,
        description: str = ...
    ) -> UpdateProjectResponseTypeDef:
        """
        Updates the description of an existing project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Client.update_project)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evidently/client/#update_project)
        """

    def update_project_data_delivery(
        self,
        *,
        project: str,
        cloudWatchLogs: CloudWatchLogsDestinationConfigTypeDef = ...,
        s3Destination: S3DestinationConfigTypeDef = ...
    ) -> UpdateProjectDataDeliveryResponseTypeDef:
        """
        Updates the data storage options for this project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Client.update_project_data_delivery)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evidently/client/#update_project_data_delivery)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_experiments"]
    ) -> ListExperimentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evidently/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_features"]) -> ListFeaturesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evidently/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_launches"]) -> ListLaunchesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evidently/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_projects"]) -> ListProjectsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evidently/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_segment_references"]
    ) -> ListSegmentReferencesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evidently/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_segments"]) -> ListSegmentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evidently/client/#get_paginator)
        """
