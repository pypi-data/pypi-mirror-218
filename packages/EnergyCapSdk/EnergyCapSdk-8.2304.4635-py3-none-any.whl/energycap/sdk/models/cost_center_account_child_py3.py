# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class CostCenterAccountChild(Model):
    """CostCenterAccountChild.

    :param account_id: The account identifier
    :type account_id: int
    :param account_code: The account code
    :type account_code: str
    :param account_info: The account info
    :type account_info: str
    :param active: Whether the account is active or not
    :type active: bool
    :param has_calculated_meter: Indicates whether the Account has a child
     calculated meter
    :type has_calculated_meter: bool
    :param has_split_parent_meter: Indicates whether the Account is a
     recipient of a split
    :type has_split_parent_meter: bool
    :param has_split_child_meter: Indicates whether the Account has a child
     split meter
    :type has_split_child_meter: bool
    :param account_type:
    :type account_type: ~energycap.sdk.models.AccountTypeChild
    """

    _attribute_map = {
        'account_id': {'key': 'accountId', 'type': 'int'},
        'account_code': {'key': 'accountCode', 'type': 'str'},
        'account_info': {'key': 'accountInfo', 'type': 'str'},
        'active': {'key': 'active', 'type': 'bool'},
        'has_calculated_meter': {'key': 'hasCalculatedMeter', 'type': 'bool'},
        'has_split_parent_meter': {'key': 'hasSplitParentMeter', 'type': 'bool'},
        'has_split_child_meter': {'key': 'hasSplitChildMeter', 'type': 'bool'},
        'account_type': {'key': 'accountType', 'type': 'AccountTypeChild'},
    }

    def __init__(self, *, account_id: int=None, account_code: str=None, account_info: str=None, active: bool=None, has_calculated_meter: bool=None, has_split_parent_meter: bool=None, has_split_child_meter: bool=None, account_type=None, **kwargs) -> None:
        super(CostCenterAccountChild, self).__init__(**kwargs)
        self.account_id = account_id
        self.account_code = account_code
        self.account_info = account_info
        self.active = active
        self.has_calculated_meter = has_calculated_meter
        self.has_split_parent_meter = has_split_parent_meter
        self.has_split_child_meter = has_split_child_meter
        self.account_type = account_type
