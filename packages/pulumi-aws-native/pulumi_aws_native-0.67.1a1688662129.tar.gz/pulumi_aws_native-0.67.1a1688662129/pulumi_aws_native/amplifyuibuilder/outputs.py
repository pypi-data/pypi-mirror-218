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
    'ComponentBindingProperties',
    'ComponentChild',
    'ComponentCollectionProperties',
    'ComponentEvents',
    'ComponentOverrides',
    'ComponentProperties',
    'ComponentTags',
    'ComponentVariant',
    'ComponentVariantValues',
    'FormButton',
    'FormCTA',
    'FormDataTypeConfig',
    'FormFieldPosition',
    'FormFieldsMap',
    'FormSectionalElementMap',
    'FormStyle',
    'FormStyleConfig',
    'FormTags',
    'ThemeTags',
    'ThemeValue',
    'ThemeValues',
]

@pulumi.output_type
class ComponentBindingProperties(dict):
    def __init__(__self__):
        pass


@pulumi.output_type
class ComponentChild(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "componentType":
            suggest = "component_type"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ComponentChild. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ComponentChild.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ComponentChild.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 component_type: str,
                 name: str,
                 properties: 'outputs.ComponentProperties',
                 children: Optional[Sequence['outputs.ComponentChild']] = None,
                 events: Optional['outputs.ComponentEvents'] = None):
        pulumi.set(__self__, "component_type", component_type)
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "properties", properties)
        if children is not None:
            pulumi.set(__self__, "children", children)
        if events is not None:
            pulumi.set(__self__, "events", events)

    @property
    @pulumi.getter(name="componentType")
    def component_type(self) -> str:
        return pulumi.get(self, "component_type")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def properties(self) -> 'outputs.ComponentProperties':
        return pulumi.get(self, "properties")

    @property
    @pulumi.getter
    def children(self) -> Optional[Sequence['outputs.ComponentChild']]:
        return pulumi.get(self, "children")

    @property
    @pulumi.getter
    def events(self) -> Optional['outputs.ComponentEvents']:
        return pulumi.get(self, "events")


@pulumi.output_type
class ComponentCollectionProperties(dict):
    def __init__(__self__):
        pass


@pulumi.output_type
class ComponentEvents(dict):
    def __init__(__self__):
        pass


@pulumi.output_type
class ComponentOverrides(dict):
    def __init__(__self__):
        pass


@pulumi.output_type
class ComponentProperties(dict):
    def __init__(__self__):
        pass


@pulumi.output_type
class ComponentTags(dict):
    def __init__(__self__):
        pass


@pulumi.output_type
class ComponentVariant(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "variantValues":
            suggest = "variant_values"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ComponentVariant. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ComponentVariant.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ComponentVariant.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 overrides: Optional['outputs.ComponentOverrides'] = None,
                 variant_values: Optional['outputs.ComponentVariantValues'] = None):
        if overrides is not None:
            pulumi.set(__self__, "overrides", overrides)
        if variant_values is not None:
            pulumi.set(__self__, "variant_values", variant_values)

    @property
    @pulumi.getter
    def overrides(self) -> Optional['outputs.ComponentOverrides']:
        return pulumi.get(self, "overrides")

    @property
    @pulumi.getter(name="variantValues")
    def variant_values(self) -> Optional['outputs.ComponentVariantValues']:
        return pulumi.get(self, "variant_values")


@pulumi.output_type
class ComponentVariantValues(dict):
    def __init__(__self__):
        pass


@pulumi.output_type
class FormButton(dict):
    def __init__(__self__, *,
                 children: Optional[str] = None,
                 excluded: Optional[bool] = None,
                 position: Optional['outputs.FormFieldPosition'] = None):
        if children is not None:
            pulumi.set(__self__, "children", children)
        if excluded is not None:
            pulumi.set(__self__, "excluded", excluded)
        if position is not None:
            pulumi.set(__self__, "position", position)

    @property
    @pulumi.getter
    def children(self) -> Optional[str]:
        return pulumi.get(self, "children")

    @property
    @pulumi.getter
    def excluded(self) -> Optional[bool]:
        return pulumi.get(self, "excluded")

    @property
    @pulumi.getter
    def position(self) -> Optional['outputs.FormFieldPosition']:
        return pulumi.get(self, "position")


