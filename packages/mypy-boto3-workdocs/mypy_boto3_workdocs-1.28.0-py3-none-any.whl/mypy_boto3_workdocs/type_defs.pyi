"""
Type annotations for workdocs service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/type_defs/)

Usage::

    ```python
    from mypy_boto3_workdocs.type_defs import AbortDocumentVersionUploadRequestRequestTypeDef

    data: AbortDocumentVersionUploadRequestRequestTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    ActivityTypeType,
    BooleanEnumTypeType,
    CommentStatusTypeType,
    CommentVisibilityTypeType,
    ContentCategoryTypeType,
    DocumentSourceTypeType,
    DocumentStatusTypeType,
    DocumentThumbnailTypeType,
    FolderContentTypeType,
    LanguageCodeTypeType,
    LocaleTypeType,
    OrderByFieldTypeType,
    OrderTypeType,
    PrincipalRoleTypeType,
    PrincipalTypeType,
    ResourceSortTypeType,
    ResourceStateTypeType,
    ResourceTypeType,
    ResponseItemTypeType,
    RolePermissionTypeType,
    RoleTypeType,
    SearchCollectionTypeType,
    SearchQueryScopeTypeType,
    SearchResourceTypeType,
    ShareStatusTypeType,
    SortOrderType,
    StorageTypeType,
    SubscriptionProtocolTypeType,
    UserFilterTypeType,
    UserSortTypeType,
    UserStatusTypeType,
    UserTypeType,
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
    "AbortDocumentVersionUploadRequestRequestTypeDef",
    "ActivateUserRequestRequestTypeDef",
    "UserMetadataTypeDef",
    "NotificationOptionsTypeDef",
    "SharePrincipalTypeDef",
    "ShareResultTypeDef",
    "CreateCommentRequestRequestTypeDef",
    "CreateCustomMetadataRequestRequestTypeDef",
    "CreateFolderRequestRequestTypeDef",
    "FolderMetadataTypeDef",
    "CreateLabelsRequestRequestTypeDef",
    "CreateNotificationSubscriptionRequestRequestTypeDef",
    "SubscriptionTypeDef",
    "StorageRuleTypeTypeDef",
    "DateRangeTypeTypeDef",
    "DeactivateUserRequestRequestTypeDef",
    "DeleteCommentRequestRequestTypeDef",
    "DeleteCustomMetadataRequestRequestTypeDef",
    "DeleteDocumentRequestRequestTypeDef",
    "DeleteDocumentVersionRequestRequestTypeDef",
    "DeleteFolderContentsRequestRequestTypeDef",
    "DeleteFolderRequestRequestTypeDef",
    "DeleteLabelsRequestRequestTypeDef",
    "DeleteNotificationSubscriptionRequestRequestTypeDef",
    "DeleteUserRequestRequestTypeDef",
    "DescribeActivitiesRequestDescribeActivitiesPaginateTypeDef",
    "DescribeActivitiesRequestRequestTypeDef",
    "DescribeCommentsRequestDescribeCommentsPaginateTypeDef",
    "DescribeCommentsRequestRequestTypeDef",
    "DescribeDocumentVersionsRequestDescribeDocumentVersionsPaginateTypeDef",
    "DescribeDocumentVersionsRequestRequestTypeDef",
    "DocumentVersionMetadataTypeDef",
    "DescribeFolderContentsRequestDescribeFolderContentsPaginateTypeDef",
    "DescribeFolderContentsRequestRequestTypeDef",
    "DescribeGroupsRequestDescribeGroupsPaginateTypeDef",
    "DescribeGroupsRequestRequestTypeDef",
    "GroupMetadataTypeDef",
    "DescribeNotificationSubscriptionsRequestDescribeNotificationSubscriptionsPaginateTypeDef",
    "DescribeNotificationSubscriptionsRequestRequestTypeDef",
    "DescribeResourcePermissionsRequestDescribeResourcePermissionsPaginateTypeDef",
    "DescribeResourcePermissionsRequestRequestTypeDef",
    "DescribeRootFoldersRequestDescribeRootFoldersPaginateTypeDef",
    "DescribeRootFoldersRequestRequestTypeDef",
    "DescribeUsersRequestDescribeUsersPaginateTypeDef",
    "DescribeUsersRequestRequestTypeDef",
    "EmptyResponseMetadataTypeDef",
    "LongRangeTypeTypeDef",
    "SearchPrincipalTypeTypeDef",
    "GetCurrentUserRequestRequestTypeDef",
    "GetDocumentPathRequestRequestTypeDef",
    "GetDocumentRequestRequestTypeDef",
    "GetDocumentVersionRequestRequestTypeDef",
    "GetFolderPathRequestRequestTypeDef",
    "GetFolderRequestRequestTypeDef",
    "GetResourcesRequestRequestTypeDef",
    "InitiateDocumentVersionUploadRequestRequestTypeDef",
    "UploadMetadataTypeDef",
    "PaginatorConfigTypeDef",
    "PermissionInfoTypeDef",
    "RemoveAllResourcePermissionsRequestRequestTypeDef",
    "RemoveResourcePermissionRequestRequestTypeDef",
    "ResourcePathComponentTypeDef",
    "ResponseMetadataTypeDef",
    "RestoreDocumentVersionsRequestRequestTypeDef",
    "SearchSortResultTypeDef",
    "UpdateDocumentRequestRequestTypeDef",
    "UpdateDocumentVersionRequestRequestTypeDef",
    "UpdateFolderRequestRequestTypeDef",
    "ResourceMetadataTypeDef",
    "AddResourcePermissionsRequestRequestTypeDef",
    "AddResourcePermissionsResponseTypeDef",
    "CreateFolderResponseTypeDef",
    "DescribeRootFoldersResponseTypeDef",
    "GetFolderResponseTypeDef",
    "CreateNotificationSubscriptionResponseTypeDef",
    "DescribeNotificationSubscriptionsResponseTypeDef",
    "CreateUserRequestRequestTypeDef",
    "UpdateUserRequestRequestTypeDef",
    "UserStorageMetadataTypeDef",
    "DescribeDocumentVersionsResponseTypeDef",
    "DocumentMetadataTypeDef",
    "GetDocumentVersionResponseTypeDef",
    "DescribeGroupsResponseTypeDef",
    "ParticipantsTypeDef",
    "FiltersTypeDef",
    "PrincipalTypeDef",
    "ResourcePathTypeDef",
    "UserTypeDef",
    "DescribeFolderContentsResponseTypeDef",
    "GetDocumentResponseTypeDef",
    "GetResourcesResponseTypeDef",
    "InitiateDocumentVersionUploadResponseTypeDef",
    "SearchResourcesRequestRequestTypeDef",
    "SearchResourcesRequestSearchResourcesPaginateTypeDef",
    "DescribeResourcePermissionsResponseTypeDef",
    "GetDocumentPathResponseTypeDef",
    "GetFolderPathResponseTypeDef",
    "ActivateUserResponseTypeDef",
    "CommentMetadataTypeDef",
    "CommentTypeDef",
    "CreateUserResponseTypeDef",
    "DescribeUsersResponseTypeDef",
    "GetCurrentUserResponseTypeDef",
    "UpdateUserResponseTypeDef",
    "ActivityTypeDef",
    "ResponseItemTypeDef",
    "CreateCommentResponseTypeDef",
    "DescribeCommentsResponseTypeDef",
    "DescribeActivitiesResponseTypeDef",
    "SearchResourcesResponseTypeDef",
)

_RequiredAbortDocumentVersionUploadRequestRequestTypeDef = TypedDict(
    "_RequiredAbortDocumentVersionUploadRequestRequestTypeDef",
    {
        "DocumentId": str,
        "VersionId": str,
    },
)
_OptionalAbortDocumentVersionUploadRequestRequestTypeDef = TypedDict(
    "_OptionalAbortDocumentVersionUploadRequestRequestTypeDef",
    {
        "AuthenticationToken": str,
    },
    total=False,
)

class AbortDocumentVersionUploadRequestRequestTypeDef(
    _RequiredAbortDocumentVersionUploadRequestRequestTypeDef,
    _OptionalAbortDocumentVersionUploadRequestRequestTypeDef,
):
    pass

_RequiredActivateUserRequestRequestTypeDef = TypedDict(
    "_RequiredActivateUserRequestRequestTypeDef",
    {
        "UserId": str,
    },
)
_OptionalActivateUserRequestRequestTypeDef = TypedDict(
    "_OptionalActivateUserRequestRequestTypeDef",
    {
        "AuthenticationToken": str,
    },
    total=False,
)

class ActivateUserRequestRequestTypeDef(
    _RequiredActivateUserRequestRequestTypeDef, _OptionalActivateUserRequestRequestTypeDef
):
    pass

UserMetadataTypeDef = TypedDict(
    "UserMetadataTypeDef",
    {
        "Id": str,
        "Username": str,
        "GivenName": str,
        "Surname": str,
        "EmailAddress": str,
    },
    total=False,
)

NotificationOptionsTypeDef = TypedDict(
    "NotificationOptionsTypeDef",
    {
        "SendEmail": bool,
        "EmailMessage": str,
    },
    total=False,
)

SharePrincipalTypeDef = TypedDict(
    "SharePrincipalTypeDef",
    {
        "Id": str,
        "Type": PrincipalTypeType,
        "Role": RoleTypeType,
    },
)

ShareResultTypeDef = TypedDict(
    "ShareResultTypeDef",
    {
        "PrincipalId": str,
        "InviteePrincipalId": str,
        "Role": RoleTypeType,
        "Status": ShareStatusTypeType,
        "ShareId": str,
        "StatusMessage": str,
    },
    total=False,
)

_RequiredCreateCommentRequestRequestTypeDef = TypedDict(
    "_RequiredCreateCommentRequestRequestTypeDef",
    {
        "DocumentId": str,
        "VersionId": str,
        "Text": str,
    },
)
_OptionalCreateCommentRequestRequestTypeDef = TypedDict(
    "_OptionalCreateCommentRequestRequestTypeDef",
    {
        "AuthenticationToken": str,
        "ParentId": str,
        "ThreadId": str,
        "Visibility": CommentVisibilityTypeType,
        "NotifyCollaborators": bool,
    },
    total=False,
)

class CreateCommentRequestRequestTypeDef(
    _RequiredCreateCommentRequestRequestTypeDef, _OptionalCreateCommentRequestRequestTypeDef
):
    pass

_RequiredCreateCustomMetadataRequestRequestTypeDef = TypedDict(
    "_RequiredCreateCustomMetadataRequestRequestTypeDef",
    {
        "ResourceId": str,
        "CustomMetadata": Mapping[str, str],
    },
)
_OptionalCreateCustomMetadataRequestRequestTypeDef = TypedDict(
    "_OptionalCreateCustomMetadataRequestRequestTypeDef",
    {
        "AuthenticationToken": str,
        "VersionId": str,
    },
    total=False,
)

class CreateCustomMetadataRequestRequestTypeDef(
    _RequiredCreateCustomMetadataRequestRequestTypeDef,
    _OptionalCreateCustomMetadataRequestRequestTypeDef,
):
    pass

_RequiredCreateFolderRequestRequestTypeDef = TypedDict(
    "_RequiredCreateFolderRequestRequestTypeDef",
    {
        "ParentFolderId": str,
    },
)
_OptionalCreateFolderRequestRequestTypeDef = TypedDict(
    "_OptionalCreateFolderRequestRequestTypeDef",
    {
        "AuthenticationToken": str,
        "Name": str,
    },
    total=False,
)

class CreateFolderRequestRequestTypeDef(
    _RequiredCreateFolderRequestRequestTypeDef, _OptionalCreateFolderRequestRequestTypeDef
):
    pass

FolderMetadataTypeDef = TypedDict(
    "FolderMetadataTypeDef",
    {
        "Id": str,
        "Name": str,
        "CreatorId": str,
        "ParentFolderId": str,
        "CreatedTimestamp": datetime,
        "ModifiedTimestamp": datetime,
        "ResourceState": ResourceStateTypeType,
        "Signature": str,
        "Labels": List[str],
        "Size": int,
        "LatestVersionSize": int,
    },
    total=False,
)

_RequiredCreateLabelsRequestRequestTypeDef = TypedDict(
    "_RequiredCreateLabelsRequestRequestTypeDef",
    {
        "ResourceId": str,
        "Labels": Sequence[str],
    },
)
_OptionalCreateLabelsRequestRequestTypeDef = TypedDict(
    "_OptionalCreateLabelsRequestRequestTypeDef",
    {
        "AuthenticationToken": str,
    },
    total=False,
)

class CreateLabelsRequestRequestTypeDef(
    _RequiredCreateLabelsRequestRequestTypeDef, _OptionalCreateLabelsRequestRequestTypeDef
):
    pass

CreateNotificationSubscriptionRequestRequestTypeDef = TypedDict(
    "CreateNotificationSubscriptionRequestRequestTypeDef",
    {
        "OrganizationId": str,
        "Endpoint": str,
        "Protocol": SubscriptionProtocolTypeType,
        "SubscriptionType": Literal["ALL"],
    },
)

SubscriptionTypeDef = TypedDict(
    "SubscriptionTypeDef",
    {
        "SubscriptionId": str,
        "EndPoint": str,
        "Protocol": SubscriptionProtocolTypeType,
    },
    total=False,
)

StorageRuleTypeTypeDef = TypedDict(
    "StorageRuleTypeTypeDef",
    {
        "StorageAllocatedInBytes": int,
        "StorageType": StorageTypeType,
    },
    total=False,
)

DateRangeTypeTypeDef = TypedDict(
    "DateRangeTypeTypeDef",
    {
        "StartValue": Union[datetime, str],
        "EndValue": Union[datetime, str],
    },
    total=False,
)

_RequiredDeactivateUserRequestRequestTypeDef = TypedDict(
    "_RequiredDeactivateUserRequestRequestTypeDef",
    {
        "UserId": str,
    },
)
_OptionalDeactivateUserRequestRequestTypeDef = TypedDict(
    "_OptionalDeactivateUserRequestRequestTypeDef",
    {
        "AuthenticationToken": str,
    },
    total=False,
)

class DeactivateUserRequestRequestTypeDef(
    _RequiredDeactivateUserRequestRequestTypeDef, _OptionalDeactivateUserRequestRequestTypeDef
):
    pass

_RequiredDeleteCommentRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteCommentRequestRequestTypeDef",
    {
        "DocumentId": str,
        "VersionId": str,
        "CommentId": str,
    },
)
_OptionalDeleteCommentRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteCommentRequestRequestTypeDef",
    {
        "AuthenticationToken": str,
    },
    total=False,
)

class DeleteCommentRequestRequestTypeDef(
    _RequiredDeleteCommentRequestRequestTypeDef, _OptionalDeleteCommentRequestRequestTypeDef
):
    pass

_RequiredDeleteCustomMetadataRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteCustomMetadataRequestRequestTypeDef",
    {
        "ResourceId": str,
    },
)
_OptionalDeleteCustomMetadataRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteCustomMetadataRequestRequestTypeDef",
    {
        "AuthenticationToken": str,
        "VersionId": str,
        "Keys": Sequence[str],
        "DeleteAll": bool,
    },
    total=False,
)

class DeleteCustomMetadataRequestRequestTypeDef(
    _RequiredDeleteCustomMetadataRequestRequestTypeDef,
    _OptionalDeleteCustomMetadataRequestRequestTypeDef,
):
    pass

_RequiredDeleteDocumentRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteDocumentRequestRequestTypeDef",
    {
        "DocumentId": str,
    },
)
_OptionalDeleteDocumentRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteDocumentRequestRequestTypeDef",
    {
        "AuthenticationToken": str,
    },
    total=False,
)

class DeleteDocumentRequestRequestTypeDef(
    _RequiredDeleteDocumentRequestRequestTypeDef, _OptionalDeleteDocumentRequestRequestTypeDef
):
    pass

_RequiredDeleteDocumentVersionRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteDocumentVersionRequestRequestTypeDef",
    {
        "DocumentId": str,
        "VersionId": str,
        "DeletePriorVersions": bool,
    },
)
_OptionalDeleteDocumentVersionRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteDocumentVersionRequestRequestTypeDef",
    {
        "AuthenticationToken": str,
    },
    total=False,
)

class DeleteDocumentVersionRequestRequestTypeDef(
    _RequiredDeleteDocumentVersionRequestRequestTypeDef,
    _OptionalDeleteDocumentVersionRequestRequestTypeDef,
):
    pass

_RequiredDeleteFolderContentsRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteFolderContentsRequestRequestTypeDef",
    {
        "FolderId": str,
    },
)
_OptionalDeleteFolderContentsRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteFolderContentsRequestRequestTypeDef",
    {
        "AuthenticationToken": str,
    },
    total=False,
)

class DeleteFolderContentsRequestRequestTypeDef(
    _RequiredDeleteFolderContentsRequestRequestTypeDef,
    _OptionalDeleteFolderContentsRequestRequestTypeDef,
):
    pass

_RequiredDeleteFolderRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteFolderRequestRequestTypeDef",
    {
        "FolderId": str,
    },
)
_OptionalDeleteFolderRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteFolderRequestRequestTypeDef",
    {
        "AuthenticationToken": str,
    },
    total=False,
)

class DeleteFolderRequestRequestTypeDef(
    _RequiredDeleteFolderRequestRequestTypeDef, _OptionalDeleteFolderRequestRequestTypeDef
):
    pass

_RequiredDeleteLabelsRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteLabelsRequestRequestTypeDef",
    {
        "ResourceId": str,
    },
)
_OptionalDeleteLabelsRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteLabelsRequestRequestTypeDef",
    {
        "AuthenticationToken": str,
        "Labels": Sequence[str],
        "DeleteAll": bool,
    },
    total=False,
)

class DeleteLabelsRequestRequestTypeDef(
    _RequiredDeleteLabelsRequestRequestTypeDef, _OptionalDeleteLabelsRequestRequestTypeDef
):
    pass

DeleteNotificationSubscriptionRequestRequestTypeDef = TypedDict(
    "DeleteNotificationSubscriptionRequestRequestTypeDef",
    {
        "SubscriptionId": str,
        "OrganizationId": str,
    },
)

_RequiredDeleteUserRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteUserRequestRequestTypeDef",
    {
        "UserId": str,
    },
)
_OptionalDeleteUserRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteUserRequestRequestTypeDef",
    {
        "AuthenticationToken": str,
    },
    total=False,
)

class DeleteUserRequestRequestTypeDef(
    _RequiredDeleteUserRequestRequestTypeDef, _OptionalDeleteUserRequestRequestTypeDef
):
    pass

DescribeActivitiesRequestDescribeActivitiesPaginateTypeDef = TypedDict(
    "DescribeActivitiesRequestDescribeActivitiesPaginateTypeDef",
    {
        "AuthenticationToken": str,
        "StartTime": Union[datetime, str],
        "EndTime": Union[datetime, str],
        "OrganizationId": str,
        "ActivityTypes": str,
        "ResourceId": str,
        "UserId": str,
        "IncludeIndirectActivities": bool,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

DescribeActivitiesRequestRequestTypeDef = TypedDict(
    "DescribeActivitiesRequestRequestTypeDef",
    {
        "AuthenticationToken": str,
        "StartTime": Union[datetime, str],
        "EndTime": Union[datetime, str],
        "OrganizationId": str,
        "ActivityTypes": str,
        "ResourceId": str,
        "UserId": str,
        "IncludeIndirectActivities": bool,
        "Limit": int,
        "Marker": str,
    },
    total=False,
)

_RequiredDescribeCommentsRequestDescribeCommentsPaginateTypeDef = TypedDict(
    "_RequiredDescribeCommentsRequestDescribeCommentsPaginateTypeDef",
    {
        "DocumentId": str,
        "VersionId": str,
    },
)
_OptionalDescribeCommentsRequestDescribeCommentsPaginateTypeDef = TypedDict(
    "_OptionalDescribeCommentsRequestDescribeCommentsPaginateTypeDef",
    {
        "AuthenticationToken": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

class DescribeCommentsRequestDescribeCommentsPaginateTypeDef(
    _RequiredDescribeCommentsRequestDescribeCommentsPaginateTypeDef,
    _OptionalDescribeCommentsRequestDescribeCommentsPaginateTypeDef,
):
    pass

_RequiredDescribeCommentsRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeCommentsRequestRequestTypeDef",
    {
        "DocumentId": str,
        "VersionId": str,
    },
)
_OptionalDescribeCommentsRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeCommentsRequestRequestTypeDef",
    {
        "AuthenticationToken": str,
        "Limit": int,
        "Marker": str,
    },
    total=False,
)

class DescribeCommentsRequestRequestTypeDef(
    _RequiredDescribeCommentsRequestRequestTypeDef, _OptionalDescribeCommentsRequestRequestTypeDef
):
    pass

_RequiredDescribeDocumentVersionsRequestDescribeDocumentVersionsPaginateTypeDef = TypedDict(
    "_RequiredDescribeDocumentVersionsRequestDescribeDocumentVersionsPaginateTypeDef",
    {
        "DocumentId": str,
    },
)
_OptionalDescribeDocumentVersionsRequestDescribeDocumentVersionsPaginateTypeDef = TypedDict(
    "_OptionalDescribeDocumentVersionsRequestDescribeDocumentVersionsPaginateTypeDef",
    {
        "AuthenticationToken": str,
        "Include": str,
        "Fields": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

class DescribeDocumentVersionsRequestDescribeDocumentVersionsPaginateTypeDef(
    _RequiredDescribeDocumentVersionsRequestDescribeDocumentVersionsPaginateTypeDef,
    _OptionalDescribeDocumentVersionsRequestDescribeDocumentVersionsPaginateTypeDef,
):
    pass

_RequiredDescribeDocumentVersionsRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeDocumentVersionsRequestRequestTypeDef",
    {
        "DocumentId": str,
    },
)
_OptionalDescribeDocumentVersionsRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeDocumentVersionsRequestRequestTypeDef",
    {
        "AuthenticationToken": str,
        "Marker": str,
        "Limit": int,
        "Include": str,
        "Fields": str,
    },
    total=False,
)

class DescribeDocumentVersionsRequestRequestTypeDef(
    _RequiredDescribeDocumentVersionsRequestRequestTypeDef,
    _OptionalDescribeDocumentVersionsRequestRequestTypeDef,
):
    pass

DocumentVersionMetadataTypeDef = TypedDict(
    "DocumentVersionMetadataTypeDef",
    {
        "Id": str,
        "Name": str,
        "ContentType": str,
        "Size": int,
        "Signature": str,
        "Status": DocumentStatusTypeType,
        "CreatedTimestamp": datetime,
        "ModifiedTimestamp": datetime,
        "ContentCreatedTimestamp": datetime,
        "ContentModifiedTimestamp": datetime,
        "CreatorId": str,
        "Thumbnail": Dict[DocumentThumbnailTypeType, str],
        "Source": Dict[DocumentSourceTypeType, str],
    },
    total=False,
)

_RequiredDescribeFolderContentsRequestDescribeFolderContentsPaginateTypeDef = TypedDict(
    "_RequiredDescribeFolderContentsRequestDescribeFolderContentsPaginateTypeDef",
    {
        "FolderId": str,
    },
)
_OptionalDescribeFolderContentsRequestDescribeFolderContentsPaginateTypeDef = TypedDict(
    "_OptionalDescribeFolderContentsRequestDescribeFolderContentsPaginateTypeDef",
    {
        "AuthenticationToken": str,
        "Sort": ResourceSortTypeType,
        "Order": OrderTypeType,
        "Type": FolderContentTypeType,
        "Include": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

class DescribeFolderContentsRequestDescribeFolderContentsPaginateTypeDef(
    _RequiredDescribeFolderContentsRequestDescribeFolderContentsPaginateTypeDef,
    _OptionalDescribeFolderContentsRequestDescribeFolderContentsPaginateTypeDef,
):
    pass

_RequiredDescribeFolderContentsRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeFolderContentsRequestRequestTypeDef",
    {
        "FolderId": str,
    },
)
_OptionalDescribeFolderContentsRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeFolderContentsRequestRequestTypeDef",
    {
        "AuthenticationToken": str,
        "Sort": ResourceSortTypeType,
        "Order": OrderTypeType,
        "Limit": int,
        "Marker": str,
        "Type": FolderContentTypeType,
        "Include": str,
    },
    total=False,
)

class DescribeFolderContentsRequestRequestTypeDef(
    _RequiredDescribeFolderContentsRequestRequestTypeDef,
    _OptionalDescribeFolderContentsRequestRequestTypeDef,
):
    pass

_RequiredDescribeGroupsRequestDescribeGroupsPaginateTypeDef = TypedDict(
    "_RequiredDescribeGroupsRequestDescribeGroupsPaginateTypeDef",
    {
        "SearchQuery": str,
    },
)
_OptionalDescribeGroupsRequestDescribeGroupsPaginateTypeDef = TypedDict(
    "_OptionalDescribeGroupsRequestDescribeGroupsPaginateTypeDef",
    {
        "AuthenticationToken": str,
        "OrganizationId": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

class DescribeGroupsRequestDescribeGroupsPaginateTypeDef(
    _RequiredDescribeGroupsRequestDescribeGroupsPaginateTypeDef,
    _OptionalDescribeGroupsRequestDescribeGroupsPaginateTypeDef,
):
    pass

_RequiredDescribeGroupsRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeGroupsRequestRequestTypeDef",
    {
        "SearchQuery": str,
    },
)
_OptionalDescribeGroupsRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeGroupsRequestRequestTypeDef",
    {
        "AuthenticationToken": str,
        "OrganizationId": str,
        "Marker": str,
        "Limit": int,
    },
    total=False,
)

class DescribeGroupsRequestRequestTypeDef(
    _RequiredDescribeGroupsRequestRequestTypeDef, _OptionalDescribeGroupsRequestRequestTypeDef
):
    pass

GroupMetadataTypeDef = TypedDict(
    "GroupMetadataTypeDef",
    {
        "Id": str,
        "Name": str,
    },
    total=False,
)

_RequiredDescribeNotificationSubscriptionsRequestDescribeNotificationSubscriptionsPaginateTypeDef = TypedDict(
    "_RequiredDescribeNotificationSubscriptionsRequestDescribeNotificationSubscriptionsPaginateTypeDef",
    {
        "OrganizationId": str,
    },
)
_OptionalDescribeNotificationSubscriptionsRequestDescribeNotificationSubscriptionsPaginateTypeDef = TypedDict(
    "_OptionalDescribeNotificationSubscriptionsRequestDescribeNotificationSubscriptionsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

class DescribeNotificationSubscriptionsRequestDescribeNotificationSubscriptionsPaginateTypeDef(
    _RequiredDescribeNotificationSubscriptionsRequestDescribeNotificationSubscriptionsPaginateTypeDef,
    _OptionalDescribeNotificationSubscriptionsRequestDescribeNotificationSubscriptionsPaginateTypeDef,
):
    pass

_RequiredDescribeNotificationSubscriptionsRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeNotificationSubscriptionsRequestRequestTypeDef",
    {
        "OrganizationId": str,
    },
)
_OptionalDescribeNotificationSubscriptionsRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeNotificationSubscriptionsRequestRequestTypeDef",
    {
        "Marker": str,
        "Limit": int,
    },
    total=False,
)

class DescribeNotificationSubscriptionsRequestRequestTypeDef(
    _RequiredDescribeNotificationSubscriptionsRequestRequestTypeDef,
    _OptionalDescribeNotificationSubscriptionsRequestRequestTypeDef,
):
    pass

_RequiredDescribeResourcePermissionsRequestDescribeResourcePermissionsPaginateTypeDef = TypedDict(
    "_RequiredDescribeResourcePermissionsRequestDescribeResourcePermissionsPaginateTypeDef",
    {
        "ResourceId": str,
    },
)
_OptionalDescribeResourcePermissionsRequestDescribeResourcePermissionsPaginateTypeDef = TypedDict(
    "_OptionalDescribeResourcePermissionsRequestDescribeResourcePermissionsPaginateTypeDef",
    {
        "AuthenticationToken": str,
        "PrincipalId": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

class DescribeResourcePermissionsRequestDescribeResourcePermissionsPaginateTypeDef(
    _RequiredDescribeResourcePermissionsRequestDescribeResourcePermissionsPaginateTypeDef,
    _OptionalDescribeResourcePermissionsRequestDescribeResourcePermissionsPaginateTypeDef,
):
    pass

_RequiredDescribeResourcePermissionsRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeResourcePermissionsRequestRequestTypeDef",
    {
        "ResourceId": str,
    },
)
_OptionalDescribeResourcePermissionsRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeResourcePermissionsRequestRequestTypeDef",
    {
        "AuthenticationToken": str,
        "PrincipalId": str,
        "Limit": int,
        "Marker": str,
    },
    total=False,
)

class DescribeResourcePermissionsRequestRequestTypeDef(
    _RequiredDescribeResourcePermissionsRequestRequestTypeDef,
    _OptionalDescribeResourcePermissionsRequestRequestTypeDef,
):
    pass

_RequiredDescribeRootFoldersRequestDescribeRootFoldersPaginateTypeDef = TypedDict(
    "_RequiredDescribeRootFoldersRequestDescribeRootFoldersPaginateTypeDef",
    {
        "AuthenticationToken": str,
    },
)
_OptionalDescribeRootFoldersRequestDescribeRootFoldersPaginateTypeDef = TypedDict(
    "_OptionalDescribeRootFoldersRequestDescribeRootFoldersPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

class DescribeRootFoldersRequestDescribeRootFoldersPaginateTypeDef(
    _RequiredDescribeRootFoldersRequestDescribeRootFoldersPaginateTypeDef,
    _OptionalDescribeRootFoldersRequestDescribeRootFoldersPaginateTypeDef,
):
    pass

_RequiredDescribeRootFoldersRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeRootFoldersRequestRequestTypeDef",
    {
        "AuthenticationToken": str,
    },
)
_OptionalDescribeRootFoldersRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeRootFoldersRequestRequestTypeDef",
    {
        "Limit": int,
        "Marker": str,
    },
    total=False,
)

class DescribeRootFoldersRequestRequestTypeDef(
    _RequiredDescribeRootFoldersRequestRequestTypeDef,
    _OptionalDescribeRootFoldersRequestRequestTypeDef,
):
    pass

DescribeUsersRequestDescribeUsersPaginateTypeDef = TypedDict(
    "DescribeUsersRequestDescribeUsersPaginateTypeDef",
    {
        "AuthenticationToken": str,
        "OrganizationId": str,
        "UserIds": str,
        "Query": str,
        "Include": UserFilterTypeType,
        "Order": OrderTypeType,
        "Sort": UserSortTypeType,
        "Fields": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

DescribeUsersRequestRequestTypeDef = TypedDict(
    "DescribeUsersRequestRequestTypeDef",
    {
        "AuthenticationToken": str,
        "OrganizationId": str,
        "UserIds": str,
        "Query": str,
        "Include": UserFilterTypeType,
        "Order": OrderTypeType,
        "Sort": UserSortTypeType,
        "Marker": str,
        "Limit": int,
        "Fields": str,
    },
    total=False,
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

LongRangeTypeTypeDef = TypedDict(
    "LongRangeTypeTypeDef",
    {
        "StartValue": int,
        "EndValue": int,
    },
    total=False,
)

_RequiredSearchPrincipalTypeTypeDef = TypedDict(
    "_RequiredSearchPrincipalTypeTypeDef",
    {
        "Id": str,
    },
)
_OptionalSearchPrincipalTypeTypeDef = TypedDict(
    "_OptionalSearchPrincipalTypeTypeDef",
    {
        "Roles": Sequence[PrincipalRoleTypeType],
    },
    total=False,
)

class SearchPrincipalTypeTypeDef(
    _RequiredSearchPrincipalTypeTypeDef, _OptionalSearchPrincipalTypeTypeDef
):
    pass

GetCurrentUserRequestRequestTypeDef = TypedDict(
    "GetCurrentUserRequestRequestTypeDef",
    {
        "AuthenticationToken": str,
    },
)

_RequiredGetDocumentPathRequestRequestTypeDef = TypedDict(
    "_RequiredGetDocumentPathRequestRequestTypeDef",
    {
        "DocumentId": str,
    },
)
_OptionalGetDocumentPathRequestRequestTypeDef = TypedDict(
    "_OptionalGetDocumentPathRequestRequestTypeDef",
    {
        "AuthenticationToken": str,
        "Limit": int,
        "Fields": str,
        "Marker": str,
    },
    total=False,
)

class GetDocumentPathRequestRequestTypeDef(
    _RequiredGetDocumentPathRequestRequestTypeDef, _OptionalGetDocumentPathRequestRequestTypeDef
):
    pass

_RequiredGetDocumentRequestRequestTypeDef = TypedDict(
    "_RequiredGetDocumentRequestRequestTypeDef",
    {
        "DocumentId": str,
    },
)
_OptionalGetDocumentRequestRequestTypeDef = TypedDict(
    "_OptionalGetDocumentRequestRequestTypeDef",
    {
        "AuthenticationToken": str,
        "IncludeCustomMetadata": bool,
    },
    total=False,
)

class GetDocumentRequestRequestTypeDef(
    _RequiredGetDocumentRequestRequestTypeDef, _OptionalGetDocumentRequestRequestTypeDef
):
    pass

_RequiredGetDocumentVersionRequestRequestTypeDef = TypedDict(
    "_RequiredGetDocumentVersionRequestRequestTypeDef",
    {
        "DocumentId": str,
        "VersionId": str,
    },
)
_OptionalGetDocumentVersionRequestRequestTypeDef = TypedDict(
    "_OptionalGetDocumentVersionRequestRequestTypeDef",
    {
        "AuthenticationToken": str,
        "Fields": str,
        "IncludeCustomMetadata": bool,
    },
    total=False,
)

class GetDocumentVersionRequestRequestTypeDef(
    _RequiredGetDocumentVersionRequestRequestTypeDef,
    _OptionalGetDocumentVersionRequestRequestTypeDef,
):
    pass

_RequiredGetFolderPathRequestRequestTypeDef = TypedDict(
    "_RequiredGetFolderPathRequestRequestTypeDef",
    {
        "FolderId": str,
    },
)
_OptionalGetFolderPathRequestRequestTypeDef = TypedDict(
    "_OptionalGetFolderPathRequestRequestTypeDef",
    {
        "AuthenticationToken": str,
        "Limit": int,
        "Fields": str,
        "Marker": str,
    },
    total=False,
)

class GetFolderPathRequestRequestTypeDef(
    _RequiredGetFolderPathRequestRequestTypeDef, _OptionalGetFolderPathRequestRequestTypeDef
):
    pass

_RequiredGetFolderRequestRequestTypeDef = TypedDict(
    "_RequiredGetFolderRequestRequestTypeDef",
    {
        "FolderId": str,
    },
)
_OptionalGetFolderRequestRequestTypeDef = TypedDict(
    "_OptionalGetFolderRequestRequestTypeDef",
    {
        "AuthenticationToken": str,
        "IncludeCustomMetadata": bool,
    },
    total=False,
)

class GetFolderRequestRequestTypeDef(
    _RequiredGetFolderRequestRequestTypeDef, _OptionalGetFolderRequestRequestTypeDef
):
    pass

GetResourcesRequestRequestTypeDef = TypedDict(
    "GetResourcesRequestRequestTypeDef",
    {
        "AuthenticationToken": str,
        "UserId": str,
        "CollectionType": Literal["SHARED_WITH_ME"],
        "Limit": int,
        "Marker": str,
    },
    total=False,
)

InitiateDocumentVersionUploadRequestRequestTypeDef = TypedDict(
    "InitiateDocumentVersionUploadRequestRequestTypeDef",
    {
        "AuthenticationToken": str,
        "Id": str,
        "Name": str,
        "ContentCreatedTimestamp": Union[datetime, str],
        "ContentModifiedTimestamp": Union[datetime, str],
        "ContentType": str,
        "DocumentSizeInBytes": int,
        "ParentFolderId": str,
    },
    total=False,
)

UploadMetadataTypeDef = TypedDict(
    "UploadMetadataTypeDef",
    {
        "UploadUrl": str,
        "SignedHeaders": Dict[str, str],
    },
    total=False,
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

PermissionInfoTypeDef = TypedDict(
    "PermissionInfoTypeDef",
    {
        "Role": RoleTypeType,
        "Type": RolePermissionTypeType,
    },
    total=False,
)

_RequiredRemoveAllResourcePermissionsRequestRequestTypeDef = TypedDict(
    "_RequiredRemoveAllResourcePermissionsRequestRequestTypeDef",
    {
        "ResourceId": str,
    },
)
_OptionalRemoveAllResourcePermissionsRequestRequestTypeDef = TypedDict(
    "_OptionalRemoveAllResourcePermissionsRequestRequestTypeDef",
    {
        "AuthenticationToken": str,
    },
    total=False,
)

class RemoveAllResourcePermissionsRequestRequestTypeDef(
    _RequiredRemoveAllResourcePermissionsRequestRequestTypeDef,
    _OptionalRemoveAllResourcePermissionsRequestRequestTypeDef,
):
    pass

_RequiredRemoveResourcePermissionRequestRequestTypeDef = TypedDict(
    "_RequiredRemoveResourcePermissionRequestRequestTypeDef",
    {
        "ResourceId": str,
        "PrincipalId": str,
    },
)
_OptionalRemoveResourcePermissionRequestRequestTypeDef = TypedDict(
    "_OptionalRemoveResourcePermissionRequestRequestTypeDef",
    {
        "AuthenticationToken": str,
        "PrincipalType": PrincipalTypeType,
    },
    total=False,
)

class RemoveResourcePermissionRequestRequestTypeDef(
    _RequiredRemoveResourcePermissionRequestRequestTypeDef,
    _OptionalRemoveResourcePermissionRequestRequestTypeDef,
):
    pass

ResourcePathComponentTypeDef = TypedDict(
    "ResourcePathComponentTypeDef",
    {
        "Id": str,
        "Name": str,
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

_RequiredRestoreDocumentVersionsRequestRequestTypeDef = TypedDict(
    "_RequiredRestoreDocumentVersionsRequestRequestTypeDef",
    {
        "DocumentId": str,
    },
)
_OptionalRestoreDocumentVersionsRequestRequestTypeDef = TypedDict(
    "_OptionalRestoreDocumentVersionsRequestRequestTypeDef",
    {
        "AuthenticationToken": str,
    },
    total=False,
)

class RestoreDocumentVersionsRequestRequestTypeDef(
    _RequiredRestoreDocumentVersionsRequestRequestTypeDef,
    _OptionalRestoreDocumentVersionsRequestRequestTypeDef,
):
    pass

SearchSortResultTypeDef = TypedDict(
    "SearchSortResultTypeDef",
    {
        "Field": OrderByFieldTypeType,
        "Order": SortOrderType,
    },
    total=False,
)

_RequiredUpdateDocumentRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateDocumentRequestRequestTypeDef",
    {
        "DocumentId": str,
    },
)
_OptionalUpdateDocumentRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateDocumentRequestRequestTypeDef",
    {
        "AuthenticationToken": str,
        "Name": str,
        "ParentFolderId": str,
        "ResourceState": ResourceStateTypeType,
    },
    total=False,
)

class UpdateDocumentRequestRequestTypeDef(
    _RequiredUpdateDocumentRequestRequestTypeDef, _OptionalUpdateDocumentRequestRequestTypeDef
):
    pass

_RequiredUpdateDocumentVersionRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateDocumentVersionRequestRequestTypeDef",
    {
        "DocumentId": str,
        "VersionId": str,
    },
)
_OptionalUpdateDocumentVersionRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateDocumentVersionRequestRequestTypeDef",
    {
        "AuthenticationToken": str,
        "VersionStatus": Literal["ACTIVE"],
    },
    total=False,
)

class UpdateDocumentVersionRequestRequestTypeDef(
    _RequiredUpdateDocumentVersionRequestRequestTypeDef,
    _OptionalUpdateDocumentVersionRequestRequestTypeDef,
):
    pass

_RequiredUpdateFolderRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateFolderRequestRequestTypeDef",
    {
        "FolderId": str,
    },
)
_OptionalUpdateFolderRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateFolderRequestRequestTypeDef",
    {
        "AuthenticationToken": str,
        "Name": str,
        "ParentFolderId": str,
        "ResourceState": ResourceStateTypeType,
    },
    total=False,
)

class UpdateFolderRequestRequestTypeDef(
    _RequiredUpdateFolderRequestRequestTypeDef, _OptionalUpdateFolderRequestRequestTypeDef
):
    pass

ResourceMetadataTypeDef = TypedDict(
    "ResourceMetadataTypeDef",
    {
        "Type": ResourceTypeType,
        "Name": str,
        "OriginalName": str,
        "Id": str,
        "VersionId": str,
        "Owner": UserMetadataTypeDef,
        "ParentId": str,
    },
    total=False,
)

_RequiredAddResourcePermissionsRequestRequestTypeDef = TypedDict(
    "_RequiredAddResourcePermissionsRequestRequestTypeDef",
    {
        "ResourceId": str,
        "Principals": Sequence[SharePrincipalTypeDef],
    },
)
_OptionalAddResourcePermissionsRequestRequestTypeDef = TypedDict(
    "_OptionalAddResourcePermissionsRequestRequestTypeDef",
    {
        "AuthenticationToken": str,
        "NotificationOptions": NotificationOptionsTypeDef,
    },
    total=False,
)

class AddResourcePermissionsRequestRequestTypeDef(
    _RequiredAddResourcePermissionsRequestRequestTypeDef,
    _OptionalAddResourcePermissionsRequestRequestTypeDef,
):
    pass

AddResourcePermissionsResponseTypeDef = TypedDict(
    "AddResourcePermissionsResponseTypeDef",
    {
        "ShareResults": List[ShareResultTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateFolderResponseTypeDef = TypedDict(
    "CreateFolderResponseTypeDef",
    {
        "Metadata": FolderMetadataTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeRootFoldersResponseTypeDef = TypedDict(
    "DescribeRootFoldersResponseTypeDef",
    {
        "Folders": List[FolderMetadataTypeDef],
        "Marker": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetFolderResponseTypeDef = TypedDict(
    "GetFolderResponseTypeDef",
    {
        "Metadata": FolderMetadataTypeDef,
        "CustomMetadata": Dict[str, str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateNotificationSubscriptionResponseTypeDef = TypedDict(
    "CreateNotificationSubscriptionResponseTypeDef",
    {
        "Subscription": SubscriptionTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeNotificationSubscriptionsResponseTypeDef = TypedDict(
    "DescribeNotificationSubscriptionsResponseTypeDef",
    {
        "Subscriptions": List[SubscriptionTypeDef],
        "Marker": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateUserRequestRequestTypeDef = TypedDict(
    "_RequiredCreateUserRequestRequestTypeDef",
    {
        "Username": str,
        "GivenName": str,
        "Surname": str,
        "Password": str,
    },
)
_OptionalCreateUserRequestRequestTypeDef = TypedDict(
    "_OptionalCreateUserRequestRequestTypeDef",
    {
        "OrganizationId": str,
        "EmailAddress": str,
        "TimeZoneId": str,
        "StorageRule": StorageRuleTypeTypeDef,
        "AuthenticationToken": str,
    },
    total=False,
)

class CreateUserRequestRequestTypeDef(
    _RequiredCreateUserRequestRequestTypeDef, _OptionalCreateUserRequestRequestTypeDef
):
    pass

_RequiredUpdateUserRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateUserRequestRequestTypeDef",
    {
        "UserId": str,
    },
)
_OptionalUpdateUserRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateUserRequestRequestTypeDef",
    {
        "AuthenticationToken": str,
        "GivenName": str,
        "Surname": str,
        "Type": UserTypeType,
        "StorageRule": StorageRuleTypeTypeDef,
        "TimeZoneId": str,
        "Locale": LocaleTypeType,
        "GrantPoweruserPrivileges": BooleanEnumTypeType,
    },
    total=False,
)

class UpdateUserRequestRequestTypeDef(
    _RequiredUpdateUserRequestRequestTypeDef, _OptionalUpdateUserRequestRequestTypeDef
):
    pass

UserStorageMetadataTypeDef = TypedDict(
    "UserStorageMetadataTypeDef",
    {
        "StorageUtilizedInBytes": int,
        "StorageRule": StorageRuleTypeTypeDef,
    },
    total=False,
)

DescribeDocumentVersionsResponseTypeDef = TypedDict(
    "DescribeDocumentVersionsResponseTypeDef",
    {
        "DocumentVersions": List[DocumentVersionMetadataTypeDef],
        "Marker": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DocumentMetadataTypeDef = TypedDict(
    "DocumentMetadataTypeDef",
    {
        "Id": str,
        "CreatorId": str,
        "ParentFolderId": str,
        "CreatedTimestamp": datetime,
        "ModifiedTimestamp": datetime,
        "LatestVersionMetadata": DocumentVersionMetadataTypeDef,
        "ResourceState": ResourceStateTypeType,
        "Labels": List[str],
    },
    total=False,
)

GetDocumentVersionResponseTypeDef = TypedDict(
    "GetDocumentVersionResponseTypeDef",
    {
        "Metadata": DocumentVersionMetadataTypeDef,
        "CustomMetadata": Dict[str, str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeGroupsResponseTypeDef = TypedDict(
    "DescribeGroupsResponseTypeDef",
    {
        "Groups": List[GroupMetadataTypeDef],
        "Marker": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ParticipantsTypeDef = TypedDict(
    "ParticipantsTypeDef",
    {
        "Users": List[UserMetadataTypeDef],
        "Groups": List[GroupMetadataTypeDef],
    },
    total=False,
)

FiltersTypeDef = TypedDict(
    "FiltersTypeDef",
    {
        "TextLocales": Sequence[LanguageCodeTypeType],
        "ContentCategories": Sequence[ContentCategoryTypeType],
        "ResourceTypes": Sequence[SearchResourceTypeType],
        "Labels": Sequence[str],
        "Principals": Sequence[SearchPrincipalTypeTypeDef],
        "AncestorIds": Sequence[str],
        "SearchCollectionTypes": Sequence[SearchCollectionTypeType],
        "SizeRange": LongRangeTypeTypeDef,
        "CreatedRange": DateRangeTypeTypeDef,
        "ModifiedRange": DateRangeTypeTypeDef,
    },
    total=False,
)

PrincipalTypeDef = TypedDict(
    "PrincipalTypeDef",
    {
        "Id": str,
        "Type": PrincipalTypeType,
        "Roles": List[PermissionInfoTypeDef],
    },
    total=False,
)

ResourcePathTypeDef = TypedDict(
    "ResourcePathTypeDef",
    {
        "Components": List[ResourcePathComponentTypeDef],
    },
    total=False,
)

UserTypeDef = TypedDict(
    "UserTypeDef",
    {
        "Id": str,
        "Username": str,
        "EmailAddress": str,
        "GivenName": str,
        "Surname": str,
        "OrganizationId": str,
        "RootFolderId": str,
        "RecycleBinFolderId": str,
        "Status": UserStatusTypeType,
        "Type": UserTypeType,
        "CreatedTimestamp": datetime,
        "ModifiedTimestamp": datetime,
        "TimeZoneId": str,
        "Locale": LocaleTypeType,
        "Storage": UserStorageMetadataTypeDef,
    },
    total=False,
)

DescribeFolderContentsResponseTypeDef = TypedDict(
    "DescribeFolderContentsResponseTypeDef",
    {
        "Folders": List[FolderMetadataTypeDef],
        "Documents": List[DocumentMetadataTypeDef],
        "Marker": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetDocumentResponseTypeDef = TypedDict(
    "GetDocumentResponseTypeDef",
    {
        "Metadata": DocumentMetadataTypeDef,
        "CustomMetadata": Dict[str, str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetResourcesResponseTypeDef = TypedDict(
    "GetResourcesResponseTypeDef",
    {
        "Folders": List[FolderMetadataTypeDef],
        "Documents": List[DocumentMetadataTypeDef],
        "Marker": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

InitiateDocumentVersionUploadResponseTypeDef = TypedDict(
    "InitiateDocumentVersionUploadResponseTypeDef",
    {
        "Metadata": DocumentMetadataTypeDef,
        "UploadMetadata": UploadMetadataTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

SearchResourcesRequestRequestTypeDef = TypedDict(
    "SearchResourcesRequestRequestTypeDef",
    {
        "AuthenticationToken": str,
        "QueryText": str,
        "QueryScopes": Sequence[SearchQueryScopeTypeType],
        "OrganizationId": str,
        "AdditionalResponseFields": Sequence[Literal["WEBURL"]],
        "Filters": FiltersTypeDef,
        "OrderBy": Sequence[SearchSortResultTypeDef],
        "Limit": int,
        "Marker": str,
    },
    total=False,
)

SearchResourcesRequestSearchResourcesPaginateTypeDef = TypedDict(
    "SearchResourcesRequestSearchResourcesPaginateTypeDef",
    {
        "AuthenticationToken": str,
        "QueryText": str,
        "QueryScopes": Sequence[SearchQueryScopeTypeType],
        "OrganizationId": str,
        "AdditionalResponseFields": Sequence[Literal["WEBURL"]],
        "Filters": FiltersTypeDef,
        "OrderBy": Sequence[SearchSortResultTypeDef],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

DescribeResourcePermissionsResponseTypeDef = TypedDict(
    "DescribeResourcePermissionsResponseTypeDef",
    {
        "Principals": List[PrincipalTypeDef],
        "Marker": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetDocumentPathResponseTypeDef = TypedDict(
    "GetDocumentPathResponseTypeDef",
    {
        "Path": ResourcePathTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetFolderPathResponseTypeDef = TypedDict(
    "GetFolderPathResponseTypeDef",
    {
        "Path": ResourcePathTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ActivateUserResponseTypeDef = TypedDict(
    "ActivateUserResponseTypeDef",
    {
        "User": UserTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CommentMetadataTypeDef = TypedDict(
    "CommentMetadataTypeDef",
    {
        "CommentId": str,
        "Contributor": UserTypeDef,
        "CreatedTimestamp": datetime,
        "CommentStatus": CommentStatusTypeType,
        "RecipientId": str,
        "ContributorId": str,
    },
    total=False,
)

_RequiredCommentTypeDef = TypedDict(
    "_RequiredCommentTypeDef",
    {
        "CommentId": str,
    },
)
_OptionalCommentTypeDef = TypedDict(
    "_OptionalCommentTypeDef",
    {
        "ParentId": str,
        "ThreadId": str,
        "Text": str,
        "Contributor": UserTypeDef,
        "CreatedTimestamp": datetime,
        "Status": CommentStatusTypeType,
        "Visibility": CommentVisibilityTypeType,
        "RecipientId": str,
    },
    total=False,
)

class CommentTypeDef(_RequiredCommentTypeDef, _OptionalCommentTypeDef):
    pass

CreateUserResponseTypeDef = TypedDict(
    "CreateUserResponseTypeDef",
    {
        "User": UserTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeUsersResponseTypeDef = TypedDict(
    "DescribeUsersResponseTypeDef",
    {
        "Users": List[UserTypeDef],
        "TotalNumberOfUsers": int,
        "Marker": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetCurrentUserResponseTypeDef = TypedDict(
    "GetCurrentUserResponseTypeDef",
    {
        "User": UserTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateUserResponseTypeDef = TypedDict(
    "UpdateUserResponseTypeDef",
    {
        "User": UserTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ActivityTypeDef = TypedDict(
    "ActivityTypeDef",
    {
        "Type": ActivityTypeType,
        "TimeStamp": datetime,
        "IsIndirectActivity": bool,
        "OrganizationId": str,
        "Initiator": UserMetadataTypeDef,
        "Participants": ParticipantsTypeDef,
        "ResourceMetadata": ResourceMetadataTypeDef,
        "OriginalParent": ResourceMetadataTypeDef,
        "CommentMetadata": CommentMetadataTypeDef,
    },
    total=False,
)

ResponseItemTypeDef = TypedDict(
    "ResponseItemTypeDef",
    {
        "ResourceType": ResponseItemTypeType,
        "WebUrl": str,
        "DocumentMetadata": DocumentMetadataTypeDef,
        "FolderMetadata": FolderMetadataTypeDef,
        "CommentMetadata": CommentMetadataTypeDef,
        "DocumentVersionMetadata": DocumentVersionMetadataTypeDef,
    },
    total=False,
)

CreateCommentResponseTypeDef = TypedDict(
    "CreateCommentResponseTypeDef",
    {
        "Comment": CommentTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeCommentsResponseTypeDef = TypedDict(
    "DescribeCommentsResponseTypeDef",
    {
        "Comments": List[CommentTypeDef],
        "Marker": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeActivitiesResponseTypeDef = TypedDict(
    "DescribeActivitiesResponseTypeDef",
    {
        "UserActivities": List[ActivityTypeDef],
        "Marker": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

SearchResourcesResponseTypeDef = TypedDict(
    "SearchResourcesResponseTypeDef",
    {
        "Items": List[ResponseItemTypeDef],
        "Marker": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)
