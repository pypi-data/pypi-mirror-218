"""
Type annotations for arc-zonal-shift service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_arc_zonal_shift/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_arc_zonal_shift.client import ARCZonalShiftClient
    from mypy_boto3_arc_zonal_shift.paginator import (
        ListManagedResourcesPaginator,
        ListZonalShiftsPaginator,
    )

    session = Session()
    client: ARCZonalShiftClient = session.client("arc-zonal-shift")

    list_managed_resources_paginator: ListManagedResourcesPaginator = client.get_paginator("list_managed_resources")
    list_zonal_shifts_paginator: ListZonalShiftsPaginator = client.get_paginator("list_zonal_shifts")
    ```
"""
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .literals import ZonalShiftStatusType
from .type_defs import (
    ListManagedResourcesResponseTypeDef,
    ListZonalShiftsResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = ("ListManagedResourcesPaginator", "ListZonalShiftsPaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListManagedResourcesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-zonal-shift.html#ARCZonalShift.Paginator.ListManagedResources)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_arc_zonal_shift/paginators/#listmanagedresourcespaginator)
    """

    def paginate(
        self, *, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> _PageIterator[ListManagedResourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-zonal-shift.html#ARCZonalShift.Paginator.ListManagedResources.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_arc_zonal_shift/paginators/#listmanagedresourcespaginator)
        """

class ListZonalShiftsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-zonal-shift.html#ARCZonalShift.Paginator.ListZonalShifts)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_arc_zonal_shift/paginators/#listzonalshiftspaginator)
    """

    def paginate(
        self,
        *,
        status: ZonalShiftStatusType = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> _PageIterator[ListZonalShiftsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-zonal-shift.html#ARCZonalShift.Paginator.ListZonalShifts.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_arc_zonal_shift/paginators/#listzonalshiftspaginator)
        """
