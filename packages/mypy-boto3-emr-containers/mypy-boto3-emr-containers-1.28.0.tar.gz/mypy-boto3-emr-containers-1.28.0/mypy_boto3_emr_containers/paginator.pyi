"""
Type annotations for emr-containers service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr_containers/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_emr_containers.client import EMRContainersClient
    from mypy_boto3_emr_containers.paginator import (
        ListJobRunsPaginator,
        ListJobTemplatesPaginator,
        ListManagedEndpointsPaginator,
        ListVirtualClustersPaginator,
    )

    session = Session()
    client: EMRContainersClient = session.client("emr-containers")

    list_job_runs_paginator: ListJobRunsPaginator = client.get_paginator("list_job_runs")
    list_job_templates_paginator: ListJobTemplatesPaginator = client.get_paginator("list_job_templates")
    list_managed_endpoints_paginator: ListManagedEndpointsPaginator = client.get_paginator("list_managed_endpoints")
    list_virtual_clusters_paginator: ListVirtualClustersPaginator = client.get_paginator("list_virtual_clusters")
    ```
"""
import sys
from datetime import datetime
from typing import Generic, Iterator, Sequence, TypeVar, Union

from botocore.paginate import PageIterator, Paginator

from .literals import EndpointStateType, JobRunStateType, VirtualClusterStateType
from .type_defs import (
    ListJobRunsResponseTypeDef,
    ListJobTemplatesResponseTypeDef,
    ListManagedEndpointsResponseTypeDef,
    ListVirtualClustersResponseTypeDef,
    PaginatorConfigTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = (
    "ListJobRunsPaginator",
    "ListJobTemplatesPaginator",
    "ListManagedEndpointsPaginator",
    "ListVirtualClustersPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListJobRunsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers.html#EMRContainers.Paginator.ListJobRuns)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr_containers/paginators/#listjobrunspaginator)
    """

    def paginate(
        self,
        *,
        virtualClusterId: str,
        createdBefore: Union[datetime, str] = ...,
        createdAfter: Union[datetime, str] = ...,
        name: str = ...,
        states: Sequence[JobRunStateType] = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> _PageIterator[ListJobRunsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers.html#EMRContainers.Paginator.ListJobRuns.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr_containers/paginators/#listjobrunspaginator)
        """

class ListJobTemplatesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers.html#EMRContainers.Paginator.ListJobTemplates)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr_containers/paginators/#listjobtemplatespaginator)
    """

    def paginate(
        self,
        *,
        createdAfter: Union[datetime, str] = ...,
        createdBefore: Union[datetime, str] = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> _PageIterator[ListJobTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers.html#EMRContainers.Paginator.ListJobTemplates.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr_containers/paginators/#listjobtemplatespaginator)
        """

class ListManagedEndpointsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers.html#EMRContainers.Paginator.ListManagedEndpoints)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr_containers/paginators/#listmanagedendpointspaginator)
    """

    def paginate(
        self,
        *,
        virtualClusterId: str,
        createdBefore: Union[datetime, str] = ...,
        createdAfter: Union[datetime, str] = ...,
        types: Sequence[str] = ...,
        states: Sequence[EndpointStateType] = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> _PageIterator[ListManagedEndpointsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers.html#EMRContainers.Paginator.ListManagedEndpoints.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr_containers/paginators/#listmanagedendpointspaginator)
        """

class ListVirtualClustersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers.html#EMRContainers.Paginator.ListVirtualClusters)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr_containers/paginators/#listvirtualclusterspaginator)
    """

    def paginate(
        self,
        *,
        containerProviderId: str = ...,
        containerProviderType: Literal["EKS"] = ...,
        createdAfter: Union[datetime, str] = ...,
        createdBefore: Union[datetime, str] = ...,
        states: Sequence[VirtualClusterStateType] = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> _PageIterator[ListVirtualClustersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers.html#EMRContainers.Paginator.ListVirtualClusters.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr_containers/paginators/#listvirtualclusterspaginator)
        """
