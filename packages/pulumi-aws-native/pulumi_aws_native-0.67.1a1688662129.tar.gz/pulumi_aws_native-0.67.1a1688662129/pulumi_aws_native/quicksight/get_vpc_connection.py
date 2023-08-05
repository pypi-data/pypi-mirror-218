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
from ._enums import *

__all__ = [
    'GetVPCConnectionResult',
    'AwaitableGetVPCConnectionResult',
    'get_vpc_connection',
    'get_vpc_connection_output',
]

@pulumi.output_type
class GetVPCConnectionResult:
    def __init__(__self__, arn=None, availability_status=None, created_time=None, dns_resolvers=None, last_updated_time=None, name=None, network_interfaces=None, role_arn=None, security_group_ids=None, status=None, tags=None, v_pc_id=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if availability_status and not isinstance(availability_status, str):
            raise TypeError("Expected argument 'availability_status' to be a str")
        pulumi.set(__self__, "availability_status", availability_status)
        if created_time and not isinstance(created_time, str):
            raise TypeError("Expected argument 'created_time' to be a str")
        pulumi.set(__self__, "created_time", created_time)
        if dns_resolvers and not isinstance(dns_resolvers, list):
            raise TypeError("Expected argument 'dns_resolvers' to be a list")
        pulumi.set(__self__, "dns_resolvers", dns_resolvers)
        if last_updated_time and not isinstance(last_updated_time, str):
            raise TypeError("Expected argument 'last_updated_time' to be a str")
        pulumi.set(__self__, "last_updated_time", last_updated_time)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if network_interfaces and not isinstance(network_interfaces, list):
            raise TypeError("Expected argument 'network_interfaces' to be a list")
        pulumi.set(__self__, "network_interfaces", network_interfaces)
        if role_arn and not isinstance(role_arn, str):
            raise TypeError("Expected argument 'role_arn' to be a str")
        pulumi.set(__self__, "role_arn", role_arn)
        if security_group_ids and not isinstance(security_group_ids, list):
            raise TypeError("Expected argument 'security_group_ids' to be a list")
        pulumi.set(__self__, "security_group_ids", security_group_ids)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)
        if v_pc_id and not isinstance(v_pc_id, str):
            raise TypeError("Expected argument 'v_pc_id' to be a str")
        pulumi.set(__self__, "v_pc_id", v_pc_id)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="availabilityStatus")
    def availability_status(self) -> Optional['VPCConnectionAvailabilityStatus']:
        return pulumi.get(self, "availability_status")

    @property
    @pulumi.getter(name="createdTime")
    def created_time(self) -> Optional[str]:
        return pulumi.get(self, "created_time")

    @property
    @pulumi.getter(name="dnsResolvers")
    def dns_resolvers(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "dns_resolvers")

    @property
    @pulumi.getter(name="lastUpdatedTime")
    def last_updated_time(self) -> Optional[str]:
        return pulumi.get(self, "last_updated_time")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="networkInterfaces")
    def network_interfaces(self) -> Optional[Sequence['outputs.VPCConnectionNetworkInterface']]:
        return pulumi.get(self, "network_interfaces")

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> Optional[str]:
        return pulumi.get(self, "role_arn")

    @property
    @pulumi.getter(name="securityGroupIds")
    def security_group_ids(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "security_group_ids")

    @property
    @pulumi.getter
    def status(self) -> Optional['VPCConnectionResourceStatus']:
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['outputs.VPCConnectionTag']]:
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="vPCId")
    def v_pc_id(self) -> Optional[str]:
        return pulumi.get(self, "v_pc_id")


class AwaitableGetVPCConnectionResult(GetVPCConnectionResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetVPCConnectionResult(
            arn=self.arn,
            availability_status=self.availability_status,
            created_time=self.created_time,
            dns_resolvers=self.dns_resolvers,
            last_updated_time=self.last_updated_time,
            name=self.name,
            network_interfaces=self.network_interfaces,
            role_arn=self.role_arn,
            security_group_ids=self.security_group_ids,
            status=self.status,
            tags=self.tags,
            v_pc_id=self.v_pc_id)


def get_vpc_connection(aws_account_id: Optional[str] = None,
                       v_pc_connection_id: Optional[str] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetVPCConnectionResult:
    """
    Definition of the AWS::QuickSight::VPCConnection Resource Type.
    """
    __args__ = dict()
    __args__['awsAccountId'] = aws_account_id
    __args__['vPCConnectionId'] = v_pc_connection_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:quicksight:getVPCConnection', __args__, opts=opts, typ=GetVPCConnectionResult).value

    return AwaitableGetVPCConnectionResult(
        arn=__ret__.arn,
        availability_status=__ret__.availability_status,
        created_time=__ret__.created_time,
        dns_resolvers=__ret__.dns_resolvers,
        last_updated_time=__ret__.last_updated_time,
        name=__ret__.name,
        network_interfaces=__ret__.network_interfaces,
        role_arn=__ret__.role_arn,
        security_group_ids=__ret__.security_group_ids,
        status=__ret__.status,
        tags=__ret__.tags,
        v_pc_id=__ret__.v_pc_id)


@_utilities.lift_output_func(get_vpc_connection)
def get_vpc_connection_output(aws_account_id: Optional[pulumi.Input[str]] = None,
                              v_pc_connection_id: Optional[pulumi.Input[str]] = None,
                              opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetVPCConnectionResult]:
    """
    Definition of the AWS::QuickSight::VPCConnection Resource Type.
    """
    ...
