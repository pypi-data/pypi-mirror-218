# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class MeterGroupResponse(Model):
    """MeterGroupResponse.

    :param meter_group_id: The meter group identifier
    :type meter_group_id: int
    :param meter_group_code: The meter group code
    :type meter_group_code: str
    :param meter_group_info: The meter group info
    :type meter_group_info: str
    :param auto_group: Indicates if this meter group is an autogroup
    :type auto_group: bool
    :param meter_group_category:
    :type meter_group_category: ~energycap.sdk.models.MeterGroupCategoryChild
    :param user_defined_auto_group: Indicates if this meter group is an user
     defined auto group
    :type user_defined_auto_group: bool
    :param last_updated: The last time a member was inserted, updated, or
     deleted from the group
    :type last_updated: datetime
    """

    _attribute_map = {
        'meter_group_id': {'key': 'meterGroupId', 'type': 'int'},
        'meter_group_code': {'key': 'meterGroupCode', 'type': 'str'},
        'meter_group_info': {'key': 'meterGroupInfo', 'type': 'str'},
        'auto_group': {'key': 'autoGroup', 'type': 'bool'},
        'meter_group_category': {'key': 'meterGroupCategory', 'type': 'MeterGroupCategoryChild'},
        'user_defined_auto_group': {'key': 'userDefinedAutoGroup', 'type': 'bool'},
        'last_updated': {'key': 'lastUpdated', 'type': 'iso-8601'},
    }

    def __init__(self, *, meter_group_id: int=None, meter_group_code: str=None, meter_group_info: str=None, auto_group: bool=None, meter_group_category=None, user_defined_auto_group: bool=None, last_updated=None, **kwargs) -> None:
        super(MeterGroupResponse, self).__init__(**kwargs)
        self.meter_group_id = meter_group_id
        self.meter_group_code = meter_group_code
        self.meter_group_info = meter_group_info
        self.auto_group = auto_group
        self.meter_group_category = meter_group_category
        self.user_defined_auto_group = user_defined_auto_group
        self.last_updated = last_updated
