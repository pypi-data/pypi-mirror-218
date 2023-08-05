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
    'GetAttributeGroupAssociationResult',
    'AwaitableGetAttributeGroupAssociationResult',
    'get_attribute_group_association',
    'get_attribute_group_association_output',
]

@pulumi.output_type
class GetAttributeGroupAssociationResult:
    def __init__(__self__, application_arn=None, attribute_group_arn=None, id=None):
        if application_arn and not isinstance(application_arn, str):
            raise TypeError("Expected argument 'application_arn' to be a str")
        pulumi.set(__self__, "application_arn", application_arn)
        if attribute_group_arn and not isinstance(attribute_group_arn, str):
            raise TypeError("Expected argument 'attribute_group_arn' to be a str")
        pulumi.set(__self__, "attribute_group_arn", attribute_group_arn)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)

    @property
    @pulumi.getter(name="applicationArn")
    def application_arn(self) -> Optional[str]:
        return pulumi.get(self, "application_arn")

    @property
    @pulumi.getter(name="attributeGroupArn")
    def attribute_group_arn(self) -> Optional[str]:
        return pulumi.get(self, "attribute_group_arn")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        return pulumi.get(self, "id")


class AwaitableGetAttributeGroupAssociationResult(GetAttributeGroupAssociationResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAttributeGroupAssociationResult(
            application_arn=self.application_arn,
            attribute_group_arn=self.attribute_group_arn,
            id=self.id)


def get_attribute_group_association(id: Optional[str] = None,
                                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAttributeGroupAssociationResult:
    """
    Resource Schema for AWS::ServiceCatalogAppRegistry::AttributeGroupAssociation.
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:servicecatalogappregistry:getAttributeGroupAssociation', __args__, opts=opts, typ=GetAttributeGroupAssociationResult).value

    return AwaitableGetAttributeGroupAssociationResult(
        application_arn=__ret__.application_arn,
        attribute_group_arn=__ret__.attribute_group_arn,
        id=__ret__.id)


@_utilities.lift_output_func(get_attribute_group_association)
def get_attribute_group_association_output(id: Optional[pulumi.Input[str]] = None,
                                           opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetAttributeGroupAssociationResult]:
    """
    Resource Schema for AWS::ServiceCatalogAppRegistry::AttributeGroupAssociation.
    """
    ...
