# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from ._enums import *

__all__ = [
    'DevicePoolRule',
    'DevicePoolTag',
    'InstanceProfileTag',
    'NetworkProfileTag',
    'ProjectTag',
    'ProjectVpcConfig',
    'TestGridProjectTag',
    'TestGridProjectVpcConfig',
    'VPCEConfigurationTag',
]

@pulumi.output_type
class DevicePoolRule(dict):
    """
    Represents a condition for a device pool.
    """
    def __init__(__self__, *,
                 attribute: Optional['DevicePoolRuleAttribute'] = None,
                 operator: Optional['DevicePoolRuleOperator'] = None,
                 value: Optional[str] = None):
        """
        Represents a condition for a device pool.
        :param 'DevicePoolRuleAttribute' attribute: The rule's stringified attribute.
        :param 'DevicePoolRuleOperator' operator: Specifies how Device Farm compares the rule's attribute to the value.
        :param str value: The rule's value.
        """
        if attribute is not None:
            pulumi.set(__self__, "attribute", attribute)
        if operator is not None:
            pulumi.set(__self__, "operator", operator)
        if value is not None:
            pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def attribute(self) -> Optional['DevicePoolRuleAttribute']:
        """
        The rule's stringified attribute.
        """
        return pulumi.get(self, "attribute")

    @property
    @pulumi.getter
    def operator(self) -> Optional['DevicePoolRuleOperator']:
        """
        Specifies how Device Farm compares the rule's attribute to the value.
        """
        return pulumi.get(self, "operator")

    @property
    @pulumi.getter
    def value(self) -> Optional[str]:
        """
        The rule's value.
        """
        return pulumi.get(self, "value")


@pulumi.output_type
class DevicePoolTag(dict):
    def __init__(__self__, *,
                 key: str,
                 value: str):
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> str:
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def value(self) -> str:
        return pulumi.get(self, "value")


@pulumi.output_type
class InstanceProfileTag(dict):
    def __init__(__self__, *,
                 key: str,
                 value: str):
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> str:
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def value(self) -> str:
        return pulumi.get(self, "value")


@pulumi.output_type
class NetworkProfileTag(dict):
    def __init__(__self__, *,
                 key: str,
                 value: str):
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> str:
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def value(self) -> str:
        return pulumi.get(self, "value")


@pulumi.output_type
class ProjectTag(dict):
    def __init__(__self__, *,
                 key: str,
                 value: str):
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> str:
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def value(self) -> str:
        return pulumi.get(self, "value")


@pulumi.output_type
class ProjectVpcConfig(dict):
    """
    The VPC security groups and subnets that are attached to a project
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "securityGroupIds":
            suggest = "security_group_ids"
        elif key == "subnetIds":
            suggest = "subnet_ids"
        elif key == "vpcId":
            suggest = "vpc_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ProjectVpcConfig. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ProjectVpcConfig.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ProjectVpcConfig.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 security_group_ids: Sequence[str],
                 subnet_ids: Sequence[str],
                 vpc_id: str):
        """
        The VPC security groups and subnets that are attached to a project
        :param Sequence[str] security_group_ids: An array of security group Ids in your Amazon VPC
        :param Sequence[str] subnet_ids: A array of subnet IDs in your Amazon VPC.
        :param str vpc_id: The ID of the Amazon VPC
        """
        pulumi.set(__self__, "security_group_ids", security_group_ids)
        pulumi.set(__self__, "subnet_ids", subnet_ids)
        pulumi.set(__self__, "vpc_id", vpc_id)

    @property
    @pulumi.getter(name="securityGroupIds")
    def security_group_ids(self) -> Sequence[str]:
        """
        An array of security group Ids in your Amazon VPC
        """
        return pulumi.get(self, "security_group_ids")

    @property
    @pulumi.getter(name="subnetIds")
    def subnet_ids(self) -> Sequence[str]:
        """
        A array of subnet IDs in your Amazon VPC.
        """
        return pulumi.get(self, "subnet_ids")

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> str:
        """
        The ID of the Amazon VPC
        """
        return pulumi.get(self, "vpc_id")


@pulumi.output_type
class TestGridProjectTag(dict):
    def __init__(__self__, *,
                 key: str,
                 value: str):
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> str:
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def value(self) -> str:
        return pulumi.get(self, "value")


@pulumi.output_type
class TestGridProjectVpcConfig(dict):
    """
    The VPC security groups and subnets that are attached to a TestGrid project.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "securityGroupIds":
            suggest = "security_group_ids"
        elif key == "subnetIds":
            suggest = "subnet_ids"
        elif key == "vpcId":
            suggest = "vpc_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in TestGridProjectVpcConfig. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        TestGridProjectVpcConfig.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        TestGridProjectVpcConfig.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 security_group_ids: Sequence[str],
                 subnet_ids: Sequence[str],
                 vpc_id: str):
        """
        The VPC security groups and subnets that are attached to a TestGrid project.
        :param Sequence[str] security_group_ids: A list of VPC security group IDs in your Amazon VPC.
        :param Sequence[str] subnet_ids: A list of VPC subnet IDs in your Amazon VPC.
        """
        pulumi.set(__self__, "security_group_ids", security_group_ids)
        pulumi.set(__self__, "subnet_ids", subnet_ids)
        pulumi.set(__self__, "vpc_id", vpc_id)

    @property
    @pulumi.getter(name="securityGroupIds")
    def security_group_ids(self) -> Sequence[str]:
        """
        A list of VPC security group IDs in your Amazon VPC.
        """
        return pulumi.get(self, "security_group_ids")

    @property
    @pulumi.getter(name="subnetIds")
    def subnet_ids(self) -> Sequence[str]:
        """
        A list of VPC subnet IDs in your Amazon VPC.
        """
        return pulumi.get(self, "subnet_ids")

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> str:
        return pulumi.get(self, "vpc_id")


@pulumi.output_type
class VPCEConfigurationTag(dict):
    def __init__(__self__, *,
                 key: str,
                 value: str):
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> str:
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def value(self) -> str:
        return pulumi.get(self, "value")


