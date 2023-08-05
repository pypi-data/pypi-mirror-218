# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class AccountMeterChildWithSerialNumber(Model):
    """AccountMeterChildWithSerialNumber.

    :param serial_number: The Serial Number of the Meter
    :type serial_number: str
    :param account_meter_id: The AccountMeter identifier
    :type account_meter_id: int
    :param start_date: The beginning date and time for this AccountMeter
     relationship
    :type start_date: datetime
    :param end_date: The ending date and time for this AccountMeter
     relationship
    :type end_date: datetime
    :param meter_id: The Meter identifier for this AccountMeter
    :type meter_id: int
    :param meter_code: The code of the Meter for this AccountMeter
    :type meter_code: str
    :param meter_info: The info of the Meter for this AccountMeter
    :type meter_info: str
    :param place:
    :type place: ~energycap.sdk.models.PlaceChild
    :param commodity:
    :type commodity: ~energycap.sdk.models.CommodityChild
    :param meter_general_ledger:
    :type meter_general_ledger: ~energycap.sdk.models.GeneralLedgerChild
    :param vendor_type:
    :type vendor_type: ~energycap.sdk.models.VendorTypeChild
    :param active: Indicates whether the Meter is Active
    :type active: bool
    :param is_calculated_meter: Indicates whether the Meter is a calculated
     meter
    :type is_calculated_meter: bool
    :param is_split_parent_meter: Indicates whether the Meter is a parent of a
     split
    :type is_split_parent_meter: bool
    :param is_split_child_meter: Indicates whether the Meter is a child of a
     split
    :type is_split_child_meter: bool
    """

    _attribute_map = {
        'serial_number': {'key': 'serialNumber', 'type': 'str'},
        'account_meter_id': {'key': 'accountMeterId', 'type': 'int'},
        'start_date': {'key': 'startDate', 'type': 'iso-8601'},
        'end_date': {'key': 'endDate', 'type': 'iso-8601'},
        'meter_id': {'key': 'meterId', 'type': 'int'},
        'meter_code': {'key': 'meterCode', 'type': 'str'},
        'meter_info': {'key': 'meterInfo', 'type': 'str'},
        'place': {'key': 'place', 'type': 'PlaceChild'},
        'commodity': {'key': 'commodity', 'type': 'CommodityChild'},
        'meter_general_ledger': {'key': 'meterGeneralLedger', 'type': 'GeneralLedgerChild'},
        'vendor_type': {'key': 'vendorType', 'type': 'VendorTypeChild'},
        'active': {'key': 'active', 'type': 'bool'},
        'is_calculated_meter': {'key': 'isCalculatedMeter', 'type': 'bool'},
        'is_split_parent_meter': {'key': 'isSplitParentMeter', 'type': 'bool'},
        'is_split_child_meter': {'key': 'isSplitChildMeter', 'type': 'bool'},
    }

    def __init__(self, *, serial_number: str=None, account_meter_id: int=None, start_date=None, end_date=None, meter_id: int=None, meter_code: str=None, meter_info: str=None, place=None, commodity=None, meter_general_ledger=None, vendor_type=None, active: bool=None, is_calculated_meter: bool=None, is_split_parent_meter: bool=None, is_split_child_meter: bool=None, **kwargs) -> None:
        super(AccountMeterChildWithSerialNumber, self).__init__(**kwargs)
        self.serial_number = serial_number
        self.account_meter_id = account_meter_id
        self.start_date = start_date
        self.end_date = end_date
        self.meter_id = meter_id
        self.meter_code = meter_code
        self.meter_info = meter_info
        self.place = place
        self.commodity = commodity
        self.meter_general_ledger = meter_general_ledger
        self.vendor_type = vendor_type
        self.active = active
        self.is_calculated_meter = is_calculated_meter
        self.is_split_parent_meter = is_split_parent_meter
        self.is_split_child_meter = is_split_child_meter
