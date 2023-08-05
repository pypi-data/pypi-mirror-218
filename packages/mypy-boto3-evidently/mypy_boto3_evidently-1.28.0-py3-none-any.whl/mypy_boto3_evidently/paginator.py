"""
Type annotations for evidently service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evidently/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_evidently.client import CloudWatchEvidentlyClient
    from mypy_boto3_evidently.paginator import (
        ListExperimentsPaginator,
        ListFeaturesPaginator,
        ListLaunchesPaginator,
        ListProjectsPaginator,
        ListSegmentReferencesPaginator,
        ListSegmentsPaginator,
    )

    session = Session()
    client: CloudWatchEvidentlyClient = session.client("evidently")

    list_experiments_paginator: ListExperimentsPaginator = client.get_paginator("list_experiments")
    list_features_paginator: ListFeaturesPaginator = client.get_paginator("list_features")
    list_launches_paginator: ListLaunchesPaginator = client.get_paginator("list_launches")
    list_projects_paginator: ListProjectsPaginator = client.get_paginator("list_projects")
    list_segment_references_paginator: ListSegmentReferencesPaginator = client.get_paginator("list_segment_references")
    list_segments_paginator: ListSegmentsPaginator = client.get_paginator("list_segments")
    ```
"""
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .literals import ExperimentStatusType, LaunchStatusType, SegmentReferenceResourceTypeType
from .type_defs import (
    ListExperimentsResponseTypeDef,
    ListFeaturesResponseTypeDef,
    ListLaunchesResponseTypeDef,
    ListProjectsResponseTypeDef,
    ListSegmentReferencesResponseTypeDef,
    ListSegmentsResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "ListExperimentsPaginator",
    "ListFeaturesPaginator",
    "ListLaunchesPaginator",
    "ListProjectsPaginator",
    "ListSegmentReferencesPaginator",
    "ListSegmentsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListExperimentsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Paginator.ListExperiments)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evidently/paginators/#listexperimentspaginator)
    """

    def paginate(
        self,
        *,
        project: str,
        status: ExperimentStatusType = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> _PageIterator[ListExperimentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Paginator.ListExperiments.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evidently/paginators/#listexperimentspaginator)
        """


class ListFeaturesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Paginator.ListFeatures)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evidently/paginators/#listfeaturespaginator)
    """

    def paginate(
        self, *, project: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> _PageIterator[ListFeaturesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Paginator.ListFeatures.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evidently/paginators/#listfeaturespaginator)
        """


class ListLaunchesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Paginator.ListLaunches)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evidently/paginators/#listlaunchespaginator)
    """

    def paginate(
        self,
        *,
        project: str,
        status: LaunchStatusType = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> _PageIterator[ListLaunchesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Paginator.ListLaunches.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evidently/paginators/#listlaunchespaginator)
        """


class ListProjectsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Paginator.ListProjects)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evidently/paginators/#listprojectspaginator)
    """

    def paginate(
        self, *, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> _PageIterator[ListProjectsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Paginator.ListProjects.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evidently/paginators/#listprojectspaginator)
        """


class ListSegmentReferencesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Paginator.ListSegmentReferences)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evidently/paginators/#listsegmentreferencespaginator)
    """

    def paginate(
        self,
        *,
        segment: str,
        type: SegmentReferenceResourceTypeType,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> _PageIterator[ListSegmentReferencesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Paginator.ListSegmentReferences.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evidently/paginators/#listsegmentreferencespaginator)
        """


class ListSegmentsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Paginator.ListSegments)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evidently/paginators/#listsegmentspaginator)
    """

    def paginate(
        self, *, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> _PageIterator[ListSegmentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evidently.html#CloudWatchEvidently.Paginator.ListSegments.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evidently/paginators/#listsegmentspaginator)
        """
