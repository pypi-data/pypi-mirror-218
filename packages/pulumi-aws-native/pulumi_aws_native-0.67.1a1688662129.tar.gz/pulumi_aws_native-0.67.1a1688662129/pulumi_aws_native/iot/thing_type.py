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
from ._inputs import *

__all__ = ['ThingTypeArgs', 'ThingType']

@pulumi.input_type
class ThingTypeArgs:
    def __init__(__self__, *,
                 deprecate_thing_type: Optional[pulumi.Input[bool]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['ThingTypeTagArgs']]]] = None,
                 thing_type_name: Optional[pulumi.Input[str]] = None,
                 thing_type_properties: Optional[pulumi.Input['ThingTypePropertiesPropertiesArgs']] = None):
        """
        The set of arguments for constructing a ThingType resource.
        :param pulumi.Input[Sequence[pulumi.Input['ThingTypeTagArgs']]] tags: An array of key-value pairs to apply to this resource.
        """
        if deprecate_thing_type is not None:
            pulumi.set(__self__, "deprecate_thing_type", deprecate_thing_type)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if thing_type_name is not None:
            pulumi.set(__self__, "thing_type_name", thing_type_name)
        if thing_type_properties is not None:
            pulumi.set(__self__, "thing_type_properties", thing_type_properties)

    @property
    @pulumi.getter(name="deprecateThingType")
    def deprecate_thing_type(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "deprecate_thing_type")

    @deprecate_thing_type.setter
    def deprecate_thing_type(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "deprecate_thing_type", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ThingTypeTagArgs']]]]:
        """
        An array of key-value pairs to apply to this resource.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ThingTypeTagArgs']]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="thingTypeName")
    def thing_type_name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "thing_type_name")

    @thing_type_name.setter
    def thing_type_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "thing_type_name", value)

    @property
    @pulumi.getter(name="thingTypeProperties")
    def thing_type_properties(self) -> Optional[pulumi.Input['ThingTypePropertiesPropertiesArgs']]:
        return pulumi.get(self, "thing_type_properties")

    @thing_type_properties.setter
    def thing_type_properties(self, value: Optional[pulumi.Input['ThingTypePropertiesPropertiesArgs']]):
        pulumi.set(self, "thing_type_properties", value)


class ThingType(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 deprecate_thing_type: Optional[pulumi.Input[bool]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ThingTypeTagArgs']]]]] = None,
                 thing_type_name: Optional[pulumi.Input[str]] = None,
                 thing_type_properties: Optional[pulumi.Input[pulumi.InputType['ThingTypePropertiesPropertiesArgs']]] = None,
                 __props__=None):
        """
        Resource Type definition for AWS::IoT::ThingType

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ThingTypeTagArgs']]]] tags: An array of key-value pairs to apply to this resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[ThingTypeArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource Type definition for AWS::IoT::ThingType

        :param str resource_name: The name of the resource.
        :param ThingTypeArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ThingTypeArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 deprecate_thing_type: Optional[pulumi.Input[bool]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ThingTypeTagArgs']]]]] = None,
                 thing_type_name: Optional[pulumi.Input[str]] = None,
                 thing_type_properties: Optional[pulumi.Input[pulumi.InputType['ThingTypePropertiesPropertiesArgs']]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ThingTypeArgs.__new__(ThingTypeArgs)

            __props__.__dict__["deprecate_thing_type"] = deprecate_thing_type
            __props__.__dict__["tags"] = tags
            __props__.__dict__["thing_type_name"] = thing_type_name
            __props__.__dict__["thing_type_properties"] = thing_type_properties
            __props__.__dict__["arn"] = None
        super(ThingType, __self__).__init__(
            'aws-native:iot:ThingType',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ThingType':
        """
        Get an existing ThingType resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ThingTypeArgs.__new__(ThingTypeArgs)

        __props__.__dict__["arn"] = None
        __props__.__dict__["deprecate_thing_type"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["thing_type_name"] = None
        __props__.__dict__["thing_type_properties"] = None
        return ThingType(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="deprecateThingType")
    def deprecate_thing_type(self) -> pulumi.Output[Optional[bool]]:
        return pulumi.get(self, "deprecate_thing_type")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['outputs.ThingTypeTag']]]:
        """
        An array of key-value pairs to apply to this resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="thingTypeName")
    def thing_type_name(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "thing_type_name")

    @property
    @pulumi.getter(name="thingTypeProperties")
    def thing_type_properties(self) -> pulumi.Output[Optional['outputs.ThingTypePropertiesProperties']]:
        return pulumi.get(self, "thing_type_properties")

