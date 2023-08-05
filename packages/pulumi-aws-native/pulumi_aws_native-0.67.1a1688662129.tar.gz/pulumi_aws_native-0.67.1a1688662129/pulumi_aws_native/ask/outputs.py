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
    'SkillAuthenticationConfiguration',
    'SkillOverrides',
    'SkillPackage',
]

@pulumi.output_type
class SkillAuthenticationConfiguration(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "clientId":
            suggest = "client_id"
        elif key == "clientSecret":
            suggest = "client_secret"
        elif key == "refreshToken":
            suggest = "refresh_token"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in SkillAuthenticationConfiguration. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        SkillAuthenticationConfiguration.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        SkillAuthenticationConfiguration.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 client_id: str,
                 client_secret: str,
                 refresh_token: str):
        pulumi.set(__self__, "client_id", client_id)
        pulumi.set(__self__, "client_secret", client_secret)
        pulumi.set(__self__, "refresh_token", refresh_token)

    @property
    @pulumi.getter(name="clientId")
    def client_id(self) -> str:
        return pulumi.get(self, "client_id")

    @property
    @pulumi.getter(name="clientSecret")
    def client_secret(self) -> str:
        return pulumi.get(self, "client_secret")

    @property
    @pulumi.getter(name="refreshToken")
    def refresh_token(self) -> str:
        return pulumi.get(self, "refresh_token")


@pulumi.output_type
class SkillOverrides(dict):
    def __init__(__self__, *,
                 manifest: Optional[Any] = None):
        if manifest is not None:
            pulumi.set(__self__, "manifest", manifest)

    @property
    @pulumi.getter
    def manifest(self) -> Optional[Any]:
        return pulumi.get(self, "manifest")


@pulumi.output_type
class SkillPackage(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "s3Bucket":
            suggest = "s3_bucket"
        elif key == "s3Key":
            suggest = "s3_key"
        elif key == "s3BucketRole":
            suggest = "s3_bucket_role"
        elif key == "s3ObjectVersion":
            suggest = "s3_object_version"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in SkillPackage. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        SkillPackage.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        SkillPackage.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 s3_bucket: str,
                 s3_key: str,
                 overrides: Optional['outputs.SkillOverrides'] = None,
                 s3_bucket_role: Optional[str] = None,
                 s3_object_version: Optional[str] = None):
        pulumi.set(__self__, "s3_bucket", s3_bucket)
        pulumi.set(__self__, "s3_key", s3_key)
        if overrides is not None:
            pulumi.set(__self__, "overrides", overrides)
        if s3_bucket_role is not None:
            pulumi.set(__self__, "s3_bucket_role", s3_bucket_role)
        if s3_object_version is not None:
            pulumi.set(__self__, "s3_object_version", s3_object_version)

    @property
    @pulumi.getter(name="s3Bucket")
    def s3_bucket(self) -> str:
        return pulumi.get(self, "s3_bucket")

    @property
    @pulumi.getter(name="s3Key")
    def s3_key(self) -> str:
        return pulumi.get(self, "s3_key")

    @property
    @pulumi.getter
    def overrides(self) -> Optional['outputs.SkillOverrides']:
        return pulumi.get(self, "overrides")

    @property
    @pulumi.getter(name="s3BucketRole")
    def s3_bucket_role(self) -> Optional[str]:
        return pulumi.get(self, "s3_bucket_role")

    @property
    @pulumi.getter(name="s3ObjectVersion")
    def s3_object_version(self) -> Optional[str]:
        return pulumi.get(self, "s3_object_version")


