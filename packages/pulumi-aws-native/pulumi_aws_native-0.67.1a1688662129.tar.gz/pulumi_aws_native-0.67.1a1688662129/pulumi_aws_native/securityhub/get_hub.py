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
    'GetHubResult',
    'AwaitableGetHubResult',
    'get_hub',
    'get_hub_output',
]

@pulumi.output_type
class GetHubResult:
    def __init__(__self__, auto_enable_controls=None, control_finding_generator=None, enable_default_standards=None, id=None, tags=None):
        if auto_enable_controls and not isinstance(auto_enable_controls, bool):
            raise TypeError("Expected argument 'auto_enable_controls' to be a bool")
        pulumi.set(__self__, "auto_enable_controls", auto_enable_controls)
        if control_finding_generator and not isinstance(control_finding_generator, str):
            raise TypeError("Expected argument 'control_finding_generator' to be a str")
        pulumi.set(__self__, "control_finding_generator", control_finding_generator)
        if enable_default_standards and not isinstance(enable_default_standards, bool):
            raise TypeError("Expected argument 'enable_default_standards' to be a bool")
        pulumi.set(__self__, "enable_default_standards", enable_default_standards)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="autoEnableControls")
    def auto_enable_controls(self) -> Optional[bool]:
        return pulumi.get(self, "auto_enable_controls")

    @property
    @pulumi.getter(name="controlFindingGenerator")
    def control_finding_generator(self) -> Optional[str]:
        return pulumi.get(self, "control_finding_generator")

    @property
    @pulumi.getter(name="enableDefaultStandards")
    def enable_default_standards(self) -> Optional[bool]:
        return pulumi.get(self, "enable_default_standards")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Any]:
        return pulumi.get(self, "tags")


class AwaitableGetHubResult(GetHubResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetHubResult(
            auto_enable_controls=self.auto_enable_controls,
            control_finding_generator=self.control_finding_generator,
            enable_default_standards=self.enable_default_standards,
            id=self.id,
            tags=self.tags)


def get_hub(id: Optional[str] = None,
            opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetHubResult:
    """
    Resource Type definition for AWS::SecurityHub::Hub
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:securityhub:getHub', __args__, opts=opts, typ=GetHubResult).value

    return AwaitableGetHubResult(
        auto_enable_controls=__ret__.auto_enable_controls,
        control_finding_generator=__ret__.control_finding_generator,
        enable_default_standards=__ret__.enable_default_standards,
        id=__ret__.id,
        tags=__ret__.tags)


@_utilities.lift_output_func(get_hub)
def get_hub_output(id: Optional[pulumi.Input[str]] = None,
                   opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetHubResult]:
    """
    Resource Type definition for AWS::SecurityHub::Hub
    """
    ...
