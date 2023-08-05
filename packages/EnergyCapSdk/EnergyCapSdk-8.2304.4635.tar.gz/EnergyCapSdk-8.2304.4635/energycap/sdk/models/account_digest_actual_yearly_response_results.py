# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class AccountDigestActualYearlyResponseResults(Model):
    """AccountDigestActualYearlyResponseResults.

    :param year: Year
    :type year: str
    :param total_cost: Total Cost
    :type total_cost: float
    :param global_use: Global Use
    :type global_use: float
    :param global_use_unit_cost: Global Use Unit Cost
    :type global_use_unit_cost: float
    """

    _attribute_map = {
        'year': {'key': 'year', 'type': 'str'},
        'total_cost': {'key': 'totalCost', 'type': 'float'},
        'global_use': {'key': 'globalUse', 'type': 'float'},
        'global_use_unit_cost': {'key': 'globalUseUnitCost', 'type': 'float'},
    }

    def __init__(self, **kwargs):
        super(AccountDigestActualYearlyResponseResults, self).__init__(**kwargs)
        self.year = kwargs.get('year', None)
        self.total_cost = kwargs.get('total_cost', None)
        self.global_use = kwargs.get('global_use', None)
        self.global_use_unit_cost = kwargs.get('global_use_unit_cost', None)
