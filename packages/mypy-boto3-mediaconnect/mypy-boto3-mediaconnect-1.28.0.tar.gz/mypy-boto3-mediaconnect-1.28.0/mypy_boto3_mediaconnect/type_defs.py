"""
Type annotations for mediaconnect service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediaconnect/type_defs/)

Usage::

    ```python
    from mypy_boto3_mediaconnect.type_defs import VpcInterfaceAttachmentTypeDef

    data: VpcInterfaceAttachmentTypeDef = {...}
    ```
"""
import sys
from typing import Dict, List, Mapping, Sequence

from .literals import (
    AlgorithmType,
    BridgePlacementType,
    BridgeStateType,
    ColorimetryType,
    ConnectionStatusType,
    DesiredStateType,
    EncoderProfileType,
    EncodingNameType,
    EntitlementStatusType,
    FailoverModeType,
    GatewayStateType,
    InstanceStateType,
    KeyTypeType,
    MaintenanceDayType,
    MediaStreamTypeType,
    NetworkInterfaceTypeType,
    ProtocolType,
    RangeType,
    ReservationStateType,
    ScanModeType,
    SourceTypeType,
    StateType,
    StatusType,
    TcsType,
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
    "VpcInterfaceAttachmentTypeDef",
    "AddBridgeNetworkOutputRequestTypeDef",
    "AddBridgeNetworkSourceRequestTypeDef",
    "AddEgressGatewayBridgeRequestTypeDef",
    "VpcInterfaceRequestTypeDef",
    "VpcInterfaceTypeDef",
    "AddIngressGatewayBridgeRequestTypeDef",
    "AddMaintenanceTypeDef",
    "EncryptionTypeDef",
    "BridgeFlowOutputTypeDef",
    "BridgeNetworkOutputTypeDef",
    "BridgeNetworkSourceTypeDef",
    "EgressGatewayBridgeTypeDef",
    "IngressGatewayBridgeTypeDef",
    "MessageDetailTypeDef",
    "GatewayNetworkTypeDef",
    "DeleteBridgeRequestRequestTypeDef",
    "DeleteBridgeResponseTypeDef",
    "DeleteFlowRequestRequestTypeDef",
    "DeleteFlowResponseTypeDef",
    "DeleteGatewayRequestRequestTypeDef",
    "DeleteGatewayResponseTypeDef",
    "DeregisterGatewayInstanceRequestRequestTypeDef",
    "DeregisterGatewayInstanceResponseTypeDef",
    "DescribeBridgeRequestRequestTypeDef",
    "WaiterConfigTypeDef",
    "DescribeFlowRequestRequestTypeDef",
    "MessagesTypeDef",
    "DescribeGatewayInstanceRequestRequestTypeDef",
    "DescribeGatewayRequestRequestTypeDef",
    "DescribeOfferingRequestRequestTypeDef",
    "DescribeReservationRequestRequestTypeDef",
    "InterfaceRequestTypeDef",
    "InterfaceTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EncodingParametersRequestTypeDef",
    "EncodingParametersTypeDef",
    "SourcePriorityTypeDef",
    "MaintenanceTypeDef",
    "FmtpRequestTypeDef",
    "FmtpTypeDef",
    "ListBridgesRequestListBridgesPaginateTypeDef",
    "ListBridgesRequestRequestTypeDef",
    "ListedBridgeTypeDef",
    "ListEntitlementsRequestListEntitlementsPaginateTypeDef",
    "ListEntitlementsRequestRequestTypeDef",
    "ListedEntitlementTypeDef",
    "ListFlowsRequestListFlowsPaginateTypeDef",
    "ListFlowsRequestRequestTypeDef",
    "ListGatewayInstancesRequestListGatewayInstancesPaginateTypeDef",
    "ListGatewayInstancesRequestRequestTypeDef",
    "ListedGatewayInstanceTypeDef",
    "ListGatewaysRequestListGatewaysPaginateTypeDef",
    "ListGatewaysRequestRequestTypeDef",
    "ListedGatewayTypeDef",
    "ListOfferingsRequestListOfferingsPaginateTypeDef",
    "ListOfferingsRequestRequestTypeDef",
    "ListReservationsRequestListReservationsPaginateTypeDef",
    "ListReservationsRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ResourceSpecificationTypeDef",
    "TransportTypeDef",
    "PaginatorConfigTypeDef",
    "PurchaseOfferingRequestRequestTypeDef",
    "RemoveBridgeOutputRequestRequestTypeDef",
    "RemoveBridgeOutputResponseTypeDef",
    "RemoveBridgeSourceRequestRequestTypeDef",
    "RemoveBridgeSourceResponseTypeDef",
    "RemoveFlowMediaStreamRequestRequestTypeDef",
    "RemoveFlowMediaStreamResponseTypeDef",
    "RemoveFlowOutputRequestRequestTypeDef",
    "RemoveFlowOutputResponseTypeDef",
    "RemoveFlowSourceRequestRequestTypeDef",
    "RemoveFlowSourceResponseTypeDef",
    "RemoveFlowVpcInterfaceRequestRequestTypeDef",
    "RemoveFlowVpcInterfaceResponseTypeDef",
    "ResponseMetadataTypeDef",
    "RevokeFlowEntitlementRequestRequestTypeDef",
    "RevokeFlowEntitlementResponseTypeDef",
    "StartFlowRequestRequestTypeDef",
    "StartFlowResponseTypeDef",
    "StopFlowRequestRequestTypeDef",
    "StopFlowResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateBridgeNetworkOutputRequestTypeDef",
    "UpdateBridgeNetworkSourceRequestTypeDef",
    "UpdateEgressGatewayBridgeRequestTypeDef",
    "UpdateIngressGatewayBridgeRequestTypeDef",
    "UpdateBridgeStateRequestRequestTypeDef",
    "UpdateBridgeStateResponseTypeDef",
    "UpdateEncryptionTypeDef",
    "UpdateMaintenanceTypeDef",
    "UpdateGatewayInstanceRequestRequestTypeDef",
    "UpdateGatewayInstanceResponseTypeDef",
    "AddBridgeFlowSourceRequestTypeDef",
    "BridgeFlowSourceTypeDef",
    "GatewayBridgeSourceTypeDef",
    "SetGatewayBridgeSourceRequestTypeDef",
    "UpdateBridgeFlowSourceRequestTypeDef",
    "UpdateGatewayBridgeSourceRequestTypeDef",
    "AddBridgeOutputRequestTypeDef",
    "AddFlowVpcInterfacesRequestRequestTypeDef",
    "AddFlowVpcInterfacesResponseTypeDef",
    "EntitlementTypeDef",
    "GrantEntitlementRequestTypeDef",
    "BridgeOutputTypeDef",
    "GatewayInstanceTypeDef",
    "CreateGatewayRequestRequestTypeDef",
    "GatewayTypeDef",
    "DescribeFlowRequestFlowActiveWaitTypeDef",
    "DescribeFlowRequestFlowDeletedWaitTypeDef",
    "DescribeFlowRequestFlowStandbyWaitTypeDef",
    "DestinationConfigurationRequestTypeDef",
    "InputConfigurationRequestTypeDef",
    "DestinationConfigurationTypeDef",
    "InputConfigurationTypeDef",
    "FailoverConfigTypeDef",
    "UpdateFailoverConfigTypeDef",
    "ListedFlowTypeDef",
    "MediaStreamAttributesRequestTypeDef",
    "MediaStreamAttributesTypeDef",
    "ListBridgesResponseTypeDef",
    "ListEntitlementsResponseTypeDef",
    "ListGatewayInstancesResponseTypeDef",
    "ListGatewaysResponseTypeDef",
    "OfferingTypeDef",
    "ReservationTypeDef",
    "UpdateBridgeOutputRequestRequestTypeDef",
    "UpdateFlowEntitlementRequestRequestTypeDef",
    "AddBridgeSourceRequestTypeDef",
    "BridgeSourceTypeDef",
    "UpdateBridgeSourceRequestRequestTypeDef",
    "AddBridgeOutputsRequestRequestTypeDef",
    "GrantFlowEntitlementsResponseTypeDef",
    "UpdateFlowEntitlementResponseTypeDef",
    "GrantFlowEntitlementsRequestRequestTypeDef",
    "AddBridgeOutputsResponseTypeDef",
    "UpdateBridgeOutputResponseTypeDef",
    "DescribeGatewayInstanceResponseTypeDef",
    "CreateGatewayResponseTypeDef",
    "DescribeGatewayResponseTypeDef",
    "MediaStreamOutputConfigurationRequestTypeDef",
    "MediaStreamSourceConfigurationRequestTypeDef",
    "MediaStreamOutputConfigurationTypeDef",
    "MediaStreamSourceConfigurationTypeDef",
    "UpdateBridgeRequestRequestTypeDef",
    "UpdateFlowRequestRequestTypeDef",
    "ListFlowsResponseTypeDef",
    "AddMediaStreamRequestTypeDef",
    "UpdateFlowMediaStreamRequestRequestTypeDef",
    "MediaStreamTypeDef",
    "DescribeOfferingResponseTypeDef",
    "ListOfferingsResponseTypeDef",
    "DescribeReservationResponseTypeDef",
    "ListReservationsResponseTypeDef",
    "PurchaseOfferingResponseTypeDef",
    "AddBridgeSourcesRequestRequestTypeDef",
    "CreateBridgeRequestRequestTypeDef",
    "AddBridgeSourcesResponseTypeDef",
    "BridgeTypeDef",
    "UpdateBridgeSourceResponseTypeDef",
    "AddOutputRequestTypeDef",
    "UpdateFlowOutputRequestRequestTypeDef",
    "SetSourceRequestTypeDef",
    "UpdateFlowSourceRequestRequestTypeDef",
    "OutputTypeDef",
    "SourceTypeDef",
    "AddFlowMediaStreamsRequestRequestTypeDef",
    "AddFlowMediaStreamsResponseTypeDef",
    "UpdateFlowMediaStreamResponseTypeDef",
    "CreateBridgeResponseTypeDef",
    "DescribeBridgeResponseTypeDef",
    "UpdateBridgeResponseTypeDef",
    "AddFlowOutputsRequestRequestTypeDef",
    "AddFlowSourcesRequestRequestTypeDef",
    "CreateFlowRequestRequestTypeDef",
    "AddFlowOutputsResponseTypeDef",
    "UpdateFlowOutputResponseTypeDef",
    "AddFlowSourcesResponseTypeDef",
    "FlowTypeDef",
    "UpdateFlowSourceResponseTypeDef",
    "CreateFlowResponseTypeDef",
    "DescribeFlowResponseTypeDef",
    "UpdateFlowResponseTypeDef",
)

