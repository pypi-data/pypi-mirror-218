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
    'GetStackResult',
    'AwaitableGetStackResult',
    'get_stack',
    'get_stack_output',
]

@pulumi.output_type
class GetStackResult:
    def __init__(__self__, id=None, notification_arns=None, parameters=None, tags=None, template_url=None, timeout_in_minutes=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if notification_arns and not isinstance(notification_arns, list):
            raise TypeError("Expected argument 'notification_arns' to be a list")
        pulumi.set(__self__, "notification_arns", notification_arns)
        if parameters and not isinstance(parameters, dict):
            raise TypeError("Expected argument 'parameters' to be a dict")
        pulumi.set(__self__, "parameters", parameters)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)
        if template_url and not isinstance(template_url, str):
            raise TypeError("Expected argument 'template_url' to be a str")
        pulumi.set(__self__, "template_url", template_url)
        if timeout_in_minutes and not isinstance(timeout_in_minutes, int):
            raise TypeError("Expected argument 'timeout_in_minutes' to be a int")
        pulumi.set(__self__, "timeout_in_minutes", timeout_in_minutes)

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="notificationARNs")
    def notification_arns(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "notification_arns")

    @property
    @pulumi.getter
    def parameters(self) -> Optional[Any]:
        return pulumi.get(self, "parameters")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['outputs.StackTag']]:
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="templateURL")
    def template_url(self) -> Optional[str]:
        return pulumi.get(self, "template_url")

    @property
    @pulumi.getter(name="timeoutInMinutes")
    def timeout_in_minutes(self) -> Optional[int]:
        return pulumi.get(self, "timeout_in_minutes")


class AwaitableGetStackResult(GetStackResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetStackResult(
            id=self.id,
            notification_arns=self.notification_arns,
            parameters=self.parameters,
            tags=self.tags,
            template_url=self.template_url,
            timeout_in_minutes=self.timeout_in_minutes)


def get_stack(id: Optional[str] = None,
              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetStackResult:
    """
    Resource Type definition for AWS::CloudFormation::Stack
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:cloudformation:getStack', __args__, opts=opts, typ=GetStackResult).value

    return AwaitableGetStackResult(
        id=__ret__.id,
        notification_arns=__ret__.notification_arns,
        parameters=__ret__.parameters,
        tags=__ret__.tags,
        template_url=__ret__.template_url,
        timeout_in_minutes=__ret__.timeout_in_minutes)


@_utilities.lift_output_func(get_stack)
def get_stack_output(id: Optional[pulumi.Input[str]] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetStackResult]:
    """
    Resource Type definition for AWS::CloudFormation::Stack
    """
    ...
