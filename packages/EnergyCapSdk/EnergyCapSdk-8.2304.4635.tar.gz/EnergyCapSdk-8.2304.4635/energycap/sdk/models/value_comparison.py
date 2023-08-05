# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class ValueComparison(Model):
    """General purpose value comparison DTO.

    :param current_value:
    :type current_value: ~energycap.sdk.models.ValueWithUnit
    :param previous_value:
    :type previous_value: ~energycap.sdk.models.ValueWithUnit
    """

    _attribute_map = {
        'current_value': {'key': 'currentValue', 'type': 'ValueWithUnit'},
        'previous_value': {'key': 'previousValue', 'type': 'ValueWithUnit'},
    }

    def __init__(self, **kwargs):
        super(ValueComparison, self).__init__(**kwargs)
        self.current_value = kwargs.get('current_value', None)
        self.previous_value = kwargs.get('previous_value', None)
