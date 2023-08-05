# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['OrganizationAdminArgs', 'OrganizationAdmin']

@pulumi.input_type
class OrganizationAdminArgs:
    def __init__(__self__, *,
                 account_id: pulumi.Input[str]):
        """
        The set of arguments for constructing a OrganizationAdmin resource.
        :param pulumi.Input[str] account_id: The account ID of the account that should be registered as your Organization's delegated administrator for Detective
        """
        pulumi.set(__self__, "account_id", account_id)

    @property
    @pulumi.getter(name="accountId")
    def account_id(self) -> pulumi.Input[str]:
        """
        The account ID of the account that should be registered as your Organization's delegated administrator for Detective
        """
        return pulumi.get(self, "account_id")

    @account_id.setter
    def account_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "account_id", value)


class OrganizationAdmin(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Resource schema for AWS::Detective::OrganizationAdmin

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_id: The account ID of the account that should be registered as your Organization's delegated administrator for Detective
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: OrganizationAdminArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource schema for AWS::Detective::OrganizationAdmin

        :param str resource_name: The name of the resource.
        :param OrganizationAdminArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(OrganizationAdminArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = OrganizationAdminArgs.__new__(OrganizationAdminArgs)

            if account_id is None and not opts.urn:
                raise TypeError("Missing required property 'account_id'")
            __props__.__dict__["account_id"] = account_id
            __props__.__dict__["graph_arn"] = None
        super(OrganizationAdmin, __self__).__init__(
            'aws-native:detective:OrganizationAdmin',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'OrganizationAdmin':
        """
        Get an existing OrganizationAdmin resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = OrganizationAdminArgs.__new__(OrganizationAdminArgs)

        __props__.__dict__["account_id"] = None
        __props__.__dict__["graph_arn"] = None
        return OrganizationAdmin(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="accountId")
    def account_id(self) -> pulumi.Output[str]:
        """
        The account ID of the account that should be registered as your Organization's delegated administrator for Detective
        """
        return pulumi.get(self, "account_id")

    @property
    @pulumi.getter(name="graphArn")
    def graph_arn(self) -> pulumi.Output[str]:
        """
        The Detective graph ARN
        """
        return pulumi.get(self, "graph_arn")

