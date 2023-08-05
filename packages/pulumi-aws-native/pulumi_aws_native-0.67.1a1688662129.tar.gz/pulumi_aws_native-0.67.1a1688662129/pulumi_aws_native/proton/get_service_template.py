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
    'GetServiceTemplateResult',
    'AwaitableGetServiceTemplateResult',
    'get_service_template',
    'get_service_template_output',
]

@pulumi.output_type
class GetServiceTemplateResult:
    def __init__(__self__, arn=None, description=None, display_name=None, tags=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if display_name and not isinstance(display_name, str):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, "display_name", display_name)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        <p>The Amazon Resource Name (ARN) of the service template.</p>
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        <p>A description of the service template.</p>
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[str]:
        """
        <p>The name of the service template as displayed in the developer interface.</p>
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['outputs.ServiceTemplateTag']]:
        """
        <p>An optional list of metadata items that you can associate with the Proton service template. A tag is a key-value pair.</p>
                 <p>For more information, see <a href="https://docs.aws.amazon.com/proton/latest/userguide/resources.html">Proton resources and tagging</a> in the
                <i>Proton User Guide</i>.</p>
        """
        return pulumi.get(self, "tags")


class AwaitableGetServiceTemplateResult(GetServiceTemplateResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetServiceTemplateResult(
            arn=self.arn,
            description=self.description,
            display_name=self.display_name,
            tags=self.tags)


def get_service_template(arn: Optional[str] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetServiceTemplateResult:
    """
    Definition of AWS::Proton::ServiceTemplate Resource Type


    :param str arn: <p>The Amazon Resource Name (ARN) of the service template.</p>
    """
    __args__ = dict()
    __args__['arn'] = arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:proton:getServiceTemplate', __args__, opts=opts, typ=GetServiceTemplateResult).value

    return AwaitableGetServiceTemplateResult(
        arn=__ret__.arn,
        description=__ret__.description,
        display_name=__ret__.display_name,
        tags=__ret__.tags)


@_utilities.lift_output_func(get_service_template)
def get_service_template_output(arn: Optional[pulumi.Input[str]] = None,
                                opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetServiceTemplateResult]:
    """
    Definition of AWS::Proton::ServiceTemplate Resource Type


    :param str arn: <p>The Amazon Resource Name (ARN) of the service template.</p>
    """
    ...
