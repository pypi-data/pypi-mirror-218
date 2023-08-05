# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class UDFFieldChild(Model):
    """UDFFieldChild.

    :param udf_id:  <span class='property-internal'>Required (defined)</span>
    :type udf_id: int
    :param data_type:
    :type data_type: ~energycap.sdk.models.DataTypeResponse
    :param name:  <span class='property-internal'>Required (defined)</span>
    :type name: str
    :param description:  <span class='property-internal'>Required
     (defined)</span>
    :type description: str
    :param display_order:  <span class='property-internal'>Required
     (defined)</span>
    :type display_order: int
    :param value:  <span class='property-internal'>Required (defined)</span>
    :type value: str
    :param udf_select_values:  <span class='property-internal'>Required
     (defined)</span>
    :type udf_select_values:
     list[~energycap.sdk.models.UDFSelectValueEntityResponse]
    :param important:  <span class='property-internal'>Required
     (defined)</span>
    :type important: bool
    """

    _attribute_map = {
        'udf_id': {'key': 'udfId', 'type': 'int'},
        'data_type': {'key': 'dataType', 'type': 'DataTypeResponse'},
        'name': {'key': 'name', 'type': 'str'},
        'description': {'key': 'description', 'type': 'str'},
        'display_order': {'key': 'displayOrder', 'type': 'int'},
        'value': {'key': 'value', 'type': 'str'},
        'udf_select_values': {'key': 'udfSelectValues', 'type': '[UDFSelectValueEntityResponse]'},
        'important': {'key': 'important', 'type': 'bool'},
    }

    def __init__(self, *, udf_id: int=None, data_type=None, name: str=None, description: str=None, display_order: int=None, value: str=None, udf_select_values=None, important: bool=None, **kwargs) -> None:
        super(UDFFieldChild, self).__init__(**kwargs)
        self.udf_id = udf_id
        self.data_type = data_type
        self.name = name
        self.description = description
        self.display_order = display_order
        self.value = value
        self.udf_select_values = udf_select_values
        self.important = important
