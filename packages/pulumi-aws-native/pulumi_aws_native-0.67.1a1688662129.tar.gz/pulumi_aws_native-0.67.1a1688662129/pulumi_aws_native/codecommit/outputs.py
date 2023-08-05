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
    'RepositoryCode',
    'RepositoryS3',
    'RepositoryTag',
    'RepositoryTrigger',
]

@pulumi.output_type
class RepositoryCode(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "branchName":
            suggest = "branch_name"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in RepositoryCode. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        RepositoryCode.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        RepositoryCode.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 s3: 'outputs.RepositoryS3',
                 branch_name: Optional[str] = None):
        pulumi.set(__self__, "s3", s3)
        if branch_name is not None:
            pulumi.set(__self__, "branch_name", branch_name)

    @property
    @pulumi.getter
    def s3(self) -> 'outputs.RepositoryS3':
        return pulumi.get(self, "s3")

    @property
    @pulumi.getter(name="branchName")
    def branch_name(self) -> Optional[str]:
        return pulumi.get(self, "branch_name")


@pulumi.output_type
class RepositoryS3(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "objectVersion":
            suggest = "object_version"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in RepositoryS3. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        RepositoryS3.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        RepositoryS3.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 bucket: str,
                 key: str,
                 object_version: Optional[str] = None):
        pulumi.set(__self__, "bucket", bucket)
        pulumi.set(__self__, "key", key)
        if object_version is not None:
            pulumi.set(__self__, "object_version", object_version)

    @property
    @pulumi.getter
    def bucket(self) -> str:
        return pulumi.get(self, "bucket")

    @property
    @pulumi.getter
    def key(self) -> str:
        return pulumi.get(self, "key")

    @property
    @pulumi.getter(name="objectVersion")
    def object_version(self) -> Optional[str]:
        return pulumi.get(self, "object_version")


@pulumi.output_type
class RepositoryTag(dict):
    def __init__(__self__, *,
                 key: str,
                 value: str):
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> str:
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def value(self) -> str:
        return pulumi.get(self, "value")


@pulumi.output_type
class RepositoryTrigger(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "destinationArn":
            suggest = "destination_arn"
        elif key == "customData":
            suggest = "custom_data"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in RepositoryTrigger. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        RepositoryTrigger.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        RepositoryTrigger.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 destination_arn: str,
                 events: Sequence[str],
                 name: str,
                 branches: Optional[Sequence[str]] = None,
                 custom_data: Optional[str] = None):
        pulumi.set(__self__, "destination_arn", destination_arn)
        pulumi.set(__self__, "events", events)
        pulumi.set(__self__, "name", name)
        if branches is not None:
            pulumi.set(__self__, "branches", branches)
        if custom_data is not None:
            pulumi.set(__self__, "custom_data", custom_data)

    @property
    @pulumi.getter(name="destinationArn")
    def destination_arn(self) -> str:
        return pulumi.get(self, "destination_arn")

    @property
    @pulumi.getter
    def events(self) -> Sequence[str]:
        return pulumi.get(self, "events")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def branches(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "branches")

    @property
    @pulumi.getter(name="customData")
    def custom_data(self) -> Optional[str]:
        return pulumi.get(self, "custom_data")


