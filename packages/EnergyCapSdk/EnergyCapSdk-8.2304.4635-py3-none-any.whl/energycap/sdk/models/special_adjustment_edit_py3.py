# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class SpecialAdjustmentEdit(Model):
    """SpecialAdjustmentEdit.

    All required parameters must be populated in order to send to Azure.

    :param special_adjustment_method_id: Required. The special adjustment
     method identifier <span class='property-internal'>Required</span>
    :type special_adjustment_method_id: int
    :param comments: Required. Reason for making the special adjustment <span
     class='property-internal'>Required</span>
    :type comments: str
    :param value: The amount
     See special adjustment method list for acceptable precision
     Precision of -1 means the value should not be passed in <span
     class='property-internal'>Required (defined)</span>
    :type value: float
    :param special_adjustment_type_id: Required. The special adjustment type
     identifier <span class='property-internal'>Required</span>
    :type special_adjustment_type_id: int
    :param start_date: Required. The start date <span
     class='property-internal'>Required</span>
    :type start_date: datetime
    :param end_date: Required. The end date <span
     class='property-internal'>Required</span>
    :type end_date: datetime
    :param annual_cycle_start_mmdd: The frequency start period
     Should only be passed when frequency type is Recurring <span
     class='property-internal'>Required (defined)</span>
    :type annual_cycle_start_mmdd: int
    :param annual_cycle_end_mmdd: The frequency end period
     Should only be passed when frequency type is Recurring <span
     class='property-internal'>Required (defined)</span>
    :type annual_cycle_end_mmdd: int
    """

    _validation = {
        'special_adjustment_method_id': {'required': True},
        'comments': {'required': True},
        'special_adjustment_type_id': {'required': True},
        'start_date': {'required': True},
        'end_date': {'required': True},
    }

    _attribute_map = {
        'special_adjustment_method_id': {'key': 'specialAdjustmentMethodId', 'type': 'int'},
        'comments': {'key': 'comments', 'type': 'str'},
        'value': {'key': 'value', 'type': 'float'},
        'special_adjustment_type_id': {'key': 'specialAdjustmentTypeId', 'type': 'int'},
        'start_date': {'key': 'startDate', 'type': 'iso-8601'},
        'end_date': {'key': 'endDate', 'type': 'iso-8601'},
        'annual_cycle_start_mmdd': {'key': 'annualCycleStartMMDD', 'type': 'int'},
        'annual_cycle_end_mmdd': {'key': 'annualCycleEndMMDD', 'type': 'int'},
    }

    def __init__(self, *, special_adjustment_method_id: int, comments: str, special_adjustment_type_id: int, start_date, end_date, value: float=None, annual_cycle_start_mmdd: int=None, annual_cycle_end_mmdd: int=None, **kwargs) -> None:
        super(SpecialAdjustmentEdit, self).__init__(**kwargs)
        self.special_adjustment_method_id = special_adjustment_method_id
        self.comments = comments
        self.value = value
        self.special_adjustment_type_id = special_adjustment_type_id
        self.start_date = start_date
        self.end_date = end_date
        self.annual_cycle_start_mmdd = annual_cycle_start_mmdd
        self.annual_cycle_end_mmdd = annual_cycle_end_mmdd
