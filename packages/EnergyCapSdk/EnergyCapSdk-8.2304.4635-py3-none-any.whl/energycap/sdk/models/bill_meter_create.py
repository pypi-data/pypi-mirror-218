# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class BillMeterCreate(Model):
    """BillMeterCreate.

    All required parameters must be populated in order to send to Azure.

    :param meter_id: Required. The meter the line items are assigned to <span
     class='property-internal'>Required</span>
    :type meter_id: int
    :param body_lines: Required.  <span
     class='property-internal'>Required</span> <span
     class='property-internal'>Cannot be Empty</span>
    :type body_lines: list[~energycap.sdk.models.BillMeterBodyLineCreate]
    """

    _validation = {
        'meter_id': {'required': True},
        'body_lines': {'required': True},
    }

    _attribute_map = {
        'meter_id': {'key': 'meterId', 'type': 'int'},
        'body_lines': {'key': 'bodyLines', 'type': '[BillMeterBodyLineCreate]'},
    }

    def __init__(self, **kwargs):
        super(BillMeterCreate, self).__init__(**kwargs)
        self.meter_id = kwargs.get('meter_id', None)
        self.body_lines = kwargs.get('body_lines', None)