@pulumi.output_type
class FormCTA(dict):
    def __init__(__self__, *,
                 cancel: Optional['outputs.FormButton'] = None,
                 clear: Optional['outputs.FormButton'] = None,
                 position: Optional['FormButtonsPosition'] = None,
                 submit: Optional['outputs.FormButton'] = None):
        if cancel is not None:
            pulumi.set(__self__, "cancel", cancel)
        if clear is not None:
            pulumi.set(__self__, "clear", clear)
        if position is not None:
            pulumi.set(__self__, "position", position)
        if submit is not None:
            pulumi.set(__self__, "submit", submit)

    @property
    @pulumi.getter
    def cancel(self) -> Optional['outputs.FormButton']:
        return pulumi.get(self, "cancel")

    @property
    @pulumi.getter
    def clear(self) -> Optional['outputs.FormButton']:
        return pulumi.get(self, "clear")

    @property
    @pulumi.getter
    def position(self) -> Optional['FormButtonsPosition']:
        return pulumi.get(self, "position")

    @property
    @pulumi.getter
    def submit(self) -> Optional['outputs.FormButton']:
        return pulumi.get(self, "submit")


@pulumi.output_type
class FormDataTypeConfig(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "dataSourceType":
            suggest = "data_source_type"
        elif key == "dataTypeName":
            suggest = "data_type_name"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in FormDataTypeConfig. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        FormDataTypeConfig.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        FormDataTypeConfig.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 data_source_type: 'FormDataSourceType',
                 data_type_name: str):
        pulumi.set(__self__, "data_source_type", data_source_type)
        pulumi.set(__self__, "data_type_name", data_type_name)

    @property
    @pulumi.getter(name="dataSourceType")
    def data_source_type(self) -> 'FormDataSourceType':
        return pulumi.get(self, "data_source_type")

    @property
    @pulumi.getter(name="dataTypeName")
    def data_type_name(self) -> str:
        return pulumi.get(self, "data_type_name")


@pulumi.output_type
class FormFieldPosition(dict):
    def __init__(__self__):
        pass


@pulumi.output_type
class FormFieldsMap(dict):
    def __init__(__self__):
        pass


@pulumi.output_type
class FormSectionalElementMap(dict):
    def __init__(__self__):
        pass


@pulumi.output_type
class FormStyle(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "horizontalGap":
            suggest = "horizontal_gap"
        elif key == "outerPadding":
            suggest = "outer_padding"
        elif key == "verticalGap":
            suggest = "vertical_gap"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in FormStyle. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        FormStyle.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        FormStyle.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 horizontal_gap: Optional['outputs.FormStyleConfig'] = None,
                 outer_padding: Optional['outputs.FormStyleConfig'] = None,
                 vertical_gap: Optional['outputs.FormStyleConfig'] = None):
        if horizontal_gap is not None:
            pulumi.set(__self__, "horizontal_gap", horizontal_gap)
        if outer_padding is not None:
            pulumi.set(__self__, "outer_padding", outer_padding)
        if vertical_gap is not None:
            pulumi.set(__self__, "vertical_gap", vertical_gap)

    @property
    @pulumi.getter(name="horizontalGap")
    def horizontal_gap(self) -> Optional['outputs.FormStyleConfig']:
        return pulumi.get(self, "horizontal_gap")

    @property
    @pulumi.getter(name="outerPadding")
    def outer_padding(self) -> Optional['outputs.FormStyleConfig']:
        return pulumi.get(self, "outer_padding")

    @property
    @pulumi.getter(name="verticalGap")
    def vertical_gap(self) -> Optional['outputs.FormStyleConfig']:
        return pulumi.get(self, "vertical_gap")


@pulumi.output_type
class FormStyleConfig(dict):
    def __init__(__self__):
        pass


@pulumi.output_type
class FormTags(dict):
    def __init__(__self__):
        pass


@pulumi.output_type
class ThemeTags(dict):
    def __init__(__self__):
        pass


@pulumi.output_type
class ThemeValue(dict):
    def __init__(__self__, *,
                 children: Optional[Sequence['outputs.ThemeValues']] = None,
                 value: Optional[str] = None):
        if children is not None:
            pulumi.set(__self__, "children", children)
        if value is not None:
            pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def children(self) -> Optional[Sequence['outputs.ThemeValues']]:
        return pulumi.get(self, "children")

    @property
    @pulumi.getter
    def value(self) -> Optional[str]:
        return pulumi.get(self, "value")


@pulumi.output_type
class ThemeValues(dict):
    def __init__(__self__, *,
                 key: Optional[str] = None,
                 value: Optional['outputs.ThemeValue'] = None):
        if key is not None:
            pulumi.set(__self__, "key", key)
        if value is not None:
            pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> Optional[str]:
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def value(self) -> Optional['outputs.ThemeValue']:
        return pulumi.get(self, "value")


