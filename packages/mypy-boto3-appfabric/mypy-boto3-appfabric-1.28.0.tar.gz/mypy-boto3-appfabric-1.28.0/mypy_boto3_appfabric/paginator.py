"""
Type annotations for appfabric service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appfabric/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_appfabric.client import AppFabricClient
    from mypy_boto3_appfabric.paginator import (
        ListAppAuthorizationsPaginator,
        ListAppBundlesPaginator,
        ListIngestionDestinationsPaginator,
        ListIngestionsPaginator,
    )

    session = Session()
    client: AppFabricClient = session.client("appfabric")

    list_app_authorizations_paginator: ListAppAuthorizationsPaginator = client.get_paginator("list_app_authorizations")
    list_app_bundles_paginator: ListAppBundlesPaginator = client.get_paginator("list_app_bundles")
    list_ingestion_destinations_paginator: ListIngestionDestinationsPaginator = client.get_paginator("list_ingestion_destinations")
    list_ingestions_paginator: ListIngestionsPaginator = client.get_paginator("list_ingestions")
    ```
"""
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListAppAuthorizationsResponseTypeDef,
    ListAppBundlesResponseTypeDef,
    ListIngestionDestinationsResponseTypeDef,
    ListIngestionsResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "ListAppAuthorizationsPaginator",
    "ListAppBundlesPaginator",
    "ListIngestionDestinationsPaginator",
    "ListIngestionsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListAppAuthorizationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric.html#AppFabric.Paginator.ListAppAuthorizations)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appfabric/paginators/#listappauthorizationspaginator)
    """

    def paginate(
        self, *, appBundleIdentifier: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> _PageIterator[ListAppAuthorizationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric.html#AppFabric.Paginator.ListAppAuthorizations.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appfabric/paginators/#listappauthorizationspaginator)
        """


class ListAppBundlesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric.html#AppFabric.Paginator.ListAppBundles)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appfabric/paginators/#listappbundlespaginator)
    """

    def paginate(
        self, *, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> _PageIterator[ListAppBundlesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric.html#AppFabric.Paginator.ListAppBundles.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appfabric/paginators/#listappbundlespaginator)
        """


class ListIngestionDestinationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric.html#AppFabric.Paginator.ListIngestionDestinations)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appfabric/paginators/#listingestiondestinationspaginator)
    """

    def paginate(
        self,
        *,
        appBundleIdentifier: str,
        ingestionIdentifier: str,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> _PageIterator[ListIngestionDestinationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric.html#AppFabric.Paginator.ListIngestionDestinations.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appfabric/paginators/#listingestiondestinationspaginator)
        """


class ListIngestionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric.html#AppFabric.Paginator.ListIngestions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appfabric/paginators/#listingestionspaginator)
    """

    def paginate(
        self, *, appBundleIdentifier: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> _PageIterator[ListIngestionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appfabric.html#AppFabric.Paginator.ListIngestions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_appfabric/paginators/#listingestionspaginator)
        """
