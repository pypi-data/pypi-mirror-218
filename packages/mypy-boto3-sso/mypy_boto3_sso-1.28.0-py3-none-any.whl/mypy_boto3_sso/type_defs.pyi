"""
Type annotations for sso service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sso/type_defs/)

Usage::

    ```python
    from mypy_boto3_sso.type_defs import AccountInfoTypeDef

    data: AccountInfoTypeDef = {...}
    ```
"""
import sys
from typing import Dict, List

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "AccountInfoTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetRoleCredentialsRequestRequestTypeDef",
    "RoleCredentialsTypeDef",
    "ListAccountRolesRequestListAccountRolesPaginateTypeDef",
    "ListAccountRolesRequestRequestTypeDef",
    "RoleInfoTypeDef",
    "ListAccountsRequestListAccountsPaginateTypeDef",
    "ListAccountsRequestRequestTypeDef",
    "LogoutRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "ResponseMetadataTypeDef",
    "ListAccountsResponseTypeDef",
    "GetRoleCredentialsResponseTypeDef",
    "ListAccountRolesResponseTypeDef",
)

AccountInfoTypeDef = TypedDict(
    "AccountInfoTypeDef",
    {
        "accountId": str,
        "accountName": str,
        "emailAddress": str,
    },
    total=False,
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetRoleCredentialsRequestRequestTypeDef = TypedDict(
    "GetRoleCredentialsRequestRequestTypeDef",
    {
        "roleName": str,
        "accountId": str,
        "accessToken": str,
    },
)

RoleCredentialsTypeDef = TypedDict(
    "RoleCredentialsTypeDef",
    {
        "accessKeyId": str,
        "secretAccessKey": str,
        "sessionToken": str,
        "expiration": int,
    },
    total=False,
)

_RequiredListAccountRolesRequestListAccountRolesPaginateTypeDef = TypedDict(
    "_RequiredListAccountRolesRequestListAccountRolesPaginateTypeDef",
    {
        "accessToken": str,
        "accountId": str,
    },
)
_OptionalListAccountRolesRequestListAccountRolesPaginateTypeDef = TypedDict(
    "_OptionalListAccountRolesRequestListAccountRolesPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

class ListAccountRolesRequestListAccountRolesPaginateTypeDef(
    _RequiredListAccountRolesRequestListAccountRolesPaginateTypeDef,
    _OptionalListAccountRolesRequestListAccountRolesPaginateTypeDef,
):
    pass

_RequiredListAccountRolesRequestRequestTypeDef = TypedDict(
    "_RequiredListAccountRolesRequestRequestTypeDef",
    {
        "accessToken": str,
        "accountId": str,
    },
)
_OptionalListAccountRolesRequestRequestTypeDef = TypedDict(
    "_OptionalListAccountRolesRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

class ListAccountRolesRequestRequestTypeDef(
    _RequiredListAccountRolesRequestRequestTypeDef, _OptionalListAccountRolesRequestRequestTypeDef
):
    pass

RoleInfoTypeDef = TypedDict(
    "RoleInfoTypeDef",
    {
        "roleName": str,
        "accountId": str,
    },
    total=False,
)

_RequiredListAccountsRequestListAccountsPaginateTypeDef = TypedDict(
    "_RequiredListAccountsRequestListAccountsPaginateTypeDef",
    {
        "accessToken": str,
    },
)
_OptionalListAccountsRequestListAccountsPaginateTypeDef = TypedDict(
    "_OptionalListAccountsRequestListAccountsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

class ListAccountsRequestListAccountsPaginateTypeDef(
    _RequiredListAccountsRequestListAccountsPaginateTypeDef,
    _OptionalListAccountsRequestListAccountsPaginateTypeDef,
):
    pass

_RequiredListAccountsRequestRequestTypeDef = TypedDict(
    "_RequiredListAccountsRequestRequestTypeDef",
    {
        "accessToken": str,
    },
)
_OptionalListAccountsRequestRequestTypeDef = TypedDict(
    "_OptionalListAccountsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

class ListAccountsRequestRequestTypeDef(
    _RequiredListAccountsRequestRequestTypeDef, _OptionalListAccountsRequestRequestTypeDef
):
    pass

LogoutRequestRequestTypeDef = TypedDict(
    "LogoutRequestRequestTypeDef",
    {
        "accessToken": str,
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

ListAccountsResponseTypeDef = TypedDict(
    "ListAccountsResponseTypeDef",
    {
        "nextToken": str,
        "accountList": List[AccountInfoTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetRoleCredentialsResponseTypeDef = TypedDict(
    "GetRoleCredentialsResponseTypeDef",
    {
        "roleCredentials": RoleCredentialsTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListAccountRolesResponseTypeDef = TypedDict(
    "ListAccountRolesResponseTypeDef",
    {
        "nextToken": str,
        "roleList": List[RoleInfoTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)