VpcInterfaceAttachmentTypeDef = TypedDict(
    "VpcInterfaceAttachmentTypeDef",
    {
        "VpcInterfaceName": str,
    },
    total=False,
)

AddBridgeNetworkOutputRequestTypeDef = TypedDict(
    "AddBridgeNetworkOutputRequestTypeDef",
    {
        "IpAddress": str,
        "Name": str,
        "NetworkName": str,
        "Port": int,
        "Protocol": ProtocolType,
        "Ttl": int,
    },
)

AddBridgeNetworkSourceRequestTypeDef = TypedDict(
    "AddBridgeNetworkSourceRequestTypeDef",
    {
        "MulticastIp": str,
        "Name": str,
        "NetworkName": str,
        "Port": int,
        "Protocol": ProtocolType,
    },
)

AddEgressGatewayBridgeRequestTypeDef = TypedDict(
    "AddEgressGatewayBridgeRequestTypeDef",
    {
        "MaxBitrate": int,
    },
)

_RequiredVpcInterfaceRequestTypeDef = TypedDict(
    "_RequiredVpcInterfaceRequestTypeDef",
    {
        "Name": str,
        "RoleArn": str,
        "SecurityGroupIds": Sequence[str],
        "SubnetId": str,
    },
)
_OptionalVpcInterfaceRequestTypeDef = TypedDict(
    "_OptionalVpcInterfaceRequestTypeDef",
    {
        "NetworkInterfaceType": NetworkInterfaceTypeType,
    },
    total=False,
)


class VpcInterfaceRequestTypeDef(
    _RequiredVpcInterfaceRequestTypeDef, _OptionalVpcInterfaceRequestTypeDef
):
    pass


VpcInterfaceTypeDef = TypedDict(
    "VpcInterfaceTypeDef",
    {
        "Name": str,
        "NetworkInterfaceIds": List[str],
        "NetworkInterfaceType": NetworkInterfaceTypeType,
        "RoleArn": str,
        "SecurityGroupIds": List[str],
        "SubnetId": str,
    },
)

AddIngressGatewayBridgeRequestTypeDef = TypedDict(
    "AddIngressGatewayBridgeRequestTypeDef",
    {
        "MaxBitrate": int,
        "MaxOutputs": int,
    },
)

AddMaintenanceTypeDef = TypedDict(
    "AddMaintenanceTypeDef",
    {
        "MaintenanceDay": MaintenanceDayType,
        "MaintenanceStartHour": str,
    },
)

_RequiredEncryptionTypeDef = TypedDict(
    "_RequiredEncryptionTypeDef",
    {
        "RoleArn": str,
    },
)
_OptionalEncryptionTypeDef = TypedDict(
    "_OptionalEncryptionTypeDef",
    {
        "Algorithm": AlgorithmType,
        "ConstantInitializationVector": str,
        "DeviceId": str,
        "KeyType": KeyTypeType,
        "Region": str,
        "ResourceId": str,
        "SecretArn": str,
        "Url": str,
    },
    total=False,
)


class EncryptionTypeDef(_RequiredEncryptionTypeDef, _OptionalEncryptionTypeDef):
    pass


BridgeFlowOutputTypeDef = TypedDict(
    "BridgeFlowOutputTypeDef",
    {
        "FlowArn": str,
        "FlowSourceArn": str,
        "Name": str,
    },
)

BridgeNetworkOutputTypeDef = TypedDict(
    "BridgeNetworkOutputTypeDef",
    {
        "IpAddress": str,
        "Name": str,
        "NetworkName": str,
        "Port": int,
        "Protocol": ProtocolType,
        "Ttl": int,
    },
)

BridgeNetworkSourceTypeDef = TypedDict(
    "BridgeNetworkSourceTypeDef",
    {
        "MulticastIp": str,
        "Name": str,
        "NetworkName": str,
        "Port": int,
        "Protocol": ProtocolType,
    },
)

_RequiredEgressGatewayBridgeTypeDef = TypedDict(
    "_RequiredEgressGatewayBridgeTypeDef",
    {
        "MaxBitrate": int,
    },
)
_OptionalEgressGatewayBridgeTypeDef = TypedDict(
    "_OptionalEgressGatewayBridgeTypeDef",
    {
        "InstanceId": str,
    },
    total=False,
)


class EgressGatewayBridgeTypeDef(
    _RequiredEgressGatewayBridgeTypeDef, _OptionalEgressGatewayBridgeTypeDef
):
    pass


_RequiredIngressGatewayBridgeTypeDef = TypedDict(
    "_RequiredIngressGatewayBridgeTypeDef",
    {
        "MaxBitrate": int,
        "MaxOutputs": int,
    },
)
_OptionalIngressGatewayBridgeTypeDef = TypedDict(
    "_OptionalIngressGatewayBridgeTypeDef",
    {
        "InstanceId": str,
    },
    total=False,
)


class IngressGatewayBridgeTypeDef(
    _RequiredIngressGatewayBridgeTypeDef, _OptionalIngressGatewayBridgeTypeDef
):
    pass


_RequiredMessageDetailTypeDef = TypedDict(
    "_RequiredMessageDetailTypeDef",
    {
        "Code": str,
        "Message": str,
    },
)
_OptionalMessageDetailTypeDef = TypedDict(
    "_OptionalMessageDetailTypeDef",
    {
        "ResourceName": str,
    },
    total=False,
)


class MessageDetailTypeDef(_RequiredMessageDetailTypeDef, _OptionalMessageDetailTypeDef):
    pass


GatewayNetworkTypeDef = TypedDict(
    "GatewayNetworkTypeDef",
    {
        "CidrBlock": str,
        "Name": str,
    },
)

DeleteBridgeRequestRequestTypeDef = TypedDict(
    "DeleteBridgeRequestRequestTypeDef",
    {
        "BridgeArn": str,
    },
)

