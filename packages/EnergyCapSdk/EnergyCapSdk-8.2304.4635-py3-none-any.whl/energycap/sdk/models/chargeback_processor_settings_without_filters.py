# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class ChargebackProcessorSettingsWithoutFilters(Model):
    """ChargebackProcessorSettingsWithoutFilters.

    All required parameters must be populated in order to send to Azure.

    :param billing_period: Required. Billing Period to be processed <span
     class='property-internal'>Required</span>
    :type billing_period: int
    :param start_date_for_bill: Optional Start Date for Bill being generated.
     Only used for Calculate Bill and that too when use is not from sub-meter
     reading
     The bills generated will inherit bill headers (accounting period, invoice
     number, control code, etc ) from the batch <span
     class='property-internal'>Must be between 12/31/1899 and 1/1/3000</span>
    :type start_date_for_bill: datetime
    :param end_date_for_bill: Optional End Date for Bill being generated. Only
     used for Calculate Bill and that too when use is not from sub-meter
     reading
     The bills generated will inherit bill headers (accounting period, invoice
     number, control code, etc ) from the batch <span
     class='property-internal'>Must be between 12/31/1899 and 1/1/3000</span>
    :type end_date_for_bill: datetime
    :param note: Optional note/comment
    :type note: str
    :param batch_settings:
    :type batch_settings: ~energycap.sdk.models.BatchCreate
    """

    _validation = {
        'billing_period': {'required': True},
    }

    _attribute_map = {
        'billing_period': {'key': 'billingPeriod', 'type': 'int'},
        'start_date_for_bill': {'key': 'startDateForBill', 'type': 'iso-8601'},
        'end_date_for_bill': {'key': 'endDateForBill', 'type': 'iso-8601'},
        'note': {'key': 'note', 'type': 'str'},
        'batch_settings': {'key': 'batchSettings', 'type': 'BatchCreate'},
    }

    def __init__(self, **kwargs):
        super(ChargebackProcessorSettingsWithoutFilters, self).__init__(**kwargs)
        self.billing_period = kwargs.get('billing_period', None)
        self.start_date_for_bill = kwargs.get('start_date_for_bill', None)
        self.end_date_for_bill = kwargs.get('end_date_for_bill', None)
        self.note = kwargs.get('note', None)
        self.batch_settings = kwargs.get('batch_settings', None)
