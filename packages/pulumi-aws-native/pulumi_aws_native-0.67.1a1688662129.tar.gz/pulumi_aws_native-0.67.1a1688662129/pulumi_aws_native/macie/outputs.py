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
    'AllowListCriteria',
    'AllowListTag',
    'FindingsFilterCriterion',
    'FindingsFilterFindingCriteria',
]

@pulumi.output_type
class AllowListCriteria(dict):
    """
    The regex or s3 object to use for the AllowList.
    """
    def __init__(__self__):
        """
        The regex or s3 object to use for the AllowList.
        """
        pass


@pulumi.output_type
class AllowListTag(dict):
    """
    A key-value pair to associate with a resource.
    """
    def __init__(__self__, *,
                 key: str,
                 value: str):
        """
        A key-value pair to associate with a resource.
        :param str key: The tag's key.
        :param str value: The tag's value.
        """
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> str:
        """
        The tag's key.
        """
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        The tag's value.
        """
        return pulumi.get(self, "value")


@pulumi.output_type
class FindingsFilterCriterion(dict):
    """
    Map of filter criteria.
    """
    def __init__(__self__):
        """
        Map of filter criteria.
        """
        pass


@pulumi.output_type
class FindingsFilterFindingCriteria(dict):
    def __init__(__self__, *,
                 criterion: Optional['outputs.FindingsFilterCriterion'] = None):
        if criterion is not None:
            pulumi.set(__self__, "criterion", criterion)

    @property
    @pulumi.getter
    def criterion(self) -> Optional['outputs.FindingsFilterCriterion']:
        return pulumi.get(self, "criterion")


