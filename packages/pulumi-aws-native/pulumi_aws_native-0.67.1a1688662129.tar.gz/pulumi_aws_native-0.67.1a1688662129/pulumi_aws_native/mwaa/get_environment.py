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
from ._enums import *

__all__ = [
    'GetEnvironmentResult',
    'AwaitableGetEnvironmentResult',
    'get_environment',
    'get_environment_output',
]

@pulumi.output_type
class GetEnvironmentResult:
    def __init__(__self__, airflow_configuration_options=None, airflow_version=None, arn=None, dag_s3_path=None, environment_class=None, execution_role_arn=None, logging_configuration=None, max_workers=None, min_workers=None, network_configuration=None, plugins_s3_object_version=None, plugins_s3_path=None, requirements_s3_object_version=None, requirements_s3_path=None, schedulers=None, source_bucket_arn=None, startup_script_s3_object_version=None, startup_script_s3_path=None, tags=None, webserver_access_mode=None, webserver_url=None, weekly_maintenance_window_start=None):
        if airflow_configuration_options and not isinstance(airflow_configuration_options, dict):
            raise TypeError("Expected argument 'airflow_configuration_options' to be a dict")
        pulumi.set(__self__, "airflow_configuration_options", airflow_configuration_options)
        if airflow_version and not isinstance(airflow_version, str):
            raise TypeError("Expected argument 'airflow_version' to be a str")
        pulumi.set(__self__, "airflow_version", airflow_version)
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if dag_s3_path and not isinstance(dag_s3_path, str):
            raise TypeError("Expected argument 'dag_s3_path' to be a str")
        pulumi.set(__self__, "dag_s3_path", dag_s3_path)
        if environment_class and not isinstance(environment_class, str):
            raise TypeError("Expected argument 'environment_class' to be a str")
        pulumi.set(__self__, "environment_class", environment_class)
        if execution_role_arn and not isinstance(execution_role_arn, str):
            raise TypeError("Expected argument 'execution_role_arn' to be a str")
        pulumi.set(__self__, "execution_role_arn", execution_role_arn)
        if logging_configuration and not isinstance(logging_configuration, dict):
            raise TypeError("Expected argument 'logging_configuration' to be a dict")
        pulumi.set(__self__, "logging_configuration", logging_configuration)
        if max_workers and not isinstance(max_workers, int):
            raise TypeError("Expected argument 'max_workers' to be a int")
        pulumi.set(__self__, "max_workers", max_workers)
        if min_workers and not isinstance(min_workers, int):
            raise TypeError("Expected argument 'min_workers' to be a int")
        pulumi.set(__self__, "min_workers", min_workers)
        if network_configuration and not isinstance(network_configuration, dict):
            raise TypeError("Expected argument 'network_configuration' to be a dict")
        pulumi.set(__self__, "network_configuration", network_configuration)
        if plugins_s3_object_version and not isinstance(plugins_s3_object_version, str):
            raise TypeError("Expected argument 'plugins_s3_object_version' to be a str")
        pulumi.set(__self__, "plugins_s3_object_version", plugins_s3_object_version)
        if plugins_s3_path and not isinstance(plugins_s3_path, str):
            raise TypeError("Expected argument 'plugins_s3_path' to be a str")
        pulumi.set(__self__, "plugins_s3_path", plugins_s3_path)
        if requirements_s3_object_version and not isinstance(requirements_s3_object_version, str):
            raise TypeError("Expected argument 'requirements_s3_object_version' to be a str")
        pulumi.set(__self__, "requirements_s3_object_version", requirements_s3_object_version)
        if requirements_s3_path and not isinstance(requirements_s3_path, str):
            raise TypeError("Expected argument 'requirements_s3_path' to be a str")
        pulumi.set(__self__, "requirements_s3_path", requirements_s3_path)
        if schedulers and not isinstance(schedulers, int):
            raise TypeError("Expected argument 'schedulers' to be a int")
        pulumi.set(__self__, "schedulers", schedulers)
        if source_bucket_arn and not isinstance(source_bucket_arn, str):
            raise TypeError("Expected argument 'source_bucket_arn' to be a str")
        pulumi.set(__self__, "source_bucket_arn", source_bucket_arn)
        if startup_script_s3_object_version and not isinstance(startup_script_s3_object_version, str):
            raise TypeError("Expected argument 'startup_script_s3_object_version' to be a str")
        pulumi.set(__self__, "startup_script_s3_object_version", startup_script_s3_object_version)
        if startup_script_s3_path and not isinstance(startup_script_s3_path, str):
            raise TypeError("Expected argument 'startup_script_s3_path' to be a str")
        pulumi.set(__self__, "startup_script_s3_path", startup_script_s3_path)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if webserver_access_mode and not isinstance(webserver_access_mode, str):
            raise TypeError("Expected argument 'webserver_access_mode' to be a str")
        pulumi.set(__self__, "webserver_access_mode", webserver_access_mode)
        if webserver_url and not isinstance(webserver_url, str):
            raise TypeError("Expected argument 'webserver_url' to be a str")
        pulumi.set(__self__, "webserver_url", webserver_url)
        if weekly_maintenance_window_start and not isinstance(weekly_maintenance_window_start, str):
            raise TypeError("Expected argument 'weekly_maintenance_window_start' to be a str")
        pulumi.set(__self__, "weekly_maintenance_window_start", weekly_maintenance_window_start)

    @property
    @pulumi.getter(name="airflowConfigurationOptions")
    def airflow_configuration_options(self) -> Optional[Any]:
        """
        Key/value pairs representing Airflow configuration variables.
            Keys are prefixed by their section:

            [core]
            dags_folder={AIRFLOW_HOME}/dags

            Would be represented as

            "core.dags_folder": "{AIRFLOW_HOME}/dags"
        """
        return pulumi.get(self, "airflow_configuration_options")

    @property
    @pulumi.getter(name="airflowVersion")
    def airflow_version(self) -> Optional[str]:
        return pulumi.get(self, "airflow_version")

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="dagS3Path")
    def dag_s3_path(self) -> Optional[str]:
        return pulumi.get(self, "dag_s3_path")

    @property
    @pulumi.getter(name="environmentClass")
    def environment_class(self) -> Optional[str]:
        return pulumi.get(self, "environment_class")

    @property
    @pulumi.getter(name="executionRoleArn")
    def execution_role_arn(self) -> Optional[str]:
        return pulumi.get(self, "execution_role_arn")

    @property
    @pulumi.getter(name="loggingConfiguration")
    def logging_configuration(self) -> Optional['outputs.EnvironmentLoggingConfiguration']:
        return pulumi.get(self, "logging_configuration")

    @property
    @pulumi.getter(name="maxWorkers")
    def max_workers(self) -> Optional[int]:
        return pulumi.get(self, "max_workers")

    @property
    @pulumi.getter(name="minWorkers")
    def min_workers(self) -> Optional[int]:
        return pulumi.get(self, "min_workers")

    @property
    @pulumi.getter(name="networkConfiguration")
    def network_configuration(self) -> Optional['outputs.EnvironmentNetworkConfiguration']:
        return pulumi.get(self, "network_configuration")

    @property
    @pulumi.getter(name="pluginsS3ObjectVersion")
    def plugins_s3_object_version(self) -> Optional[str]:
        return pulumi.get(self, "plugins_s3_object_version")

    @property
    @pulumi.getter(name="pluginsS3Path")
    def plugins_s3_path(self) -> Optional[str]:
        return pulumi.get(self, "plugins_s3_path")

    @property
    @pulumi.getter(name="requirementsS3ObjectVersion")
    def requirements_s3_object_version(self) -> Optional[str]:
        return pulumi.get(self, "requirements_s3_object_version")

    @property
    @pulumi.getter(name="requirementsS3Path")
    def requirements_s3_path(self) -> Optional[str]:
        return pulumi.get(self, "requirements_s3_path")

    @property
    @pulumi.getter
    def schedulers(self) -> Optional[int]:
        return pulumi.get(self, "schedulers")

    @property
    @pulumi.getter(name="sourceBucketArn")
    def source_bucket_arn(self) -> Optional[str]:
        return pulumi.get(self, "source_bucket_arn")

    @property
    @pulumi.getter(name="startupScriptS3ObjectVersion")
    def startup_script_s3_object_version(self) -> Optional[str]:
        return pulumi.get(self, "startup_script_s3_object_version")

    @property
    @pulumi.getter(name="startupScriptS3Path")
    def startup_script_s3_path(self) -> Optional[str]:
        return pulumi.get(self, "startup_script_s3_path")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Any]:
        """
        A map of tags for the environment.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="webserverAccessMode")
    def webserver_access_mode(self) -> Optional['EnvironmentWebserverAccessMode']:
        return pulumi.get(self, "webserver_access_mode")

    @property
    @pulumi.getter(name="webserverUrl")
    def webserver_url(self) -> Optional[str]:
        return pulumi.get(self, "webserver_url")

    @property
    @pulumi.getter(name="weeklyMaintenanceWindowStart")
    def weekly_maintenance_window_start(self) -> Optional[str]:
        return pulumi.get(self, "weekly_maintenance_window_start")


class AwaitableGetEnvironmentResult(GetEnvironmentResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetEnvironmentResult(
            airflow_configuration_options=self.airflow_configuration_options,
            airflow_version=self.airflow_version,
            arn=self.arn,
            dag_s3_path=self.dag_s3_path,
            environment_class=self.environment_class,
            execution_role_arn=self.execution_role_arn,
            logging_configuration=self.logging_configuration,
            max_workers=self.max_workers,
            min_workers=self.min_workers,
            network_configuration=self.network_configuration,
            plugins_s3_object_version=self.plugins_s3_object_version,
            plugins_s3_path=self.plugins_s3_path,
            requirements_s3_object_version=self.requirements_s3_object_version,
            requirements_s3_path=self.requirements_s3_path,
            schedulers=self.schedulers,
            source_bucket_arn=self.source_bucket_arn,
            startup_script_s3_object_version=self.startup_script_s3_object_version,
            startup_script_s3_path=self.startup_script_s3_path,
            tags=self.tags,
            webserver_access_mode=self.webserver_access_mode,
            webserver_url=self.webserver_url,
            weekly_maintenance_window_start=self.weekly_maintenance_window_start)


def get_environment(name: Optional[str] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetEnvironmentResult:
    """
    Resource schema for AWS::MWAA::Environment
    """
    __args__ = dict()
    __args__['name'] = name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:mwaa:getEnvironment', __args__, opts=opts, typ=GetEnvironmentResult).value

    return AwaitableGetEnvironmentResult(
        airflow_configuration_options=__ret__.airflow_configuration_options,
        airflow_version=__ret__.airflow_version,
        arn=__ret__.arn,
        dag_s3_path=__ret__.dag_s3_path,
        environment_class=__ret__.environment_class,
        execution_role_arn=__ret__.execution_role_arn,
        logging_configuration=__ret__.logging_configuration,
        max_workers=__ret__.max_workers,
        min_workers=__ret__.min_workers,
        network_configuration=__ret__.network_configuration,
        plugins_s3_object_version=__ret__.plugins_s3_object_version,
        plugins_s3_path=__ret__.plugins_s3_path,
        requirements_s3_object_version=__ret__.requirements_s3_object_version,
        requirements_s3_path=__ret__.requirements_s3_path,
        schedulers=__ret__.schedulers,
        source_bucket_arn=__ret__.source_bucket_arn,
        startup_script_s3_object_version=__ret__.startup_script_s3_object_version,
        startup_script_s3_path=__ret__.startup_script_s3_path,
        tags=__ret__.tags,
        webserver_access_mode=__ret__.webserver_access_mode,
        webserver_url=__ret__.webserver_url,
        weekly_maintenance_window_start=__ret__.weekly_maintenance_window_start)


@_utilities.lift_output_func(get_environment)
def get_environment_output(name: Optional[pulumi.Input[str]] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetEnvironmentResult]:
    """
    Resource schema for AWS::MWAA::Environment
    """
    ...
