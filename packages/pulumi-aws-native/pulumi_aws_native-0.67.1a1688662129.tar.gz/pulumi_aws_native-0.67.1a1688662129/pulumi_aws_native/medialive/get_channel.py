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
    'GetChannelResult',
    'AwaitableGetChannelResult',
    'get_channel',
    'get_channel_output',
]

@pulumi.output_type
class GetChannelResult:
    def __init__(__self__, arn=None, cdi_input_specification=None, channel_class=None, destinations=None, encoder_settings=None, id=None, input_attachments=None, input_specification=None, inputs=None, log_level=None, maintenance=None, name=None, role_arn=None, tags=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if cdi_input_specification and not isinstance(cdi_input_specification, dict):
            raise TypeError("Expected argument 'cdi_input_specification' to be a dict")
        pulumi.set(__self__, "cdi_input_specification", cdi_input_specification)
        if channel_class and not isinstance(channel_class, str):
            raise TypeError("Expected argument 'channel_class' to be a str")
        pulumi.set(__self__, "channel_class", channel_class)
        if destinations and not isinstance(destinations, list):
            raise TypeError("Expected argument 'destinations' to be a list")
        pulumi.set(__self__, "destinations", destinations)
        if encoder_settings and not isinstance(encoder_settings, dict):
            raise TypeError("Expected argument 'encoder_settings' to be a dict")
        pulumi.set(__self__, "encoder_settings", encoder_settings)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if input_attachments and not isinstance(input_attachments, list):
            raise TypeError("Expected argument 'input_attachments' to be a list")
        pulumi.set(__self__, "input_attachments", input_attachments)
        if input_specification and not isinstance(input_specification, dict):
            raise TypeError("Expected argument 'input_specification' to be a dict")
        pulumi.set(__self__, "input_specification", input_specification)
        if inputs and not isinstance(inputs, list):
            raise TypeError("Expected argument 'inputs' to be a list")
        pulumi.set(__self__, "inputs", inputs)
        if log_level and not isinstance(log_level, str):
            raise TypeError("Expected argument 'log_level' to be a str")
        pulumi.set(__self__, "log_level", log_level)
        if maintenance and not isinstance(maintenance, dict):
            raise TypeError("Expected argument 'maintenance' to be a dict")
        pulumi.set(__self__, "maintenance", maintenance)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if role_arn and not isinstance(role_arn, str):
            raise TypeError("Expected argument 'role_arn' to be a str")
        pulumi.set(__self__, "role_arn", role_arn)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="cdiInputSpecification")
    def cdi_input_specification(self) -> Optional['outputs.ChannelCdiInputSpecification']:
        return pulumi.get(self, "cdi_input_specification")

    @property
    @pulumi.getter(name="channelClass")
    def channel_class(self) -> Optional[str]:
        return pulumi.get(self, "channel_class")

    @property
    @pulumi.getter
    def destinations(self) -> Optional[Sequence['outputs.ChannelOutputDestination']]:
        return pulumi.get(self, "destinations")

    @property
    @pulumi.getter(name="encoderSettings")
    def encoder_settings(self) -> Optional['outputs.ChannelEncoderSettings']:
        return pulumi.get(self, "encoder_settings")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="inputAttachments")
    def input_attachments(self) -> Optional[Sequence['outputs.ChannelInputAttachment']]:
        return pulumi.get(self, "input_attachments")

    @property
    @pulumi.getter(name="inputSpecification")
    def input_specification(self) -> Optional['outputs.ChannelInputSpecification']:
        return pulumi.get(self, "input_specification")

    @property
    @pulumi.getter
    def inputs(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "inputs")

    @property
    @pulumi.getter(name="logLevel")
    def log_level(self) -> Optional[str]:
        return pulumi.get(self, "log_level")

    @property
    @pulumi.getter
    def maintenance(self) -> Optional['outputs.ChannelMaintenanceCreateSettings']:
        return pulumi.get(self, "maintenance")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> Optional[str]:
        return pulumi.get(self, "role_arn")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Any]:
        return pulumi.get(self, "tags")


class AwaitableGetChannelResult(GetChannelResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetChannelResult(
            arn=self.arn,
            cdi_input_specification=self.cdi_input_specification,
            channel_class=self.channel_class,
            destinations=self.destinations,
            encoder_settings=self.encoder_settings,
            id=self.id,
            input_attachments=self.input_attachments,
            input_specification=self.input_specification,
            inputs=self.inputs,
            log_level=self.log_level,
            maintenance=self.maintenance,
            name=self.name,
            role_arn=self.role_arn,
            tags=self.tags)


def get_channel(id: Optional[str] = None,
                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetChannelResult:
    """
    Resource Type definition for AWS::MediaLive::Channel
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:medialive:getChannel', __args__, opts=opts, typ=GetChannelResult).value

    return AwaitableGetChannelResult(
        arn=__ret__.arn,
        cdi_input_specification=__ret__.cdi_input_specification,
        channel_class=__ret__.channel_class,
        destinations=__ret__.destinations,
        encoder_settings=__ret__.encoder_settings,
        id=__ret__.id,
        input_attachments=__ret__.input_attachments,
        input_specification=__ret__.input_specification,
        inputs=__ret__.inputs,
        log_level=__ret__.log_level,
        maintenance=__ret__.maintenance,
        name=__ret__.name,
        role_arn=__ret__.role_arn,
        tags=__ret__.tags)


@_utilities.lift_output_func(get_channel)
def get_channel_output(id: Optional[pulumi.Input[str]] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetChannelResult]:
    """
    Resource Type definition for AWS::MediaLive::Channel
    """
    ...
