# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'PipelineLogPublishingOptionsCloudWatchLogDestinationPropertiesArgs',
    'PipelineLogPublishingOptionsArgs',
    'PipelineTagArgs',
    'PipelineVpcOptionsArgs',
]

@pulumi.input_type
class PipelineLogPublishingOptionsCloudWatchLogDestinationPropertiesArgs:
    def __init__(__self__, *,
                 log_group: Optional[pulumi.Input[str]] = None):
        """
        The destination for OpenSearch Ingestion Service logs sent to Amazon CloudWatch.
        """
        if log_group is not None:
            pulumi.set(__self__, "log_group", log_group)

    @property
    @pulumi.getter(name="logGroup")
    def log_group(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "log_group")

    @log_group.setter
    def log_group(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "log_group", value)


@pulumi.input_type
class PipelineLogPublishingOptionsArgs:
    def __init__(__self__, *,
                 cloud_watch_log_destination: Optional[pulumi.Input['PipelineLogPublishingOptionsCloudWatchLogDestinationPropertiesArgs']] = None,
                 is_logging_enabled: Optional[pulumi.Input[bool]] = None):
        """
        Key-value pairs to configure log publishing.
        :param pulumi.Input['PipelineLogPublishingOptionsCloudWatchLogDestinationPropertiesArgs'] cloud_watch_log_destination: The destination for OpenSearch Ingestion Service logs sent to Amazon CloudWatch.
        :param pulumi.Input[bool] is_logging_enabled: Whether logs should be published.
        """
        if cloud_watch_log_destination is not None:
            pulumi.set(__self__, "cloud_watch_log_destination", cloud_watch_log_destination)
        if is_logging_enabled is not None:
            pulumi.set(__self__, "is_logging_enabled", is_logging_enabled)

    @property
    @pulumi.getter(name="cloudWatchLogDestination")
    def cloud_watch_log_destination(self) -> Optional[pulumi.Input['PipelineLogPublishingOptionsCloudWatchLogDestinationPropertiesArgs']]:
        """
        The destination for OpenSearch Ingestion Service logs sent to Amazon CloudWatch.
        """
        return pulumi.get(self, "cloud_watch_log_destination")

    @cloud_watch_log_destination.setter
    def cloud_watch_log_destination(self, value: Optional[pulumi.Input['PipelineLogPublishingOptionsCloudWatchLogDestinationPropertiesArgs']]):
        pulumi.set(self, "cloud_watch_log_destination", value)

    @property
    @pulumi.getter(name="isLoggingEnabled")
    def is_logging_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether logs should be published.
        """
        return pulumi.get(self, "is_logging_enabled")

    @is_logging_enabled.setter
    def is_logging_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "is_logging_enabled", value)


@pulumi.input_type
class PipelineTagArgs:
    def __init__(__self__, *,
                 key: pulumi.Input[str],
                 value: pulumi.Input[str]):
        """
        A key-value pair to associate with a resource.
        :param pulumi.Input[str] key: The key name of the tag. You can specify a value that is 1 to 128 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -.
        :param pulumi.Input[str] value: The value for the tag. You can specify a value that is 0 to 256 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -.
        """
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> pulumi.Input[str]:
        """
        The key name of the tag. You can specify a value that is 1 to 128 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -.
        """
        return pulumi.get(self, "key")

    @key.setter
    def key(self, value: pulumi.Input[str]):
        pulumi.set(self, "key", value)

    @property
    @pulumi.getter
    def value(self) -> pulumi.Input[str]:
        """
        The value for the tag. You can specify a value that is 0 to 256 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -.
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: pulumi.Input[str]):
        pulumi.set(self, "value", value)


@pulumi.input_type
class PipelineVpcOptionsArgs:
    def __init__(__self__, *,
                 security_group_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 subnet_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        Container for the values required to configure VPC access for the pipeline. If you don't specify these values, OpenSearch Ingestion Service creates the pipeline with a public endpoint.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] security_group_ids: A list of security groups associated with the VPC endpoint.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] subnet_ids: A list of subnet IDs associated with the VPC endpoint.
        """
        if security_group_ids is not None:
            pulumi.set(__self__, "security_group_ids", security_group_ids)
        if subnet_ids is not None:
            pulumi.set(__self__, "subnet_ids", subnet_ids)

    @property
    @pulumi.getter(name="securityGroupIds")
    def security_group_ids(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of security groups associated with the VPC endpoint.
        """
        return pulumi.get(self, "security_group_ids")

    @security_group_ids.setter
    def security_group_ids(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "security_group_ids", value)

    @property
    @pulumi.getter(name="subnetIds")
    def subnet_ids(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of subnet IDs associated with the VPC endpoint.
        """
        return pulumi.get(self, "subnet_ids")

    @subnet_ids.setter
    def subnet_ids(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "subnet_ids", value)


