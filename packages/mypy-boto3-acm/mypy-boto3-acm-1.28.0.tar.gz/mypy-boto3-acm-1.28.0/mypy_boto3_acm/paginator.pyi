"""
Type annotations for acm service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_acm.client import ACMClient
    from mypy_boto3_acm.paginator import (
        ListCertificatesPaginator,
    )

    session = Session()
    client: ACMClient = session.client("acm")

    list_certificates_paginator: ListCertificatesPaginator = client.get_paginator("list_certificates")
    ```
"""
import sys
from typing import Generic, Iterator, Sequence, TypeVar

from botocore.paginate import PageIterator, Paginator

from .literals import CertificateStatusType, SortOrderType
from .type_defs import FiltersTypeDef, ListCertificatesResponseTypeDef, PaginatorConfigTypeDef

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("ListCertificatesPaginator",)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListCertificatesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm.html#ACM.Paginator.ListCertificates)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm/paginators/#listcertificatespaginator)
    """

    def paginate(
        self,
        *,
        CertificateStatuses: Sequence[CertificateStatusType] = ...,
        Includes: FiltersTypeDef = ...,
        SortBy: Literal["CREATED_AT"] = ...,
        SortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListCertificatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm.html#ACM.Paginator.ListCertificates.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm/paginators/#listcertificatespaginator)
        """
