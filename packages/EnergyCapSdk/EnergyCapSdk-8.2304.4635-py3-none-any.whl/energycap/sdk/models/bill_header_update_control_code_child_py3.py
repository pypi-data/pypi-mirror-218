# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class BillHeaderUpdateControlCodeChild(Model):
    """Control Code.

    All required parameters must be populated in order to send to Azure.

    :param control_code:  <span class='property-internal'>Must be between 0
     and 255 characters</span> <span class='property-internal'>Required
     (defined)</span>
    :type control_code: str
    :param update: Required. Indicates whether or not the header value is
     being updated <span class='property-internal'>Required</span>
    :type update: bool
    """

    _validation = {
        'control_code': {'max_length': 255, 'min_length': 0},
        'update': {'required': True},
    }

    _attribute_map = {
        'control_code': {'key': 'controlCode', 'type': 'str'},
        'update': {'key': 'update', 'type': 'bool'},
    }

    def __init__(self, *, update: bool, control_code: str=None, **kwargs) -> None:
        super(BillHeaderUpdateControlCodeChild, self).__init__(**kwargs)
        self.control_code = control_code
        self.update = update
