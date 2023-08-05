# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['IntegrationResponseArgs', 'IntegrationResponse']

@pulumi.input_type
class IntegrationResponseArgs:
    def __init__(__self__, *,
                 api_id: pulumi.Input[str],
                 integration_id: pulumi.Input[str],
                 integration_response_key: pulumi.Input[str],
                 content_handling_strategy: Optional[pulumi.Input[str]] = None,
                 response_parameters: Optional[Any] = None,
                 response_templates: Optional[Any] = None,
                 template_selection_expression: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a IntegrationResponse resource.
        :param pulumi.Input[str] api_id: The API identifier
        :param pulumi.Input[str] integration_id: The integration ID
        :param pulumi.Input[str] integration_response_key: The integration response key
        :param pulumi.Input[str] content_handling_strategy:  Specifies how to handle response payload content type conversions
        :param Any response_parameters: A key-value map specifying response parameters that are passed to the method response from the backend
        :param Any response_templates: The collection of response templates for the integration response as a string-to-string map of key-value pairs
        :param pulumi.Input[str] template_selection_expression: The template selection expression for the integration response. Supported only for WebSocket APIs
        """
        pulumi.set(__self__, "api_id", api_id)
        pulumi.set(__self__, "integration_id", integration_id)
        pulumi.set(__self__, "integration_response_key", integration_response_key)
        if content_handling_strategy is not None:
            pulumi.set(__self__, "content_handling_strategy", content_handling_strategy)
        if response_parameters is not None:
            pulumi.set(__self__, "response_parameters", response_parameters)
        if response_templates is not None:
            pulumi.set(__self__, "response_templates", response_templates)
        if template_selection_expression is not None:
            pulumi.set(__self__, "template_selection_expression", template_selection_expression)

    @property
    @pulumi.getter(name="apiId")
    def api_id(self) -> pulumi.Input[str]:
        """
        The API identifier
        """
        return pulumi.get(self, "api_id")

    @api_id.setter
    def api_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "api_id", value)

    @property
    @pulumi.getter(name="integrationId")
    def integration_id(self) -> pulumi.Input[str]:
        """
        The integration ID
        """
        return pulumi.get(self, "integration_id")

    @integration_id.setter
    def integration_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "integration_id", value)

    @property
    @pulumi.getter(name="integrationResponseKey")
    def integration_response_key(self) -> pulumi.Input[str]:
        """
        The integration response key
        """
        return pulumi.get(self, "integration_response_key")

    @integration_response_key.setter
    def integration_response_key(self, value: pulumi.Input[str]):
        pulumi.set(self, "integration_response_key", value)

    @property
    @pulumi.getter(name="contentHandlingStrategy")
    def content_handling_strategy(self) -> Optional[pulumi.Input[str]]:
        """
         Specifies how to handle response payload content type conversions
        """
        return pulumi.get(self, "content_handling_strategy")

    @content_handling_strategy.setter
    def content_handling_strategy(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "content_handling_strategy", value)

    @property
    @pulumi.getter(name="responseParameters")
    def response_parameters(self) -> Optional[Any]:
        """
        A key-value map specifying response parameters that are passed to the method response from the backend
        """
        return pulumi.get(self, "response_parameters")

    @response_parameters.setter
    def response_parameters(self, value: Optional[Any]):
        pulumi.set(self, "response_parameters", value)

    @property
    @pulumi.getter(name="responseTemplates")
    def response_templates(self) -> Optional[Any]:
        """
        The collection of response templates for the integration response as a string-to-string map of key-value pairs
        """
        return pulumi.get(self, "response_templates")

    @response_templates.setter
    def response_templates(self, value: Optional[Any]):
        pulumi.set(self, "response_templates", value)

    @property
    @pulumi.getter(name="templateSelectionExpression")
    def template_selection_expression(self) -> Optional[pulumi.Input[str]]:
        """
        The template selection expression for the integration response. Supported only for WebSocket APIs
        """
        return pulumi.get(self, "template_selection_expression")

    @template_selection_expression.setter
    def template_selection_expression(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "template_selection_expression", value)


class IntegrationResponse(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 api_id: Optional[pulumi.Input[str]] = None,
                 content_handling_strategy: Optional[pulumi.Input[str]] = None,
                 integration_id: Optional[pulumi.Input[str]] = None,
                 integration_response_key: Optional[pulumi.Input[str]] = None,
                 response_parameters: Optional[Any] = None,
                 response_templates: Optional[Any] = None,
                 template_selection_expression: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Schema for ApiGatewayV2 Integration Response

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] api_id: The API identifier
        :param pulumi.Input[str] content_handling_strategy:  Specifies how to handle response payload content type conversions
        :param pulumi.Input[str] integration_id: The integration ID
        :param pulumi.Input[str] integration_response_key: The integration response key
        :param Any response_parameters: A key-value map specifying response parameters that are passed to the method response from the backend
        :param Any response_templates: The collection of response templates for the integration response as a string-to-string map of key-value pairs
        :param pulumi.Input[str] template_selection_expression: The template selection expression for the integration response. Supported only for WebSocket APIs
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: IntegrationResponseArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Schema for ApiGatewayV2 Integration Response

        :param str resource_name: The name of the resource.
        :param IntegrationResponseArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(IntegrationResponseArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 api_id: Optional[pulumi.Input[str]] = None,
                 content_handling_strategy: Optional[pulumi.Input[str]] = None,
                 integration_id: Optional[pulumi.Input[str]] = None,
                 integration_response_key: Optional[pulumi.Input[str]] = None,
                 response_parameters: Optional[Any] = None,
                 response_templates: Optional[Any] = None,
                 template_selection_expression: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = IntegrationResponseArgs.__new__(IntegrationResponseArgs)

            if api_id is None and not opts.urn:
                raise TypeError("Missing required property 'api_id'")
            __props__.__dict__["api_id"] = api_id
            __props__.__dict__["content_handling_strategy"] = content_handling_strategy
            if integration_id is None and not opts.urn:
                raise TypeError("Missing required property 'integration_id'")
            __props__.__dict__["integration_id"] = integration_id
            if integration_response_key is None and not opts.urn:
                raise TypeError("Missing required property 'integration_response_key'")
            __props__.__dict__["integration_response_key"] = integration_response_key
            __props__.__dict__["response_parameters"] = response_parameters
            __props__.__dict__["response_templates"] = response_templates
            __props__.__dict__["template_selection_expression"] = template_selection_expression
            __props__.__dict__["integration_response_id"] = None
        super(IntegrationResponse, __self__).__init__(
            'aws-native:apigatewayv2:IntegrationResponse',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'IntegrationResponse':
        """
        Get an existing IntegrationResponse resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = IntegrationResponseArgs.__new__(IntegrationResponseArgs)

        __props__.__dict__["api_id"] = None
        __props__.__dict__["content_handling_strategy"] = None
        __props__.__dict__["integration_id"] = None
        __props__.__dict__["integration_response_id"] = None
        __props__.__dict__["integration_response_key"] = None
        __props__.__dict__["response_parameters"] = None
        __props__.__dict__["response_templates"] = None
        __props__.__dict__["template_selection_expression"] = None
        return IntegrationResponse(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="apiId")
    def api_id(self) -> pulumi.Output[str]:
        """
        The API identifier
        """
        return pulumi.get(self, "api_id")

    @property
    @pulumi.getter(name="contentHandlingStrategy")
    def content_handling_strategy(self) -> pulumi.Output[Optional[str]]:
        """
         Specifies how to handle response payload content type conversions
        """
        return pulumi.get(self, "content_handling_strategy")

    @property
    @pulumi.getter(name="integrationId")
    def integration_id(self) -> pulumi.Output[str]:
        """
        The integration ID
        """
        return pulumi.get(self, "integration_id")

    @property
    @pulumi.getter(name="integrationResponseId")
    def integration_response_id(self) -> pulumi.Output[str]:
        """
        Integration Response ID generated by service
        """
        return pulumi.get(self, "integration_response_id")

    @property
    @pulumi.getter(name="integrationResponseKey")
    def integration_response_key(self) -> pulumi.Output[str]:
        """
        The integration response key
        """
        return pulumi.get(self, "integration_response_key")

    @property
    @pulumi.getter(name="responseParameters")
    def response_parameters(self) -> pulumi.Output[Optional[Any]]:
        """
        A key-value map specifying response parameters that are passed to the method response from the backend
        """
        return pulumi.get(self, "response_parameters")

    @property
    @pulumi.getter(name="responseTemplates")
    def response_templates(self) -> pulumi.Output[Optional[Any]]:
        """
        The collection of response templates for the integration response as a string-to-string map of key-value pairs
        """
        return pulumi.get(self, "response_templates")

    @property
    @pulumi.getter(name="templateSelectionExpression")
    def template_selection_expression(self) -> pulumi.Output[Optional[str]]:
        """
        The template selection expression for the integration response. Supported only for WebSocket APIs
        """
        return pulumi.get(self, "template_selection_expression")

