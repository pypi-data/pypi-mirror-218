# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['ClusterPolicyArgs', 'ClusterPolicy']

@pulumi.input_type
class ClusterPolicyArgs:
    def __init__(__self__, *,
                 cluster_arn: pulumi.Input[str],
                 policy: Any):
        """
        The set of arguments for constructing a ClusterPolicy resource.
        :param pulumi.Input[str] cluster_arn: The arn of the cluster for the resource policy.
        :param Any policy: A policy document containing permissions to add to the specified cluster.
        """
        pulumi.set(__self__, "cluster_arn", cluster_arn)
        pulumi.set(__self__, "policy", policy)

    @property
    @pulumi.getter(name="clusterArn")
    def cluster_arn(self) -> pulumi.Input[str]:
        """
        The arn of the cluster for the resource policy.
        """
        return pulumi.get(self, "cluster_arn")

    @cluster_arn.setter
    def cluster_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "cluster_arn", value)

    @property
    @pulumi.getter
    def policy(self) -> Any:
        """
        A policy document containing permissions to add to the specified cluster.
        """
        return pulumi.get(self, "policy")

    @policy.setter
    def policy(self, value: Any):
        pulumi.set(self, "policy", value)


class ClusterPolicy(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cluster_arn: Optional[pulumi.Input[str]] = None,
                 policy: Optional[Any] = None,
                 __props__=None):
        """
        Resource Type definition for AWS::MSK::ClusterPolicy

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] cluster_arn: The arn of the cluster for the resource policy.
        :param Any policy: A policy document containing permissions to add to the specified cluster.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ClusterPolicyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource Type definition for AWS::MSK::ClusterPolicy

        :param str resource_name: The name of the resource.
        :param ClusterPolicyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ClusterPolicyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cluster_arn: Optional[pulumi.Input[str]] = None,
                 policy: Optional[Any] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ClusterPolicyArgs.__new__(ClusterPolicyArgs)

            if cluster_arn is None and not opts.urn:
                raise TypeError("Missing required property 'cluster_arn'")
            __props__.__dict__["cluster_arn"] = cluster_arn
            if policy is None and not opts.urn:
                raise TypeError("Missing required property 'policy'")
            __props__.__dict__["policy"] = policy
            __props__.__dict__["current_version"] = None
        super(ClusterPolicy, __self__).__init__(
            'aws-native:msk:ClusterPolicy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ClusterPolicy':
        """
        Get an existing ClusterPolicy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ClusterPolicyArgs.__new__(ClusterPolicyArgs)

        __props__.__dict__["cluster_arn"] = None
        __props__.__dict__["current_version"] = None
        __props__.__dict__["policy"] = None
        return ClusterPolicy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="clusterArn")
    def cluster_arn(self) -> pulumi.Output[str]:
        """
        The arn of the cluster for the resource policy.
        """
        return pulumi.get(self, "cluster_arn")

    @property
    @pulumi.getter(name="currentVersion")
    def current_version(self) -> pulumi.Output[str]:
        """
        The current version of the policy attached to the specified cluster
        """
        return pulumi.get(self, "current_version")

    @property
    @pulumi.getter
    def policy(self) -> pulumi.Output[Any]:
        """
        A policy document containing permissions to add to the specified cluster.
        """
        return pulumi.get(self, "policy")

