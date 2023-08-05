# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs

__all__ = [
    'GetCarrierGatewayResult',
    'AwaitableGetCarrierGatewayResult',
    'get_carrier_gateway',
    'get_carrier_gateway_output',
]

@pulumi.output_type
class GetCarrierGatewayResult:
    def __init__(__self__, carrier_gateway_id=None, owner_id=None, state=None, tags=None):
        if carrier_gateway_id and not isinstance(carrier_gateway_id, str):
            raise TypeError("Expected argument 'carrier_gateway_id' to be a str")
        pulumi.set(__self__, "carrier_gateway_id", carrier_gateway_id)
        if owner_id and not isinstance(owner_id, str):
            raise TypeError("Expected argument 'owner_id' to be a str")
        pulumi.set(__self__, "owner_id", owner_id)
        if state and not isinstance(state, str):
            raise TypeError("Expected argument 'state' to be a str")
        pulumi.set(__self__, "state", state)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="carrierGatewayId")
    def carrier_gateway_id(self) -> Optional[str]:
        """
        The ID of the carrier gateway.
        """
        return pulumi.get(self, "carrier_gateway_id")

    @property
    @pulumi.getter(name="ownerId")
    def owner_id(self) -> Optional[str]:
        """
        The ID of the owner.
        """
        return pulumi.get(self, "owner_id")

    @property
    @pulumi.getter
    def state(self) -> Optional[str]:
        """
        The state of the carrier gateway.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['outputs.CarrierGatewayTag']]:
        """
        The tags for the carrier gateway.
        """
        return pulumi.get(self, "tags")


class AwaitableGetCarrierGatewayResult(GetCarrierGatewayResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetCarrierGatewayResult(
            carrier_gateway_id=self.carrier_gateway_id,
            owner_id=self.owner_id,
            state=self.state,
            tags=self.tags)


def get_carrier_gateway(carrier_gateway_id: Optional[str] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetCarrierGatewayResult:
    """
    An example resource schema demonstrating some basic constructs and validation rules.


    :param str carrier_gateway_id: The ID of the carrier gateway.
    """
    __args__ = dict()
    __args__['carrierGatewayId'] = carrier_gateway_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:ec2:getCarrierGateway', __args__, opts=opts, typ=GetCarrierGatewayResult).value

    return AwaitableGetCarrierGatewayResult(
        carrier_gateway_id=__ret__.carrier_gateway_id,
        owner_id=__ret__.owner_id,
        state=__ret__.state,
        tags=__ret__.tags)


@_utilities.lift_output_func(get_carrier_gateway)
def get_carrier_gateway_output(carrier_gateway_id: Optional[pulumi.Input[str]] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetCarrierGatewayResult]:
    """
    An example resource schema demonstrating some basic constructs and validation rules.


    :param str carrier_gateway_id: The ID of the carrier gateway.
    """
    ...
