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
    'GetLifecycleHookResult',
    'AwaitableGetLifecycleHookResult',
    'get_lifecycle_hook',
    'get_lifecycle_hook_output',
]

@pulumi.output_type
class GetLifecycleHookResult:
    def __init__(__self__, default_result=None, heartbeat_timeout=None, lifecycle_transition=None, notification_metadata=None, notification_target_arn=None, role_arn=None):
        if default_result and not isinstance(default_result, str):
            raise TypeError("Expected argument 'default_result' to be a str")
        pulumi.set(__self__, "default_result", default_result)
        if heartbeat_timeout and not isinstance(heartbeat_timeout, int):
            raise TypeError("Expected argument 'heartbeat_timeout' to be a int")
        pulumi.set(__self__, "heartbeat_timeout", heartbeat_timeout)
        if lifecycle_transition and not isinstance(lifecycle_transition, str):
            raise TypeError("Expected argument 'lifecycle_transition' to be a str")
        pulumi.set(__self__, "lifecycle_transition", lifecycle_transition)
        if notification_metadata and not isinstance(notification_metadata, str):
            raise TypeError("Expected argument 'notification_metadata' to be a str")
        pulumi.set(__self__, "notification_metadata", notification_metadata)
        if notification_target_arn and not isinstance(notification_target_arn, str):
            raise TypeError("Expected argument 'notification_target_arn' to be a str")
        pulumi.set(__self__, "notification_target_arn", notification_target_arn)
        if role_arn and not isinstance(role_arn, str):
            raise TypeError("Expected argument 'role_arn' to be a str")
        pulumi.set(__self__, "role_arn", role_arn)

    @property
    @pulumi.getter(name="defaultResult")
    def default_result(self) -> Optional[str]:
        """
        The action the Auto Scaling group takes when the lifecycle hook timeout elapses or if an unexpected failure occurs. The valid values are CONTINUE and ABANDON (default).
        """
        return pulumi.get(self, "default_result")

    @property
    @pulumi.getter(name="heartbeatTimeout")
    def heartbeat_timeout(self) -> Optional[int]:
        """
        The maximum time, in seconds, that can elapse before the lifecycle hook times out. The range is from 30 to 7200 seconds. The default value is 3600 seconds (1 hour). If the lifecycle hook times out, Amazon EC2 Auto Scaling performs the action that you specified in the DefaultResult property.
        """
        return pulumi.get(self, "heartbeat_timeout")

    @property
    @pulumi.getter(name="lifecycleTransition")
    def lifecycle_transition(self) -> Optional[str]:
        """
        The instance state to which you want to attach the lifecycle hook.
        """
        return pulumi.get(self, "lifecycle_transition")

    @property
    @pulumi.getter(name="notificationMetadata")
    def notification_metadata(self) -> Optional[str]:
        """
        Additional information that is included any time Amazon EC2 Auto Scaling sends a message to the notification target.
        """
        return pulumi.get(self, "notification_metadata")

    @property
    @pulumi.getter(name="notificationTargetARN")
    def notification_target_arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) of the notification target that Amazon EC2 Auto Scaling uses to notify you when an instance is in the transition state for the lifecycle hook. You can specify an Amazon SQS queue or an Amazon SNS topic. The notification message includes the following information: lifecycle action token, user account ID, Auto Scaling group name, lifecycle hook name, instance ID, lifecycle transition, and notification metadata.
        """
        return pulumi.get(self, "notification_target_arn")

    @property
    @pulumi.getter(name="roleARN")
    def role_arn(self) -> Optional[str]:
        """
        The ARN of the IAM role that allows the Auto Scaling group to publish to the specified notification target, for example, an Amazon SNS topic or an Amazon SQS queue.
        """
        return pulumi.get(self, "role_arn")


class AwaitableGetLifecycleHookResult(GetLifecycleHookResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetLifecycleHookResult(
            default_result=self.default_result,
            heartbeat_timeout=self.heartbeat_timeout,
            lifecycle_transition=self.lifecycle_transition,
            notification_metadata=self.notification_metadata,
            notification_target_arn=self.notification_target_arn,
            role_arn=self.role_arn)


def get_lifecycle_hook(auto_scaling_group_name: Optional[str] = None,
                       lifecycle_hook_name: Optional[str] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetLifecycleHookResult:
    """
    Resource Type definition for AWS::AutoScaling::LifecycleHook


    :param str auto_scaling_group_name: The name of the Auto Scaling group for the lifecycle hook.
    :param str lifecycle_hook_name: The name of the lifecycle hook.
    """
    __args__ = dict()
    __args__['autoScalingGroupName'] = auto_scaling_group_name
    __args__['lifecycleHookName'] = lifecycle_hook_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:autoscaling:getLifecycleHook', __args__, opts=opts, typ=GetLifecycleHookResult).value

    return AwaitableGetLifecycleHookResult(
        default_result=__ret__.default_result,
        heartbeat_timeout=__ret__.heartbeat_timeout,
        lifecycle_transition=__ret__.lifecycle_transition,
        notification_metadata=__ret__.notification_metadata,
        notification_target_arn=__ret__.notification_target_arn,
        role_arn=__ret__.role_arn)


@_utilities.lift_output_func(get_lifecycle_hook)
def get_lifecycle_hook_output(auto_scaling_group_name: Optional[pulumi.Input[str]] = None,
                              lifecycle_hook_name: Optional[pulumi.Input[str]] = None,
                              opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetLifecycleHookResult]:
    """
    Resource Type definition for AWS::AutoScaling::LifecycleHook


    :param str auto_scaling_group_name: The name of the Auto Scaling group for the lifecycle hook.
    :param str lifecycle_hook_name: The name of the lifecycle hook.
    """
    ...