DeleteBridgeResponseTypeDef = TypedDict(
    "DeleteBridgeResponseTypeDef",
    {
        "BridgeArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteFlowRequestRequestTypeDef = TypedDict(
    "DeleteFlowRequestRequestTypeDef",
    {
        "FlowArn": str,
    },
)

DeleteFlowResponseTypeDef = TypedDict(
    "DeleteFlowResponseTypeDef",
    {
        "FlowArn": str,
        "Status": StatusType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteGatewayRequestRequestTypeDef = TypedDict(
    "DeleteGatewayRequestRequestTypeDef",
    {
        "GatewayArn": str,
    },
)

DeleteGatewayResponseTypeDef = TypedDict(
    "DeleteGatewayResponseTypeDef",
    {
        "GatewayArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredDeregisterGatewayInstanceRequestRequestTypeDef = TypedDict(
    "_RequiredDeregisterGatewayInstanceRequestRequestTypeDef",
    {
        "GatewayInstanceArn": str,
    },
)
_OptionalDeregisterGatewayInstanceRequestRequestTypeDef = TypedDict(
    "_OptionalDeregisterGatewayInstanceRequestRequestTypeDef",
    {
        "Force": bool,
    },
    total=False,
)


class DeregisterGatewayInstanceRequestRequestTypeDef(
    _RequiredDeregisterGatewayInstanceRequestRequestTypeDef,
    _OptionalDeregisterGatewayInstanceRequestRequestTypeDef,
):
    pass


DeregisterGatewayInstanceResponseTypeDef = TypedDict(
    "DeregisterGatewayInstanceResponseTypeDef",
    {
        "GatewayInstanceArn": str,
        "InstanceState": InstanceStateType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeBridgeRequestRequestTypeDef = TypedDict(
    "DescribeBridgeRequestRequestTypeDef",
    {
        "BridgeArn": str,
    },
)

WaiterConfigTypeDef = TypedDict(
    "WaiterConfigTypeDef",
    {
        "Delay": int,
        "MaxAttempts": int,
    },
    total=False,
)

DescribeFlowRequestRequestTypeDef = TypedDict(
    "DescribeFlowRequestRequestTypeDef",
    {
        "FlowArn": str,
    },
)

MessagesTypeDef = TypedDict(
    "MessagesTypeDef",
    {
        "Errors": List[str],
    },
)

DescribeGatewayInstanceRequestRequestTypeDef = TypedDict(
    "DescribeGatewayInstanceRequestRequestTypeDef",
    {
        "GatewayInstanceArn": str,
    },
)

DescribeGatewayRequestRequestTypeDef = TypedDict(
    "DescribeGatewayRequestRequestTypeDef",
    {
        "GatewayArn": str,
    },
)

DescribeOfferingRequestRequestTypeDef = TypedDict(
    "DescribeOfferingRequestRequestTypeDef",
    {
        "OfferingArn": str,
    },
)

DescribeReservationRequestRequestTypeDef = TypedDict(
    "DescribeReservationRequestRequestTypeDef",
    {
        "ReservationArn": str,
    },
)

InterfaceRequestTypeDef = TypedDict(
    "InterfaceRequestTypeDef",
    {
        "Name": str,
    },
)

InterfaceTypeDef = TypedDict(
    "InterfaceTypeDef",
    {
        "Name": str,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

EncodingParametersRequestTypeDef = TypedDict(
    "EncodingParametersRequestTypeDef",
    {
        "CompressionFactor": float,
        "EncoderProfile": EncoderProfileType,
    },
)

EncodingParametersTypeDef = TypedDict(
    "EncodingParametersTypeDef",
    {
        "CompressionFactor": float,
        "EncoderProfile": EncoderProfileType,
    },
)

SourcePriorityTypeDef = TypedDict(
    "SourcePriorityTypeDef",
    {
        "PrimarySource": str,
    },
    total=False,
)

MaintenanceTypeDef = TypedDict(
    "MaintenanceTypeDef",
    {
        "MaintenanceDay": MaintenanceDayType,
        "MaintenanceDeadline": str,
        "MaintenanceScheduledDate": str,
        "MaintenanceStartHour": str,
    },
    total=False,
)

FmtpRequestTypeDef = TypedDict(
    "FmtpRequestTypeDef",
    {
        "ChannelOrder": str,
        "Colorimetry": ColorimetryType,
        "ExactFramerate": str,
        "Par": str,
        "Range": RangeType,
        "ScanMode": ScanModeType,
        "Tcs": TcsType,
    },
    total=False,
)

FmtpTypeDef = TypedDict(
    "FmtpTypeDef",
    {
        "ChannelOrder": str,
        "Colorimetry": ColorimetryType,
        "ExactFramerate": str,
        "Par": str,
        "Range": RangeType,
        "ScanMode": ScanModeType,
        "Tcs": TcsType,
    },
    total=False,
)

ListBridgesRequestListBridgesPaginateTypeDef = TypedDict(
    "ListBridgesRequestListBridgesPaginateTypeDef",
    {
        "FilterArn": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListBridgesRequestRequestTypeDef = TypedDict(
    "ListBridgesRequestRequestTypeDef",
    {
        "FilterArn": str,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListedBridgeTypeDef = TypedDict(
    "ListedBridgeTypeDef",
    {
        "BridgeArn": str,
        "BridgeState": BridgeStateType,
        "BridgeType": str,
        "Name": str,
        "PlacementArn": str,
    },
)

ListEntitlementsRequestListEntitlementsPaginateTypeDef = TypedDict(
    "ListEntitlementsRequestListEntitlementsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListEntitlementsRequestRequestTypeDef = TypedDict(
    "ListEntitlementsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

_RequiredListedEntitlementTypeDef = TypedDict(
    "_RequiredListedEntitlementTypeDef",
    {
        "EntitlementArn": str,
        "EntitlementName": str,
    },
)
_OptionalListedEntitlementTypeDef = TypedDict(
    "_OptionalListedEntitlementTypeDef",
    {
        "DataTransferSubscriberFeePercent": int,
    },
    total=False,
)


class ListedEntitlementTypeDef(
    _RequiredListedEntitlementTypeDef, _OptionalListedEntitlementTypeDef
):
    pass


ListFlowsRequestListFlowsPaginateTypeDef = TypedDict(
    "ListFlowsRequestListFlowsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListFlowsRequestRequestTypeDef = TypedDict(
    "ListFlowsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListGatewayInstancesRequestListGatewayInstancesPaginateTypeDef = TypedDict(
    "ListGatewayInstancesRequestListGatewayInstancesPaginateTypeDef",
    {
        "FilterArn": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListGatewayInstancesRequestRequestTypeDef = TypedDict(
    "ListGatewayInstancesRequestRequestTypeDef",
    {
        "FilterArn": str,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

_RequiredListedGatewayInstanceTypeDef = TypedDict(
    "_RequiredListedGatewayInstanceTypeDef",
    {
        "GatewayArn": str,
        "GatewayInstanceArn": str,
        "InstanceId": str,
    },
)
_OptionalListedGatewayInstanceTypeDef = TypedDict(
    "_OptionalListedGatewayInstanceTypeDef",
    {
        "InstanceState": InstanceStateType,
    },
    total=False,
)


class ListedGatewayInstanceTypeDef(
    _RequiredListedGatewayInstanceTypeDef, _OptionalListedGatewayInstanceTypeDef
):
    pass


ListGatewaysRequestListGatewaysPaginateTypeDef = TypedDict(
    "ListGatewaysRequestListGatewaysPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListGatewaysRequestRequestTypeDef = TypedDict(
    "ListGatewaysRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListedGatewayTypeDef = TypedDict(
    "ListedGatewayTypeDef",
    {
        "GatewayArn": str,
        "GatewayState": GatewayStateType,
        "Name": str,
    },
)

ListOfferingsRequestListOfferingsPaginateTypeDef = TypedDict(
    "ListOfferingsRequestListOfferingsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListOfferingsRequestRequestTypeDef = TypedDict(
    "ListOfferingsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListReservationsRequestListReservationsPaginateTypeDef = TypedDict(
    "ListReservationsRequestListReservationsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListReservationsRequestRequestTypeDef = TypedDict(
    "ListReservationsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "Tags": Dict[str, str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredResourceSpecificationTypeDef = TypedDict(
    "_RequiredResourceSpecificationTypeDef",
    {
        "ResourceType": Literal["Mbps_Outbound_Bandwidth"],
    },
)
_OptionalResourceSpecificationTypeDef = TypedDict(
    "_OptionalResourceSpecificationTypeDef",
    {
        "ReservedBitrate": int,
    },
    total=False,
)


class ResourceSpecificationTypeDef(
    _RequiredResourceSpecificationTypeDef, _OptionalResourceSpecificationTypeDef
):
    pass


_RequiredTransportTypeDef = TypedDict(
    "_RequiredTransportTypeDef",
    {
        "Protocol": ProtocolType,
    },
)
_OptionalTransportTypeDef = TypedDict(
    "_OptionalTransportTypeDef",
    {
        "CidrAllowList": List[str],
        "MaxBitrate": int,
        "MaxLatency": int,
        "MaxSyncBuffer": int,
        "MinLatency": int,
        "RemoteId": str,
        "SenderControlPort": int,
        "SenderIpAddress": str,
        "SmoothingLatency": int,
        "SourceListenerAddress": str,
        "SourceListenerPort": int,
        "StreamId": str,
    },
    total=False,
)


class TransportTypeDef(_RequiredTransportTypeDef, _OptionalTransportTypeDef):
    pass


PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

PurchaseOfferingRequestRequestTypeDef = TypedDict(
    "PurchaseOfferingRequestRequestTypeDef",
    {
        "OfferingArn": str,
        "ReservationName": str,
        "Start": str,
    },
)

RemoveBridgeOutputRequestRequestTypeDef = TypedDict(
    "RemoveBridgeOutputRequestRequestTypeDef",
    {
        "BridgeArn": str,
        "OutputName": str,
    },
)

RemoveBridgeOutputResponseTypeDef = TypedDict(
    "RemoveBridgeOutputResponseTypeDef",
    {
        "BridgeArn": str,
        "OutputName": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

RemoveBridgeSourceRequestRequestTypeDef = TypedDict(
    "RemoveBridgeSourceRequestRequestTypeDef",
    {
        "BridgeArn": str,
        "SourceName": str,
    },
)

RemoveBridgeSourceResponseTypeDef = TypedDict(
    "RemoveBridgeSourceResponseTypeDef",
    {
        "BridgeArn": str,
        "SourceName": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

RemoveFlowMediaStreamRequestRequestTypeDef = TypedDict(
    "RemoveFlowMediaStreamRequestRequestTypeDef",
    {
        "FlowArn": str,
        "MediaStreamName": str,
    },
)

RemoveFlowMediaStreamResponseTypeDef = TypedDict(
    "RemoveFlowMediaStreamResponseTypeDef",
    {
        "FlowArn": str,
        "MediaStreamName": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

RemoveFlowOutputRequestRequestTypeDef = TypedDict(
    "RemoveFlowOutputRequestRequestTypeDef",
    {
        "FlowArn": str,
        "OutputArn": str,
    },
)

RemoveFlowOutputResponseTypeDef = TypedDict(
    "RemoveFlowOutputResponseTypeDef",
    {
        "FlowArn": str,
        "OutputArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

RemoveFlowSourceRequestRequestTypeDef = TypedDict(
    "RemoveFlowSourceRequestRequestTypeDef",
    {
        "FlowArn": str,
        "SourceArn": str,
    },
)

RemoveFlowSourceResponseTypeDef = TypedDict(
    "RemoveFlowSourceResponseTypeDef",
    {
        "FlowArn": str,
        "SourceArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

RemoveFlowVpcInterfaceRequestRequestTypeDef = TypedDict(
    "RemoveFlowVpcInterfaceRequestRequestTypeDef",
    {
        "FlowArn": str,
        "VpcInterfaceName": str,
    },
)

RemoveFlowVpcInterfaceResponseTypeDef = TypedDict(
    "RemoveFlowVpcInterfaceResponseTypeDef",
    {
        "FlowArn": str,
        "NonDeletedNetworkInterfaceIds": List[str],
        "VpcInterfaceName": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
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

RevokeFlowEntitlementRequestRequestTypeDef = TypedDict(
    "RevokeFlowEntitlementRequestRequestTypeDef",
    {
        "EntitlementArn": str,
        "FlowArn": str,
    },
)

RevokeFlowEntitlementResponseTypeDef = TypedDict(
    "RevokeFlowEntitlementResponseTypeDef",
    {
        "EntitlementArn": str,
        "FlowArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StartFlowRequestRequestTypeDef = TypedDict(
    "StartFlowRequestRequestTypeDef",
    {
        "FlowArn": str,
    },
)

StartFlowResponseTypeDef = TypedDict(
    "StartFlowResponseTypeDef",
    {
        "FlowArn": str,
        "Status": StatusType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StopFlowRequestRequestTypeDef = TypedDict(
    "StopFlowRequestRequestTypeDef",
    {
        "FlowArn": str,
    },
)

StopFlowResponseTypeDef = TypedDict(
    "StopFlowResponseTypeDef",
    {
        "FlowArn": str,
        "Status": StatusType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "Tags": Mapping[str, str],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)

UpdateBridgeNetworkOutputRequestTypeDef = TypedDict(
    "UpdateBridgeNetworkOutputRequestTypeDef",
    {
        "IpAddress": str,
        "NetworkName": str,
        "Port": int,
        "Protocol": ProtocolType,
        "Ttl": int,
    },
    total=False,
)

UpdateBridgeNetworkSourceRequestTypeDef = TypedDict(
    "UpdateBridgeNetworkSourceRequestTypeDef",
    {
        "MulticastIp": str,
        "NetworkName": str,
        "Port": int,
        "Protocol": ProtocolType,
    },
    total=False,
)

UpdateEgressGatewayBridgeRequestTypeDef = TypedDict(
    "UpdateEgressGatewayBridgeRequestTypeDef",
    {
        "MaxBitrate": int,
    },
    total=False,
)

UpdateIngressGatewayBridgeRequestTypeDef = TypedDict(
    "UpdateIngressGatewayBridgeRequestTypeDef",
    {
        "MaxBitrate": int,
        "MaxOutputs": int,
    },
    total=False,
)

UpdateBridgeStateRequestRequestTypeDef = TypedDict(
    "UpdateBridgeStateRequestRequestTypeDef",
    {
        "BridgeArn": str,
        "DesiredState": DesiredStateType,
    },
)

UpdateBridgeStateResponseTypeDef = TypedDict(
    "UpdateBridgeStateResponseTypeDef",
    {
        "BridgeArn": str,
        "DesiredState": DesiredStateType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateEncryptionTypeDef = TypedDict(
    "UpdateEncryptionTypeDef",
    {
        "Algorithm": AlgorithmType,
        "ConstantInitializationVector": str,
        "DeviceId": str,
        "KeyType": KeyTypeType,
        "Region": str,
        "ResourceId": str,
        "RoleArn": str,
        "SecretArn": str,
        "Url": str,
    },
    total=False,
)

UpdateMaintenanceTypeDef = TypedDict(
    "UpdateMaintenanceTypeDef",
    {
        "MaintenanceDay": MaintenanceDayType,
        "MaintenanceScheduledDate": str,
        "MaintenanceStartHour": str,
    },
    total=False,
)

_RequiredUpdateGatewayInstanceRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateGatewayInstanceRequestRequestTypeDef",
    {
        "GatewayInstanceArn": str,
    },
)
_OptionalUpdateGatewayInstanceRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateGatewayInstanceRequestRequestTypeDef",
    {
        "BridgePlacement": BridgePlacementType,
    },
    total=False,
)


class UpdateGatewayInstanceRequestRequestTypeDef(
    _RequiredUpdateGatewayInstanceRequestRequestTypeDef,
    _OptionalUpdateGatewayInstanceRequestRequestTypeDef,
):
    pass


UpdateGatewayInstanceResponseTypeDef = TypedDict(
    "UpdateGatewayInstanceResponseTypeDef",
    {
        "BridgePlacement": BridgePlacementType,
        "GatewayInstanceArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredAddBridgeFlowSourceRequestTypeDef = TypedDict(
    "_RequiredAddBridgeFlowSourceRequestTypeDef",
    {
        "FlowArn": str,
        "Name": str,
    },
)
_OptionalAddBridgeFlowSourceRequestTypeDef = TypedDict(
    "_OptionalAddBridgeFlowSourceRequestTypeDef",
    {
        "FlowVpcInterfaceAttachment": VpcInterfaceAttachmentTypeDef,
    },
    total=False,
)


class AddBridgeFlowSourceRequestTypeDef(
    _RequiredAddBridgeFlowSourceRequestTypeDef, _OptionalAddBridgeFlowSourceRequestTypeDef
):
    pass


_RequiredBridgeFlowSourceTypeDef = TypedDict(
    "_RequiredBridgeFlowSourceTypeDef",
    {
        "FlowArn": str,
        "Name": str,
    },
)
_OptionalBridgeFlowSourceTypeDef = TypedDict(
    "_OptionalBridgeFlowSourceTypeDef",
    {
        "FlowVpcInterfaceAttachment": VpcInterfaceAttachmentTypeDef,
        "OutputArn": str,
    },
    total=False,
)


class BridgeFlowSourceTypeDef(_RequiredBridgeFlowSourceTypeDef, _OptionalBridgeFlowSourceTypeDef):
    pass


_RequiredGatewayBridgeSourceTypeDef = TypedDict(
    "_RequiredGatewayBridgeSourceTypeDef",
    {
        "BridgeArn": str,
    },
)
_OptionalGatewayBridgeSourceTypeDef = TypedDict(
    "_OptionalGatewayBridgeSourceTypeDef",
    {
        "VpcInterfaceAttachment": VpcInterfaceAttachmentTypeDef,
    },
    total=False,
)


class GatewayBridgeSourceTypeDef(
    _RequiredGatewayBridgeSourceTypeDef, _OptionalGatewayBridgeSourceTypeDef
):
    pass


_RequiredSetGatewayBridgeSourceRequestTypeDef = TypedDict(
    "_RequiredSetGatewayBridgeSourceRequestTypeDef",
    {
        "BridgeArn": str,
    },
)
_OptionalSetGatewayBridgeSourceRequestTypeDef = TypedDict(
    "_OptionalSetGatewayBridgeSourceRequestTypeDef",
    {
        "VpcInterfaceAttachment": VpcInterfaceAttachmentTypeDef,
    },
    total=False,
)


class SetGatewayBridgeSourceRequestTypeDef(
    _RequiredSetGatewayBridgeSourceRequestTypeDef, _OptionalSetGatewayBridgeSourceRequestTypeDef
):
    pass


UpdateBridgeFlowSourceRequestTypeDef = TypedDict(
    "UpdateBridgeFlowSourceRequestTypeDef",
    {
        "FlowArn": str,
        "FlowVpcInterfaceAttachment": VpcInterfaceAttachmentTypeDef,
    },
    total=False,
)

UpdateGatewayBridgeSourceRequestTypeDef = TypedDict(
    "UpdateGatewayBridgeSourceRequestTypeDef",
    {
        "BridgeArn": str,
        "VpcInterfaceAttachment": VpcInterfaceAttachmentTypeDef,
    },
    total=False,
)

AddBridgeOutputRequestTypeDef = TypedDict(
    "AddBridgeOutputRequestTypeDef",
    {
        "NetworkOutput": AddBridgeNetworkOutputRequestTypeDef,
    },
    total=False,
)

AddFlowVpcInterfacesRequestRequestTypeDef = TypedDict(
    "AddFlowVpcInterfacesRequestRequestTypeDef",
    {
        "FlowArn": str,
        "VpcInterfaces": Sequence[VpcInterfaceRequestTypeDef],
    },
)

AddFlowVpcInterfacesResponseTypeDef = TypedDict(
    "AddFlowVpcInterfacesResponseTypeDef",
    {
        "FlowArn": str,
        "VpcInterfaces": List[VpcInterfaceTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredEntitlementTypeDef = TypedDict(
    "_RequiredEntitlementTypeDef",
    {
        "EntitlementArn": str,
        "Name": str,
        "Subscribers": List[str],
    },
)
_OptionalEntitlementTypeDef = TypedDict(
    "_OptionalEntitlementTypeDef",
    {
        "DataTransferSubscriberFeePercent": int,
        "Description": str,
        "Encryption": EncryptionTypeDef,
        "EntitlementStatus": EntitlementStatusType,
    },
    total=False,
)


class EntitlementTypeDef(_RequiredEntitlementTypeDef, _OptionalEntitlementTypeDef):
    pass


_RequiredGrantEntitlementRequestTypeDef = TypedDict(
    "_RequiredGrantEntitlementRequestTypeDef",
    {
        "Subscribers": Sequence[str],
    },
)
_OptionalGrantEntitlementRequestTypeDef = TypedDict(
    "_OptionalGrantEntitlementRequestTypeDef",
    {
        "DataTransferSubscriberFeePercent": int,
        "Description": str,
        "Encryption": EncryptionTypeDef,
        "EntitlementStatus": EntitlementStatusType,
        "Name": str,
    },
    total=False,
)


class GrantEntitlementRequestTypeDef(
    _RequiredGrantEntitlementRequestTypeDef, _OptionalGrantEntitlementRequestTypeDef
):
    pass


BridgeOutputTypeDef = TypedDict(
    "BridgeOutputTypeDef",
    {
        "FlowOutput": BridgeFlowOutputTypeDef,
        "NetworkOutput": BridgeNetworkOutputTypeDef,
    },
    total=False,
)

_RequiredGatewayInstanceTypeDef = TypedDict(
    "_RequiredGatewayInstanceTypeDef",
    {
        "BridgePlacement": BridgePlacementType,
        "ConnectionStatus": ConnectionStatusType,
        "GatewayArn": str,
        "GatewayInstanceArn": str,
        "InstanceId": str,
        "InstanceState": InstanceStateType,
        "RunningBridgeCount": int,
    },
)
_OptionalGatewayInstanceTypeDef = TypedDict(
    "_OptionalGatewayInstanceTypeDef",
    {
        "InstanceMessages": List[MessageDetailTypeDef],
    },
    total=False,
)


class GatewayInstanceTypeDef(_RequiredGatewayInstanceTypeDef, _OptionalGatewayInstanceTypeDef):
    pass


CreateGatewayRequestRequestTypeDef = TypedDict(
    "CreateGatewayRequestRequestTypeDef",
    {
        "EgressCidrBlocks": Sequence[str],
        "Name": str,
        "Networks": Sequence[GatewayNetworkTypeDef],
    },
)

_RequiredGatewayTypeDef = TypedDict(
    "_RequiredGatewayTypeDef",
    {
        "EgressCidrBlocks": List[str],
        "GatewayArn": str,
        "Name": str,
        "Networks": List[GatewayNetworkTypeDef],
    },
)
_OptionalGatewayTypeDef = TypedDict(
    "_OptionalGatewayTypeDef",
    {
        "GatewayMessages": List[MessageDetailTypeDef],
        "GatewayState": GatewayStateType,
    },
    total=False,
)


class GatewayTypeDef(_RequiredGatewayTypeDef, _OptionalGatewayTypeDef):
    pass


_RequiredDescribeFlowRequestFlowActiveWaitTypeDef = TypedDict(
    "_RequiredDescribeFlowRequestFlowActiveWaitTypeDef",
    {
        "FlowArn": str,
    },
)
_OptionalDescribeFlowRequestFlowActiveWaitTypeDef = TypedDict(
    "_OptionalDescribeFlowRequestFlowActiveWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)


class DescribeFlowRequestFlowActiveWaitTypeDef(
    _RequiredDescribeFlowRequestFlowActiveWaitTypeDef,
    _OptionalDescribeFlowRequestFlowActiveWaitTypeDef,
):
    pass


_RequiredDescribeFlowRequestFlowDeletedWaitTypeDef = TypedDict(
    "_RequiredDescribeFlowRequestFlowDeletedWaitTypeDef",
    {
        "FlowArn": str,
    },
)
_OptionalDescribeFlowRequestFlowDeletedWaitTypeDef = TypedDict(
    "_OptionalDescribeFlowRequestFlowDeletedWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)


class DescribeFlowRequestFlowDeletedWaitTypeDef(
    _RequiredDescribeFlowRequestFlowDeletedWaitTypeDef,
    _OptionalDescribeFlowRequestFlowDeletedWaitTypeDef,
):
    pass


_RequiredDescribeFlowRequestFlowStandbyWaitTypeDef = TypedDict(
    "_RequiredDescribeFlowRequestFlowStandbyWaitTypeDef",
    {
        "FlowArn": str,
    },
)
_OptionalDescribeFlowRequestFlowStandbyWaitTypeDef = TypedDict(
    "_OptionalDescribeFlowRequestFlowStandbyWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)


class DescribeFlowRequestFlowStandbyWaitTypeDef(
    _RequiredDescribeFlowRequestFlowStandbyWaitTypeDef,
    _OptionalDescribeFlowRequestFlowStandbyWaitTypeDef,
):
    pass


DestinationConfigurationRequestTypeDef = TypedDict(
    "DestinationConfigurationRequestTypeDef",
    {
        "DestinationIp": str,
        "DestinationPort": int,
        "Interface": InterfaceRequestTypeDef,
    },
)

InputConfigurationRequestTypeDef = TypedDict(
    "InputConfigurationRequestTypeDef",
    {
        "InputPort": int,
        "Interface": InterfaceRequestTypeDef,
    },
)

DestinationConfigurationTypeDef = TypedDict(
    "DestinationConfigurationTypeDef",
    {
        "DestinationIp": str,
        "DestinationPort": int,
        "Interface": InterfaceTypeDef,
        "OutboundIp": str,
    },
)

InputConfigurationTypeDef = TypedDict(
    "InputConfigurationTypeDef",
    {
        "InputIp": str,
        "InputPort": int,
        "Interface": InterfaceTypeDef,
    },
)

FailoverConfigTypeDef = TypedDict(
    "FailoverConfigTypeDef",
    {
        "FailoverMode": FailoverModeType,
        "RecoveryWindow": int,
        "SourcePriority": SourcePriorityTypeDef,
        "State": StateType,
    },
    total=False,
)

UpdateFailoverConfigTypeDef = TypedDict(
    "UpdateFailoverConfigTypeDef",
    {
        "FailoverMode": FailoverModeType,
        "RecoveryWindow": int,
        "SourcePriority": SourcePriorityTypeDef,
        "State": StateType,
    },
    total=False,
)

_RequiredListedFlowTypeDef = TypedDict(
    "_RequiredListedFlowTypeDef",
    {
        "AvailabilityZone": str,
        "Description": str,
        "FlowArn": str,
        "Name": str,
        "SourceType": SourceTypeType,
        "Status": StatusType,
    },
)
_OptionalListedFlowTypeDef = TypedDict(
    "_OptionalListedFlowTypeDef",
    {
        "Maintenance": MaintenanceTypeDef,
    },
    total=False,
)


class ListedFlowTypeDef(_RequiredListedFlowTypeDef, _OptionalListedFlowTypeDef):
    pass


MediaStreamAttributesRequestTypeDef = TypedDict(
    "MediaStreamAttributesRequestTypeDef",
    {
        "Fmtp": FmtpRequestTypeDef,
        "Lang": str,
    },
    total=False,
)

_RequiredMediaStreamAttributesTypeDef = TypedDict(
    "_RequiredMediaStreamAttributesTypeDef",
    {
        "Fmtp": FmtpTypeDef,
    },
)
_OptionalMediaStreamAttributesTypeDef = TypedDict(
    "_OptionalMediaStreamAttributesTypeDef",
    {
        "Lang": str,
    },
    total=False,
)


class MediaStreamAttributesTypeDef(
    _RequiredMediaStreamAttributesTypeDef, _OptionalMediaStreamAttributesTypeDef
):
    pass


ListBridgesResponseTypeDef = TypedDict(
    "ListBridgesResponseTypeDef",
    {
        "Bridges": List[ListedBridgeTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListEntitlementsResponseTypeDef = TypedDict(
    "ListEntitlementsResponseTypeDef",
    {
        "Entitlements": List[ListedEntitlementTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListGatewayInstancesResponseTypeDef = TypedDict(
    "ListGatewayInstancesResponseTypeDef",
    {
        "Instances": List[ListedGatewayInstanceTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListGatewaysResponseTypeDef = TypedDict(
    "ListGatewaysResponseTypeDef",
    {
        "Gateways": List[ListedGatewayTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

OfferingTypeDef = TypedDict(
    "OfferingTypeDef",
    {
        "CurrencyCode": str,
        "Duration": int,
        "DurationUnits": Literal["MONTHS"],
        "OfferingArn": str,
        "OfferingDescription": str,
        "PricePerUnit": str,
        "PriceUnits": Literal["HOURLY"],
        "ResourceSpecification": ResourceSpecificationTypeDef,
    },
)

ReservationTypeDef = TypedDict(
    "ReservationTypeDef",
    {
        "CurrencyCode": str,
        "Duration": int,
        "DurationUnits": Literal["MONTHS"],
        "End": str,
        "OfferingArn": str,
        "OfferingDescription": str,
        "PricePerUnit": str,
        "PriceUnits": Literal["HOURLY"],
        "ReservationArn": str,
        "ReservationName": str,
        "ReservationState": ReservationStateType,
        "ResourceSpecification": ResourceSpecificationTypeDef,
        "Start": str,
    },
)

_RequiredUpdateBridgeOutputRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateBridgeOutputRequestRequestTypeDef",
    {
        "BridgeArn": str,
        "OutputName": str,
    },
)
_OptionalUpdateBridgeOutputRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateBridgeOutputRequestRequestTypeDef",
    {
        "NetworkOutput": UpdateBridgeNetworkOutputRequestTypeDef,
    },
    total=False,
)


class UpdateBridgeOutputRequestRequestTypeDef(
    _RequiredUpdateBridgeOutputRequestRequestTypeDef,
    _OptionalUpdateBridgeOutputRequestRequestTypeDef,
):
    pass


_RequiredUpdateFlowEntitlementRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateFlowEntitlementRequestRequestTypeDef",
    {
        "EntitlementArn": str,
        "FlowArn": str,
    },
)
_OptionalUpdateFlowEntitlementRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateFlowEntitlementRequestRequestTypeDef",
    {
        "Description": str,
        "Encryption": UpdateEncryptionTypeDef,
        "EntitlementStatus": EntitlementStatusType,
        "Subscribers": Sequence[str],
    },
    total=False,
)


class UpdateFlowEntitlementRequestRequestTypeDef(
    _RequiredUpdateFlowEntitlementRequestRequestTypeDef,
    _OptionalUpdateFlowEntitlementRequestRequestTypeDef,
):
    pass


AddBridgeSourceRequestTypeDef = TypedDict(
    "AddBridgeSourceRequestTypeDef",
    {
        "FlowSource": AddBridgeFlowSourceRequestTypeDef,
        "NetworkSource": AddBridgeNetworkSourceRequestTypeDef,
    },
    total=False,
)

BridgeSourceTypeDef = TypedDict(
    "BridgeSourceTypeDef",
    {
        "FlowSource": BridgeFlowSourceTypeDef,
        "NetworkSource": BridgeNetworkSourceTypeDef,
    },
    total=False,
)

_RequiredUpdateBridgeSourceRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateBridgeSourceRequestRequestTypeDef",
    {
        "BridgeArn": str,
        "SourceName": str,
    },
)
_OptionalUpdateBridgeSourceRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateBridgeSourceRequestRequestTypeDef",
    {
        "FlowSource": UpdateBridgeFlowSourceRequestTypeDef,
        "NetworkSource": UpdateBridgeNetworkSourceRequestTypeDef,
    },
    total=False,
)


class UpdateBridgeSourceRequestRequestTypeDef(
    _RequiredUpdateBridgeSourceRequestRequestTypeDef,
    _OptionalUpdateBridgeSourceRequestRequestTypeDef,
):
    pass


AddBridgeOutputsRequestRequestTypeDef = TypedDict(
    "AddBridgeOutputsRequestRequestTypeDef",
    {
        "BridgeArn": str,
        "Outputs": Sequence[AddBridgeOutputRequestTypeDef],
    },
)

GrantFlowEntitlementsResponseTypeDef = TypedDict(
    "GrantFlowEntitlementsResponseTypeDef",
    {
        "Entitlements": List[EntitlementTypeDef],
        "FlowArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateFlowEntitlementResponseTypeDef = TypedDict(
    "UpdateFlowEntitlementResponseTypeDef",
    {
        "Entitlement": EntitlementTypeDef,
        "FlowArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GrantFlowEntitlementsRequestRequestTypeDef = TypedDict(
    "GrantFlowEntitlementsRequestRequestTypeDef",
    {
        "Entitlements": Sequence[GrantEntitlementRequestTypeDef],
        "FlowArn": str,
    },
)

AddBridgeOutputsResponseTypeDef = TypedDict(
    "AddBridgeOutputsResponseTypeDef",
    {
        "BridgeArn": str,
        "Outputs": List[BridgeOutputTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateBridgeOutputResponseTypeDef = TypedDict(
    "UpdateBridgeOutputResponseTypeDef",
    {
        "BridgeArn": str,
        "Output": BridgeOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeGatewayInstanceResponseTypeDef = TypedDict(
    "DescribeGatewayInstanceResponseTypeDef",
    {
        "GatewayInstance": GatewayInstanceTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateGatewayResponseTypeDef = TypedDict(
    "CreateGatewayResponseTypeDef",
    {
        "Gateway": GatewayTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeGatewayResponseTypeDef = TypedDict(
    "DescribeGatewayResponseTypeDef",
    {
        "Gateway": GatewayTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredMediaStreamOutputConfigurationRequestTypeDef = TypedDict(
    "_RequiredMediaStreamOutputConfigurationRequestTypeDef",
    {
        "EncodingName": EncodingNameType,
        "MediaStreamName": str,
    },
)
_OptionalMediaStreamOutputConfigurationRequestTypeDef = TypedDict(
    "_OptionalMediaStreamOutputConfigurationRequestTypeDef",
    {
        "DestinationConfigurations": Sequence[DestinationConfigurationRequestTypeDef],
        "EncodingParameters": EncodingParametersRequestTypeDef,
    },
    total=False,
)


class MediaStreamOutputConfigurationRequestTypeDef(
    _RequiredMediaStreamOutputConfigurationRequestTypeDef,
    _OptionalMediaStreamOutputConfigurationRequestTypeDef,
):
    pass


_RequiredMediaStreamSourceConfigurationRequestTypeDef = TypedDict(
    "_RequiredMediaStreamSourceConfigurationRequestTypeDef",
    {
        "EncodingName": EncodingNameType,
        "MediaStreamName": str,
    },
)
_OptionalMediaStreamSourceConfigurationRequestTypeDef = TypedDict(
    "_OptionalMediaStreamSourceConfigurationRequestTypeDef",
    {
        "InputConfigurations": Sequence[InputConfigurationRequestTypeDef],
    },
    total=False,
)


class MediaStreamSourceConfigurationRequestTypeDef(
    _RequiredMediaStreamSourceConfigurationRequestTypeDef,
    _OptionalMediaStreamSourceConfigurationRequestTypeDef,
):
    pass


_RequiredMediaStreamOutputConfigurationTypeDef = TypedDict(
    "_RequiredMediaStreamOutputConfigurationTypeDef",
    {
        "EncodingName": EncodingNameType,
        "MediaStreamName": str,
    },
)
_OptionalMediaStreamOutputConfigurationTypeDef = TypedDict(
    "_OptionalMediaStreamOutputConfigurationTypeDef",
    {
        "DestinationConfigurations": List[DestinationConfigurationTypeDef],
        "EncodingParameters": EncodingParametersTypeDef,
    },
    total=False,
)


class MediaStreamOutputConfigurationTypeDef(
    _RequiredMediaStreamOutputConfigurationTypeDef, _OptionalMediaStreamOutputConfigurationTypeDef
):
    pass


_RequiredMediaStreamSourceConfigurationTypeDef = TypedDict(
    "_RequiredMediaStreamSourceConfigurationTypeDef",
    {
        "EncodingName": EncodingNameType,
        "MediaStreamName": str,
    },
)
_OptionalMediaStreamSourceConfigurationTypeDef = TypedDict(
    "_OptionalMediaStreamSourceConfigurationTypeDef",
    {
        "InputConfigurations": List[InputConfigurationTypeDef],
    },
    total=False,
)


class MediaStreamSourceConfigurationTypeDef(
    _RequiredMediaStreamSourceConfigurationTypeDef, _OptionalMediaStreamSourceConfigurationTypeDef
):
    pass


_RequiredUpdateBridgeRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateBridgeRequestRequestTypeDef",
    {
        "BridgeArn": str,
    },
)
_OptionalUpdateBridgeRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateBridgeRequestRequestTypeDef",
    {
        "EgressGatewayBridge": UpdateEgressGatewayBridgeRequestTypeDef,
        "IngressGatewayBridge": UpdateIngressGatewayBridgeRequestTypeDef,
        "SourceFailoverConfig": UpdateFailoverConfigTypeDef,
    },
    total=False,
)


class UpdateBridgeRequestRequestTypeDef(
    _RequiredUpdateBridgeRequestRequestTypeDef, _OptionalUpdateBridgeRequestRequestTypeDef
):
    pass


_RequiredUpdateFlowRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateFlowRequestRequestTypeDef",
    {
        "FlowArn": str,
    },
)
_OptionalUpdateFlowRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateFlowRequestRequestTypeDef",
    {
        "SourceFailoverConfig": UpdateFailoverConfigTypeDef,
        "Maintenance": UpdateMaintenanceTypeDef,
    },
    total=False,
)


class UpdateFlowRequestRequestTypeDef(
    _RequiredUpdateFlowRequestRequestTypeDef, _OptionalUpdateFlowRequestRequestTypeDef
):
    pass


ListFlowsResponseTypeDef = TypedDict(
    "ListFlowsResponseTypeDef",
    {
        "Flows": List[ListedFlowTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredAddMediaStreamRequestTypeDef = TypedDict(
    "_RequiredAddMediaStreamRequestTypeDef",
    {
        "MediaStreamId": int,
        "MediaStreamName": str,
        "MediaStreamType": MediaStreamTypeType,
    },
)
_OptionalAddMediaStreamRequestTypeDef = TypedDict(
    "_OptionalAddMediaStreamRequestTypeDef",
    {
        "Attributes": MediaStreamAttributesRequestTypeDef,
        "ClockRate": int,
        "Description": str,
        "VideoFormat": str,
    },
    total=False,
)


class AddMediaStreamRequestTypeDef(
    _RequiredAddMediaStreamRequestTypeDef, _OptionalAddMediaStreamRequestTypeDef
):
    pass


_RequiredUpdateFlowMediaStreamRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateFlowMediaStreamRequestRequestTypeDef",
    {
        "FlowArn": str,
        "MediaStreamName": str,
    },
)
_OptionalUpdateFlowMediaStreamRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateFlowMediaStreamRequestRequestTypeDef",
    {
        "Attributes": MediaStreamAttributesRequestTypeDef,
        "ClockRate": int,
        "Description": str,
        "MediaStreamType": MediaStreamTypeType,
        "VideoFormat": str,
    },
    total=False,
)


class UpdateFlowMediaStreamRequestRequestTypeDef(
    _RequiredUpdateFlowMediaStreamRequestRequestTypeDef,
    _OptionalUpdateFlowMediaStreamRequestRequestTypeDef,
):
    pass


_RequiredMediaStreamTypeDef = TypedDict(
    "_RequiredMediaStreamTypeDef",
    {
        "Fmt": int,
        "MediaStreamId": int,
        "MediaStreamName": str,
        "MediaStreamType": MediaStreamTypeType,
    },
)
_OptionalMediaStreamTypeDef = TypedDict(
    "_OptionalMediaStreamTypeDef",
    {
        "Attributes": MediaStreamAttributesTypeDef,
        "ClockRate": int,
        "Description": str,
        "VideoFormat": str,
    },
    total=False,
)


class MediaStreamTypeDef(_RequiredMediaStreamTypeDef, _OptionalMediaStreamTypeDef):
    pass


DescribeOfferingResponseTypeDef = TypedDict(
    "DescribeOfferingResponseTypeDef",
    {
        "Offering": OfferingTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListOfferingsResponseTypeDef = TypedDict(
    "ListOfferingsResponseTypeDef",
    {
        "NextToken": str,
        "Offerings": List[OfferingTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeReservationResponseTypeDef = TypedDict(
    "DescribeReservationResponseTypeDef",
    {
        "Reservation": ReservationTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListReservationsResponseTypeDef = TypedDict(
    "ListReservationsResponseTypeDef",
    {
        "NextToken": str,
        "Reservations": List[ReservationTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

PurchaseOfferingResponseTypeDef = TypedDict(
    "PurchaseOfferingResponseTypeDef",
    {
        "Reservation": ReservationTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

AddBridgeSourcesRequestRequestTypeDef = TypedDict(
    "AddBridgeSourcesRequestRequestTypeDef",
    {
        "BridgeArn": str,
        "Sources": Sequence[AddBridgeSourceRequestTypeDef],
    },
)

_RequiredCreateBridgeRequestRequestTypeDef = TypedDict(
    "_RequiredCreateBridgeRequestRequestTypeDef",
    {
        "Name": str,
        "PlacementArn": str,
        "Sources": Sequence[AddBridgeSourceRequestTypeDef],
    },
)
_OptionalCreateBridgeRequestRequestTypeDef = TypedDict(
    "_OptionalCreateBridgeRequestRequestTypeDef",
    {
        "EgressGatewayBridge": AddEgressGatewayBridgeRequestTypeDef,
        "IngressGatewayBridge": AddIngressGatewayBridgeRequestTypeDef,
        "Outputs": Sequence[AddBridgeOutputRequestTypeDef],
        "SourceFailoverConfig": FailoverConfigTypeDef,
    },
    total=False,
)


class CreateBridgeRequestRequestTypeDef(
    _RequiredCreateBridgeRequestRequestTypeDef, _OptionalCreateBridgeRequestRequestTypeDef
):
    pass


AddBridgeSourcesResponseTypeDef = TypedDict(
    "AddBridgeSourcesResponseTypeDef",
    {
        "BridgeArn": str,
        "Sources": List[BridgeSourceTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredBridgeTypeDef = TypedDict(
    "_RequiredBridgeTypeDef",
    {
        "BridgeArn": str,
        "BridgeState": BridgeStateType,
        "Name": str,
        "PlacementArn": str,
    },
)
_OptionalBridgeTypeDef = TypedDict(
    "_OptionalBridgeTypeDef",
    {
        "BridgeMessages": List[MessageDetailTypeDef],
        "EgressGatewayBridge": EgressGatewayBridgeTypeDef,
        "IngressGatewayBridge": IngressGatewayBridgeTypeDef,
        "Outputs": List[BridgeOutputTypeDef],
        "SourceFailoverConfig": FailoverConfigTypeDef,
        "Sources": List[BridgeSourceTypeDef],
    },
    total=False,
)


class BridgeTypeDef(_RequiredBridgeTypeDef, _OptionalBridgeTypeDef):
    pass


UpdateBridgeSourceResponseTypeDef = TypedDict(
    "UpdateBridgeSourceResponseTypeDef",
    {
        "BridgeArn": str,
        "Source": BridgeSourceTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredAddOutputRequestTypeDef = TypedDict(
    "_RequiredAddOutputRequestTypeDef",
    {
        "Protocol": ProtocolType,
    },
)
_OptionalAddOutputRequestTypeDef = TypedDict(
    "_OptionalAddOutputRequestTypeDef",
    {
        "CidrAllowList": Sequence[str],
        "Description": str,
        "Destination": str,
        "Encryption": EncryptionTypeDef,
        "MaxLatency": int,
        "MediaStreamOutputConfigurations": Sequence[MediaStreamOutputConfigurationRequestTypeDef],
        "MinLatency": int,
        "Name": str,
        "Port": int,
        "RemoteId": str,
        "SenderControlPort": int,
        "SmoothingLatency": int,
        "StreamId": str,
        "VpcInterfaceAttachment": VpcInterfaceAttachmentTypeDef,
    },
    total=False,
)


class AddOutputRequestTypeDef(_RequiredAddOutputRequestTypeDef, _OptionalAddOutputRequestTypeDef):
    pass


_RequiredUpdateFlowOutputRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateFlowOutputRequestRequestTypeDef",
    {
        "FlowArn": str,
        "OutputArn": str,
    },
)
_OptionalUpdateFlowOutputRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateFlowOutputRequestRequestTypeDef",
    {
        "CidrAllowList": Sequence[str],
        "Description": str,
        "Destination": str,
        "Encryption": UpdateEncryptionTypeDef,
        "MaxLatency": int,
        "MediaStreamOutputConfigurations": Sequence[MediaStreamOutputConfigurationRequestTypeDef],
        "MinLatency": int,
        "Port": int,
        "Protocol": ProtocolType,
        "RemoteId": str,
        "SenderControlPort": int,
        "SenderIpAddress": str,
        "SmoothingLatency": int,
        "StreamId": str,
        "VpcInterfaceAttachment": VpcInterfaceAttachmentTypeDef,
    },
    total=False,
)


class UpdateFlowOutputRequestRequestTypeDef(
    _RequiredUpdateFlowOutputRequestRequestTypeDef, _OptionalUpdateFlowOutputRequestRequestTypeDef
):
    pass


SetSourceRequestTypeDef = TypedDict(
    "SetSourceRequestTypeDef",
    {
        "Decryption": EncryptionTypeDef,
        "Description": str,
        "EntitlementArn": str,
        "IngestPort": int,
        "MaxBitrate": int,
        "MaxLatency": int,
        "MaxSyncBuffer": int,
        "MediaStreamSourceConfigurations": Sequence[MediaStreamSourceConfigurationRequestTypeDef],
        "MinLatency": int,
        "Name": str,
        "Protocol": ProtocolType,
        "SenderControlPort": int,
        "SenderIpAddress": str,
        "SourceListenerAddress": str,
        "SourceListenerPort": int,
        "StreamId": str,
        "VpcInterfaceName": str,
        "WhitelistCidr": str,
        "GatewayBridgeSource": SetGatewayBridgeSourceRequestTypeDef,
    },
    total=False,
)

_RequiredUpdateFlowSourceRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateFlowSourceRequestRequestTypeDef",
    {
        "FlowArn": str,
        "SourceArn": str,
    },
)
_OptionalUpdateFlowSourceRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateFlowSourceRequestRequestTypeDef",
    {
        "Decryption": UpdateEncryptionTypeDef,
        "Description": str,
        "EntitlementArn": str,
        "IngestPort": int,
        "MaxBitrate": int,
        "MaxLatency": int,
        "MaxSyncBuffer": int,
        "MediaStreamSourceConfigurations": Sequence[MediaStreamSourceConfigurationRequestTypeDef],
        "MinLatency": int,
        "Protocol": ProtocolType,
        "SenderControlPort": int,
        "SenderIpAddress": str,
        "SourceListenerAddress": str,
        "SourceListenerPort": int,
        "StreamId": str,
        "VpcInterfaceName": str,
        "WhitelistCidr": str,
        "GatewayBridgeSource": UpdateGatewayBridgeSourceRequestTypeDef,
    },
    total=False,
)


class UpdateFlowSourceRequestRequestTypeDef(
    _RequiredUpdateFlowSourceRequestRequestTypeDef, _OptionalUpdateFlowSourceRequestRequestTypeDef
):
    pass


_RequiredOutputTypeDef = TypedDict(
    "_RequiredOutputTypeDef",
    {
        "Name": str,
        "OutputArn": str,
    },
)
_OptionalOutputTypeDef = TypedDict(
    "_OptionalOutputTypeDef",
    {
        "DataTransferSubscriberFeePercent": int,
        "Description": str,
        "Destination": str,
        "Encryption": EncryptionTypeDef,
        "EntitlementArn": str,
        "ListenerAddress": str,
        "MediaLiveInputArn": str,
        "MediaStreamOutputConfigurations": List[MediaStreamOutputConfigurationTypeDef],
        "Port": int,
        "Transport": TransportTypeDef,
        "VpcInterfaceAttachment": VpcInterfaceAttachmentTypeDef,
        "BridgeArn": str,
        "BridgePorts": List[int],
    },
    total=False,
)


class OutputTypeDef(_RequiredOutputTypeDef, _OptionalOutputTypeDef):
    pass


_RequiredSourceTypeDef = TypedDict(
    "_RequiredSourceTypeDef",
    {
        "Name": str,
        "SourceArn": str,
    },
)
_OptionalSourceTypeDef = TypedDict(
    "_OptionalSourceTypeDef",
    {
        "DataTransferSubscriberFeePercent": int,
        "Decryption": EncryptionTypeDef,
        "Description": str,
        "EntitlementArn": str,
        "IngestIp": str,
        "IngestPort": int,
        "MediaStreamSourceConfigurations": List[MediaStreamSourceConfigurationTypeDef],
        "SenderControlPort": int,
        "SenderIpAddress": str,
        "Transport": TransportTypeDef,
        "VpcInterfaceName": str,
        "WhitelistCidr": str,
        "GatewayBridgeSource": GatewayBridgeSourceTypeDef,
    },
    total=False,
)


class SourceTypeDef(_RequiredSourceTypeDef, _OptionalSourceTypeDef):
    pass


AddFlowMediaStreamsRequestRequestTypeDef = TypedDict(
    "AddFlowMediaStreamsRequestRequestTypeDef",
    {
        "FlowArn": str,
        "MediaStreams": Sequence[AddMediaStreamRequestTypeDef],
    },
)

AddFlowMediaStreamsResponseTypeDef = TypedDict(
    "AddFlowMediaStreamsResponseTypeDef",
    {
        "FlowArn": str,
        "MediaStreams": List[MediaStreamTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateFlowMediaStreamResponseTypeDef = TypedDict(
    "UpdateFlowMediaStreamResponseTypeDef",
    {
        "FlowArn": str,
        "MediaStream": MediaStreamTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateBridgeResponseTypeDef = TypedDict(
    "CreateBridgeResponseTypeDef",
    {
        "Bridge": BridgeTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeBridgeResponseTypeDef = TypedDict(
    "DescribeBridgeResponseTypeDef",
    {
        "Bridge": BridgeTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateBridgeResponseTypeDef = TypedDict(
    "UpdateBridgeResponseTypeDef",
    {
        "Bridge": BridgeTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

AddFlowOutputsRequestRequestTypeDef = TypedDict(
    "AddFlowOutputsRequestRequestTypeDef",
    {
        "FlowArn": str,
        "Outputs": Sequence[AddOutputRequestTypeDef],
    },
)

AddFlowSourcesRequestRequestTypeDef = TypedDict(
    "AddFlowSourcesRequestRequestTypeDef",
    {
        "FlowArn": str,
        "Sources": Sequence[SetSourceRequestTypeDef],
    },
)

_RequiredCreateFlowRequestRequestTypeDef = TypedDict(
    "_RequiredCreateFlowRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalCreateFlowRequestRequestTypeDef = TypedDict(
    "_OptionalCreateFlowRequestRequestTypeDef",
    {
        "AvailabilityZone": str,
        "Entitlements": Sequence[GrantEntitlementRequestTypeDef],
        "MediaStreams": Sequence[AddMediaStreamRequestTypeDef],
        "Outputs": Sequence[AddOutputRequestTypeDef],
        "Source": SetSourceRequestTypeDef,
        "SourceFailoverConfig": FailoverConfigTypeDef,
        "Sources": Sequence[SetSourceRequestTypeDef],
        "VpcInterfaces": Sequence[VpcInterfaceRequestTypeDef],
        "Maintenance": AddMaintenanceTypeDef,
    },
    total=False,
)


class CreateFlowRequestRequestTypeDef(
    _RequiredCreateFlowRequestRequestTypeDef, _OptionalCreateFlowRequestRequestTypeDef
):
    pass


AddFlowOutputsResponseTypeDef = TypedDict(
    "AddFlowOutputsResponseTypeDef",
    {
        "FlowArn": str,
        "Outputs": List[OutputTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateFlowOutputResponseTypeDef = TypedDict(
    "UpdateFlowOutputResponseTypeDef",
    {
        "FlowArn": str,
        "Output": OutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

AddFlowSourcesResponseTypeDef = TypedDict(
    "AddFlowSourcesResponseTypeDef",
    {
        "FlowArn": str,
        "Sources": List[SourceTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredFlowTypeDef = TypedDict(
    "_RequiredFlowTypeDef",
    {
        "AvailabilityZone": str,
        "Entitlements": List[EntitlementTypeDef],
        "FlowArn": str,
        "Name": str,
        "Outputs": List[OutputTypeDef],
        "Source": SourceTypeDef,
        "Status": StatusType,
    },
)
_OptionalFlowTypeDef = TypedDict(
    "_OptionalFlowTypeDef",
    {
        "Description": str,
        "EgressIp": str,
        "MediaStreams": List[MediaStreamTypeDef],
        "SourceFailoverConfig": FailoverConfigTypeDef,
        "Sources": List[SourceTypeDef],
        "VpcInterfaces": List[VpcInterfaceTypeDef],
        "Maintenance": MaintenanceTypeDef,
    },
    total=False,
)


class FlowTypeDef(_RequiredFlowTypeDef, _OptionalFlowTypeDef):
    pass


UpdateFlowSourceResponseTypeDef = TypedDict(
    "UpdateFlowSourceResponseTypeDef",
    {
        "FlowArn": str,
        "Source": SourceTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateFlowResponseTypeDef = TypedDict(
    "CreateFlowResponseTypeDef",
    {
        "Flow": FlowTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeFlowResponseTypeDef = TypedDict(
    "DescribeFlowResponseTypeDef",
    {
        "Flow": FlowTypeDef,
        "Messages": MessagesTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateFlowResponseTypeDef = TypedDict(
    "UpdateFlowResponseTypeDef",
    {
        "Flow": FlowTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)
