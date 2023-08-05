"""
Type annotations for es service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_es.client import ElasticsearchServiceClient

    session = Session()
    client: ElasticsearchServiceClient = session.client("es")
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from botocore.client import BaseClient, ClientMeta

from .literals import EngineTypeType, ESPartitionInstanceTypeType, LogTypeType
from .paginator import (
    DescribeReservedElasticsearchInstanceOfferingsPaginator,
    DescribeReservedElasticsearchInstancesPaginator,
    GetUpgradeHistoryPaginator,
    ListElasticsearchInstanceTypesPaginator,
    ListElasticsearchVersionsPaginator,
)
from .type_defs import (
    AcceptInboundCrossClusterSearchConnectionResponseTypeDef,
    AdvancedSecurityOptionsInputTypeDef,
    AssociatePackageResponseTypeDef,
    AuthorizeVpcEndpointAccessResponseTypeDef,
    AutoTuneOptionsInputTypeDef,
    AutoTuneOptionsTypeDef,
    CancelElasticsearchServiceSoftwareUpdateResponseTypeDef,
    CognitoOptionsTypeDef,
    CreateElasticsearchDomainResponseTypeDef,
    CreateOutboundCrossClusterSearchConnectionResponseTypeDef,
    CreatePackageResponseTypeDef,
    CreateVpcEndpointResponseTypeDef,
    DeleteElasticsearchDomainResponseTypeDef,
    DeleteInboundCrossClusterSearchConnectionResponseTypeDef,
    DeleteOutboundCrossClusterSearchConnectionResponseTypeDef,
    DeletePackageResponseTypeDef,
    DeleteVpcEndpointResponseTypeDef,
    DescribeDomainAutoTunesResponseTypeDef,
    DescribeDomainChangeProgressResponseTypeDef,
    DescribeElasticsearchDomainConfigResponseTypeDef,
    DescribeElasticsearchDomainResponseTypeDef,
    DescribeElasticsearchDomainsResponseTypeDef,
    DescribeElasticsearchInstanceTypeLimitsResponseTypeDef,
    DescribeInboundCrossClusterSearchConnectionsResponseTypeDef,
    DescribeOutboundCrossClusterSearchConnectionsResponseTypeDef,
    DescribePackagesFilterTypeDef,
    DescribePackagesResponseTypeDef,
    DescribeReservedElasticsearchInstanceOfferingsResponseTypeDef,
    DescribeReservedElasticsearchInstancesResponseTypeDef,
    DescribeVpcEndpointsResponseTypeDef,
    DissociatePackageResponseTypeDef,
    DomainEndpointOptionsTypeDef,
    DomainInformationTypeDef,
    EBSOptionsTypeDef,
    ElasticsearchClusterConfigTypeDef,
    EmptyResponseMetadataTypeDef,
    EncryptionAtRestOptionsTypeDef,
    FilterTypeDef,
    GetCompatibleElasticsearchVersionsResponseTypeDef,
    GetPackageVersionHistoryResponseTypeDef,
    GetUpgradeHistoryResponseTypeDef,
    GetUpgradeStatusResponseTypeDef,
    ListDomainNamesResponseTypeDef,
    ListDomainsForPackageResponseTypeDef,
    ListElasticsearchInstanceTypesResponseTypeDef,
    ListElasticsearchVersionsResponseTypeDef,
    ListPackagesForDomainResponseTypeDef,
    ListTagsResponseTypeDef,
    ListVpcEndpointAccessResponseTypeDef,
    ListVpcEndpointsForDomainResponseTypeDef,
    ListVpcEndpointsResponseTypeDef,
    LogPublishingOptionTypeDef,
    NodeToNodeEncryptionOptionsTypeDef,
    PackageSourceTypeDef,
    PurchaseReservedElasticsearchInstanceOfferingResponseTypeDef,
    RejectInboundCrossClusterSearchConnectionResponseTypeDef,
    SnapshotOptionsTypeDef,
    StartElasticsearchServiceSoftwareUpdateResponseTypeDef,
    TagTypeDef,
    UpdateElasticsearchDomainConfigResponseTypeDef,
    UpdatePackageResponseTypeDef,
    UpdateVpcEndpointResponseTypeDef,
    UpgradeElasticsearchDomainResponseTypeDef,
    VPCOptionsTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("ElasticsearchServiceClient",)

class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    BaseException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    DisabledOperationException: Type[BotocoreClientError]
    InternalException: Type[BotocoreClientError]
    InvalidPaginationTokenException: Type[BotocoreClientError]
    InvalidTypeException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ResourceAlreadyExistsException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class ElasticsearchServiceClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ElasticsearchServiceClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#exceptions)
        """
    def accept_inbound_cross_cluster_search_connection(
        self, *, CrossClusterSearchConnectionId: str
    ) -> AcceptInboundCrossClusterSearchConnectionResponseTypeDef:
        """
        Allows the destination domain owner to accept an inbound cross-cluster search
        connection request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.accept_inbound_cross_cluster_search_connection)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#accept_inbound_cross_cluster_search_connection)
        """
    def add_tags(self, *, ARN: str, TagList: Sequence[TagTypeDef]) -> EmptyResponseMetadataTypeDef:
        """
        Attaches tags to an existing Elasticsearch domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.add_tags)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#add_tags)
        """
    def associate_package(
        self, *, PackageID: str, DomainName: str
    ) -> AssociatePackageResponseTypeDef:
        """
        Associates a package with an Amazon ES domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.associate_package)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#associate_package)
        """
    def authorize_vpc_endpoint_access(
        self, *, DomainName: str, Account: str
    ) -> AuthorizeVpcEndpointAccessResponseTypeDef:
        """
        Provides access to an Amazon OpenSearch Service domain through the use of an
        interface VPC endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.authorize_vpc_endpoint_access)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#authorize_vpc_endpoint_access)
        """
    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#can_paginate)
        """
    def cancel_elasticsearch_service_software_update(
        self, *, DomainName: str
    ) -> CancelElasticsearchServiceSoftwareUpdateResponseTypeDef:
        """
        Cancels a scheduled service software update for an Amazon ES domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.cancel_elasticsearch_service_software_update)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#cancel_elasticsearch_service_software_update)
        """
    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.close)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#close)
        """
    def create_elasticsearch_domain(
        self,
        *,
        DomainName: str,
        ElasticsearchVersion: str = ...,
        ElasticsearchClusterConfig: ElasticsearchClusterConfigTypeDef = ...,
        EBSOptions: EBSOptionsTypeDef = ...,
        AccessPolicies: str = ...,
        SnapshotOptions: SnapshotOptionsTypeDef = ...,
        VPCOptions: VPCOptionsTypeDef = ...,
        CognitoOptions: CognitoOptionsTypeDef = ...,
        EncryptionAtRestOptions: EncryptionAtRestOptionsTypeDef = ...,
        NodeToNodeEncryptionOptions: NodeToNodeEncryptionOptionsTypeDef = ...,
        AdvancedOptions: Mapping[str, str] = ...,
        LogPublishingOptions: Mapping[LogTypeType, LogPublishingOptionTypeDef] = ...,
        DomainEndpointOptions: DomainEndpointOptionsTypeDef = ...,
        AdvancedSecurityOptions: AdvancedSecurityOptionsInputTypeDef = ...,
        AutoTuneOptions: AutoTuneOptionsInputTypeDef = ...,
        TagList: Sequence[TagTypeDef] = ...
    ) -> CreateElasticsearchDomainResponseTypeDef:
        """
        Creates a new Elasticsearch domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.create_elasticsearch_domain)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#create_elasticsearch_domain)
        """
    def create_outbound_cross_cluster_search_connection(
        self,
        *,
        SourceDomainInfo: DomainInformationTypeDef,
        DestinationDomainInfo: DomainInformationTypeDef,
        ConnectionAlias: str
    ) -> CreateOutboundCrossClusterSearchConnectionResponseTypeDef:
        """
        Creates a new cross-cluster search connection from a source domain to a
        destination domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.create_outbound_cross_cluster_search_connection)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#create_outbound_cross_cluster_search_connection)
        """
    def create_package(
        self,
        *,
        PackageName: str,
        PackageType: Literal["TXT-DICTIONARY"],
        PackageSource: PackageSourceTypeDef,
        PackageDescription: str = ...
    ) -> CreatePackageResponseTypeDef:
        """
        Create a package for use with Amazon ES domains.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.create_package)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#create_package)
        """
    def create_vpc_endpoint(
        self, *, DomainArn: str, VpcOptions: VPCOptionsTypeDef, ClientToken: str = ...
    ) -> CreateVpcEndpointResponseTypeDef:
        """
        Creates an Amazon OpenSearch Service-managed VPC endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.create_vpc_endpoint)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#create_vpc_endpoint)
        """
    def delete_elasticsearch_domain(
        self, *, DomainName: str
    ) -> DeleteElasticsearchDomainResponseTypeDef:
        """
        Permanently deletes the specified Elasticsearch domain and all of its data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.delete_elasticsearch_domain)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#delete_elasticsearch_domain)
        """
    def delete_elasticsearch_service_role(self) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the service-linked role that Elasticsearch Service uses to manage and
        maintain VPC domains.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.delete_elasticsearch_service_role)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#delete_elasticsearch_service_role)
        """
    def delete_inbound_cross_cluster_search_connection(
        self, *, CrossClusterSearchConnectionId: str
    ) -> DeleteInboundCrossClusterSearchConnectionResponseTypeDef:
        """
        Allows the destination domain owner to delete an existing inbound cross-cluster
        search connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.delete_inbound_cross_cluster_search_connection)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#delete_inbound_cross_cluster_search_connection)
        """
    def delete_outbound_cross_cluster_search_connection(
        self, *, CrossClusterSearchConnectionId: str
    ) -> DeleteOutboundCrossClusterSearchConnectionResponseTypeDef:
        """
        Allows the source domain owner to delete an existing outbound cross-cluster
        search connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.delete_outbound_cross_cluster_search_connection)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#delete_outbound_cross_cluster_search_connection)
        """
    def delete_package(self, *, PackageID: str) -> DeletePackageResponseTypeDef:
        """
        Delete the package.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.delete_package)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#delete_package)
        """
    def delete_vpc_endpoint(self, *, VpcEndpointId: str) -> DeleteVpcEndpointResponseTypeDef:
        """
        Deletes an Amazon OpenSearch Service-managed interface VPC endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.delete_vpc_endpoint)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#delete_vpc_endpoint)
        """
    def describe_domain_auto_tunes(
        self, *, DomainName: str, MaxResults: int = ..., NextToken: str = ...
    ) -> DescribeDomainAutoTunesResponseTypeDef:
        """
        Provides scheduled Auto-Tune action details for the Elasticsearch domain, such
        as Auto-Tune action type, description, severity, and scheduled date.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.describe_domain_auto_tunes)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#describe_domain_auto_tunes)
        """
    def describe_domain_change_progress(
        self, *, DomainName: str, ChangeId: str = ...
    ) -> DescribeDomainChangeProgressResponseTypeDef:
        """
        Returns information about the current blue/green deployment happening on a
        domain, including a change ID, status, and progress stages.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.describe_domain_change_progress)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#describe_domain_change_progress)
        """
    def describe_elasticsearch_domain(
        self, *, DomainName: str
    ) -> DescribeElasticsearchDomainResponseTypeDef:
        """
        Returns domain configuration information about the specified Elasticsearch
        domain, including the domain ID, domain endpoint, and domain ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.describe_elasticsearch_domain)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#describe_elasticsearch_domain)
        """
    def describe_elasticsearch_domain_config(
        self, *, DomainName: str
    ) -> DescribeElasticsearchDomainConfigResponseTypeDef:
        """
        Provides cluster configuration information about the specified Elasticsearch
        domain, such as the state, creation date, update version, and update date for
        cluster options.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.describe_elasticsearch_domain_config)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#describe_elasticsearch_domain_config)
        """
    def describe_elasticsearch_domains(
        self, *, DomainNames: Sequence[str]
    ) -> DescribeElasticsearchDomainsResponseTypeDef:
        """
        Returns domain configuration information about the specified Elasticsearch
        domains, including the domain ID, domain endpoint, and domain ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.describe_elasticsearch_domains)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#describe_elasticsearch_domains)
        """
    def describe_elasticsearch_instance_type_limits(
        self,
        *,
        InstanceType: ESPartitionInstanceTypeType,
        ElasticsearchVersion: str,
        DomainName: str = ...
    ) -> DescribeElasticsearchInstanceTypeLimitsResponseTypeDef:
        """
        Describe Elasticsearch Limits for a given InstanceType and ElasticsearchVersion.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.describe_elasticsearch_instance_type_limits)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#describe_elasticsearch_instance_type_limits)
        """
    def describe_inbound_cross_cluster_search_connections(
        self, *, Filters: Sequence[FilterTypeDef] = ..., MaxResults: int = ..., NextToken: str = ...
    ) -> DescribeInboundCrossClusterSearchConnectionsResponseTypeDef:
        """
        Lists all the inbound cross-cluster search connections for a destination domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.describe_inbound_cross_cluster_search_connections)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#describe_inbound_cross_cluster_search_connections)
        """
    def describe_outbound_cross_cluster_search_connections(
        self, *, Filters: Sequence[FilterTypeDef] = ..., MaxResults: int = ..., NextToken: str = ...
    ) -> DescribeOutboundCrossClusterSearchConnectionsResponseTypeDef:
        """
        Lists all the outbound cross-cluster search connections for a source domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.describe_outbound_cross_cluster_search_connections)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#describe_outbound_cross_cluster_search_connections)
        """
    def describe_packages(
        self,
        *,
        Filters: Sequence[DescribePackagesFilterTypeDef] = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> DescribePackagesResponseTypeDef:
        """
        Describes all packages available to Amazon ES.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.describe_packages)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#describe_packages)
        """
    def describe_reserved_elasticsearch_instance_offerings(
        self,
        *,
        ReservedElasticsearchInstanceOfferingId: str = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> DescribeReservedElasticsearchInstanceOfferingsResponseTypeDef:
        """
        Lists available reserved Elasticsearch instance offerings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.describe_reserved_elasticsearch_instance_offerings)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#describe_reserved_elasticsearch_instance_offerings)
        """
    def describe_reserved_elasticsearch_instances(
        self,
        *,
        ReservedElasticsearchInstanceId: str = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> DescribeReservedElasticsearchInstancesResponseTypeDef:
        """
        Returns information about reserved Elasticsearch instances for this account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.describe_reserved_elasticsearch_instances)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#describe_reserved_elasticsearch_instances)
        """
    def describe_vpc_endpoints(
        self, *, VpcEndpointIds: Sequence[str]
    ) -> DescribeVpcEndpointsResponseTypeDef:
        """
        Describes one or more Amazon OpenSearch Service-managed VPC endpoints.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.describe_vpc_endpoints)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#describe_vpc_endpoints)
        """
    def dissociate_package(
        self, *, PackageID: str, DomainName: str
    ) -> DissociatePackageResponseTypeDef:
        """
        Dissociates a package from the Amazon ES domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.dissociate_package)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#dissociate_package)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#generate_presigned_url)
        """
    def get_compatible_elasticsearch_versions(
        self, *, DomainName: str = ...
    ) -> GetCompatibleElasticsearchVersionsResponseTypeDef:
        """
        Returns a list of upgrade compatible Elastisearch versions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.get_compatible_elasticsearch_versions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#get_compatible_elasticsearch_versions)
        """
    def get_package_version_history(
        self, *, PackageID: str, MaxResults: int = ..., NextToken: str = ...
    ) -> GetPackageVersionHistoryResponseTypeDef:
        """
        Returns a list of versions of the package, along with their creation time and
        commit message.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.get_package_version_history)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#get_package_version_history)
        """
    def get_upgrade_history(
        self, *, DomainName: str, MaxResults: int = ..., NextToken: str = ...
    ) -> GetUpgradeHistoryResponseTypeDef:
        """
        Retrieves the complete history of the last 10 upgrades that were performed on
        the domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.get_upgrade_history)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#get_upgrade_history)
        """
    def get_upgrade_status(self, *, DomainName: str) -> GetUpgradeStatusResponseTypeDef:
        """
        Retrieves the latest status of the last upgrade or upgrade eligibility check
        that was performed on the domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.get_upgrade_status)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#get_upgrade_status)
        """
    def list_domain_names(
        self, *, EngineType: EngineTypeType = ...
    ) -> ListDomainNamesResponseTypeDef:
        """
        Returns the name of all Elasticsearch domains owned by the current user's
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.list_domain_names)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#list_domain_names)
        """
    def list_domains_for_package(
        self, *, PackageID: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListDomainsForPackageResponseTypeDef:
        """
        Lists all Amazon ES domains associated with the package.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.list_domains_for_package)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#list_domains_for_package)
        """
    def list_elasticsearch_instance_types(
        self,
        *,
        ElasticsearchVersion: str,
        DomainName: str = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> ListElasticsearchInstanceTypesResponseTypeDef:
        """
        List all Elasticsearch instance types that are supported for given
        ElasticsearchVersion See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/es-2015-01-01/ListElasticsearchInstanceTypes).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.list_elasticsearch_instance_types)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#list_elasticsearch_instance_types)
        """
    def list_elasticsearch_versions(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListElasticsearchVersionsResponseTypeDef:
        """
        List all supported Elasticsearch versions See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/es-2015-01-01/ListElasticsearchVersions).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.list_elasticsearch_versions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#list_elasticsearch_versions)
        """
    def list_packages_for_domain(
        self, *, DomainName: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListPackagesForDomainResponseTypeDef:
        """
        Lists all packages associated with the Amazon ES domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.list_packages_for_domain)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#list_packages_for_domain)
        """
    def list_tags(self, *, ARN: str) -> ListTagsResponseTypeDef:
        """
        Returns all tags for the given Elasticsearch domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.list_tags)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#list_tags)
        """
    def list_vpc_endpoint_access(
        self, *, DomainName: str, NextToken: str = ...
    ) -> ListVpcEndpointAccessResponseTypeDef:
        """
        Retrieves information about each principal that is allowed to access a given
        Amazon OpenSearch Service domain through the use of an interface VPC endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.list_vpc_endpoint_access)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#list_vpc_endpoint_access)
        """
    def list_vpc_endpoints(self, *, NextToken: str = ...) -> ListVpcEndpointsResponseTypeDef:
        """
        Retrieves all Amazon OpenSearch Service-managed VPC endpoints in the current
        account and Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.list_vpc_endpoints)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#list_vpc_endpoints)
        """
    def list_vpc_endpoints_for_domain(
        self, *, DomainName: str, NextToken: str = ...
    ) -> ListVpcEndpointsForDomainResponseTypeDef:
        """
        Retrieves all Amazon OpenSearch Service-managed VPC endpoints associated with a
        particular domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.list_vpc_endpoints_for_domain)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#list_vpc_endpoints_for_domain)
        """
    def purchase_reserved_elasticsearch_instance_offering(
        self,
        *,
        ReservedElasticsearchInstanceOfferingId: str,
        ReservationName: str,
        InstanceCount: int = ...
    ) -> PurchaseReservedElasticsearchInstanceOfferingResponseTypeDef:
        """
        Allows you to purchase reserved Elasticsearch instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.purchase_reserved_elasticsearch_instance_offering)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#purchase_reserved_elasticsearch_instance_offering)
        """
    def reject_inbound_cross_cluster_search_connection(
        self, *, CrossClusterSearchConnectionId: str
    ) -> RejectInboundCrossClusterSearchConnectionResponseTypeDef:
        """
        Allows the destination domain owner to reject an inbound cross-cluster search
        connection request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.reject_inbound_cross_cluster_search_connection)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#reject_inbound_cross_cluster_search_connection)
        """
    def remove_tags(self, *, ARN: str, TagKeys: Sequence[str]) -> EmptyResponseMetadataTypeDef:
        """
        Removes the specified set of tags from the specified Elasticsearch domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.remove_tags)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#remove_tags)
        """
    def revoke_vpc_endpoint_access(self, *, DomainName: str, Account: str) -> Dict[str, Any]:
        """
        Revokes access to an Amazon OpenSearch Service domain that was provided through
        an interface VPC endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.revoke_vpc_endpoint_access)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#revoke_vpc_endpoint_access)
        """
    def start_elasticsearch_service_software_update(
        self, *, DomainName: str
    ) -> StartElasticsearchServiceSoftwareUpdateResponseTypeDef:
        """
        Schedules a service software update for an Amazon ES domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.start_elasticsearch_service_software_update)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#start_elasticsearch_service_software_update)
        """
    def update_elasticsearch_domain_config(
        self,
        *,
        DomainName: str,
        ElasticsearchClusterConfig: ElasticsearchClusterConfigTypeDef = ...,
        EBSOptions: EBSOptionsTypeDef = ...,
        SnapshotOptions: SnapshotOptionsTypeDef = ...,
        VPCOptions: VPCOptionsTypeDef = ...,
        CognitoOptions: CognitoOptionsTypeDef = ...,
        AdvancedOptions: Mapping[str, str] = ...,
        AccessPolicies: str = ...,
        LogPublishingOptions: Mapping[LogTypeType, LogPublishingOptionTypeDef] = ...,
        DomainEndpointOptions: DomainEndpointOptionsTypeDef = ...,
        AdvancedSecurityOptions: AdvancedSecurityOptionsInputTypeDef = ...,
        NodeToNodeEncryptionOptions: NodeToNodeEncryptionOptionsTypeDef = ...,
        EncryptionAtRestOptions: EncryptionAtRestOptionsTypeDef = ...,
        AutoTuneOptions: AutoTuneOptionsTypeDef = ...,
        DryRun: bool = ...
    ) -> UpdateElasticsearchDomainConfigResponseTypeDef:
        """
        Modifies the cluster configuration of the specified Elasticsearch domain,
        setting as setting the instance type and the number of instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.update_elasticsearch_domain_config)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#update_elasticsearch_domain_config)
        """
    def update_package(
        self,
        *,
        PackageID: str,
        PackageSource: PackageSourceTypeDef,
        PackageDescription: str = ...,
        CommitMessage: str = ...
    ) -> UpdatePackageResponseTypeDef:
        """
        Updates a package for use with Amazon ES domains.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.update_package)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#update_package)
        """
    def update_vpc_endpoint(
        self, *, VpcEndpointId: str, VpcOptions: VPCOptionsTypeDef
    ) -> UpdateVpcEndpointResponseTypeDef:
        """
        Modifies an Amazon OpenSearch Service-managed interface VPC endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.update_vpc_endpoint)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#update_vpc_endpoint)
        """
    def upgrade_elasticsearch_domain(
        self, *, DomainName: str, TargetVersion: str, PerformCheckOnly: bool = ...
    ) -> UpgradeElasticsearchDomainResponseTypeDef:
        """
        Allows you to either upgrade your domain or perform an Upgrade eligibility check
        to a compatible Elasticsearch version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.upgrade_elasticsearch_domain)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#upgrade_elasticsearch_domain)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["describe_reserved_elasticsearch_instance_offerings"]
    ) -> DescribeReservedElasticsearchInstanceOfferingsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["describe_reserved_elasticsearch_instances"]
    ) -> DescribeReservedElasticsearchInstancesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["get_upgrade_history"]
    ) -> GetUpgradeHistoryPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_elasticsearch_instance_types"]
    ) -> ListElasticsearchInstanceTypesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_elasticsearch_versions"]
    ) -> ListElasticsearchVersionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_es/client/#get_paginator)
        """
