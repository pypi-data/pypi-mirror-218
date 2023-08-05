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
    'GetProjectResult',
    'AwaitableGetProjectResult',
    'get_project',
    'get_project_output',
]

@pulumi.output_type
class GetProjectResult:
    def __init__(__self__, arn=None, default_job_timeout_minutes=None, name=None, tags=None, vpc_config=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if default_job_timeout_minutes and not isinstance(default_job_timeout_minutes, int):
            raise TypeError("Expected argument 'default_job_timeout_minutes' to be a int")
        pulumi.set(__self__, "default_job_timeout_minutes", default_job_timeout_minutes)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)
        if vpc_config and not isinstance(vpc_config, dict):
            raise TypeError("Expected argument 'vpc_config' to be a dict")
        pulumi.set(__self__, "vpc_config", vpc_config)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="defaultJobTimeoutMinutes")
    def default_job_timeout_minutes(self) -> Optional[int]:
        return pulumi.get(self, "default_job_timeout_minutes")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['outputs.ProjectTag']]:
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="vpcConfig")
    def vpc_config(self) -> Optional['outputs.ProjectVpcConfig']:
        return pulumi.get(self, "vpc_config")


class AwaitableGetProjectResult(GetProjectResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetProjectResult(
            arn=self.arn,
            default_job_timeout_minutes=self.default_job_timeout_minutes,
            name=self.name,
            tags=self.tags,
            vpc_config=self.vpc_config)


def get_project(arn: Optional[str] = None,
                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetProjectResult:
    """
    AWS::DeviceFarm::Project creates a new Device Farm Project
    """
    __args__ = dict()
    __args__['arn'] = arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:devicefarm:getProject', __args__, opts=opts, typ=GetProjectResult).value

    return AwaitableGetProjectResult(
        arn=__ret__.arn,
        default_job_timeout_minutes=__ret__.default_job_timeout_minutes,
        name=__ret__.name,
        tags=__ret__.tags,
        vpc_config=__ret__.vpc_config)


@_utilities.lift_output_func(get_project)
def get_project_output(arn: Optional[pulumi.Input[str]] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetProjectResult]:
    """
    AWS::DeviceFarm::Project creates a new Device Farm Project
    """
    ...
