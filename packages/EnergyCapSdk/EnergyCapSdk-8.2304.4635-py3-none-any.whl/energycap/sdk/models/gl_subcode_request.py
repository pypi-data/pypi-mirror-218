# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class GLSubcodeRequest(Model):
    """GLSubcodeRequest.

    All required parameters must be populated in order to send to Azure.

    :param sub_code_index: Required. Index of this subcode (1-20) <span
     class='property-internal'>Required</span> <span
     class='property-internal'>Must be between 1 and 20</span>
    :type sub_code_index: int
    :param sub_code_name: Required. Name for this SubCode <span
     class='property-internal'>Required</span> <span
     class='property-internal'>Must be between 0 and 32 characters</span>
    :type sub_code_name: str
    :param sub_code_type: Required. SubCodeType - should be "list"(fixed=1 in
     DB) or "text" (fixed=0 in DB) <span
     class='property-internal'>Required</span> <span
     class='property-internal'>One of list, text </span>
    :type sub_code_type: str
    :param sub_code_values: An array of pick list values when this subcode is
     a "list" <span class='property-internal'>Required when subCodeType is set
     to list</span>
    :type sub_code_values: list[str]
    """

    _validation = {
        'sub_code_index': {'required': True, 'maximum': 20, 'minimum': 1},
        'sub_code_name': {'required': True, 'max_length': 32, 'min_length': 0},
        'sub_code_type': {'required': True},
    }

    _attribute_map = {
        'sub_code_index': {'key': 'subCodeIndex', 'type': 'int'},
        'sub_code_name': {'key': 'subCodeName', 'type': 'str'},
        'sub_code_type': {'key': 'subCodeType', 'type': 'str'},
        'sub_code_values': {'key': 'subCodeValues', 'type': '[str]'},
    }

    def __init__(self, **kwargs):
        super(GLSubcodeRequest, self).__init__(**kwargs)
        self.sub_code_index = kwargs.get('sub_code_index', None)
        self.sub_code_name = kwargs.get('sub_code_name', None)
        self.sub_code_type = kwargs.get('sub_code_type', None)
        self.sub_code_values = kwargs.get('sub_code_values', None)
