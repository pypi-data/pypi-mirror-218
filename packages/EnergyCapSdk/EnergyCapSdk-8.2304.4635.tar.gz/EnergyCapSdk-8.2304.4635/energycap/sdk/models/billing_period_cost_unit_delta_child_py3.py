# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class BillingPeriodCostUnitDeltaChild(Model):
    """This data is not currently being used, it has been included for
    completeness.

    :param delta: The change in total cost from the current billing period.
    :type delta: float
    :param cost: The total cost.
    :type cost: float
    :param unit:
    :type unit: ~energycap.sdk.models.UnitChild
    """

    _attribute_map = {
        'delta': {'key': 'delta', 'type': 'float'},
        'cost': {'key': 'cost', 'type': 'float'},
        'unit': {'key': 'unit', 'type': 'UnitChild'},
    }

    def __init__(self, *, delta: float=None, cost: float=None, unit=None, **kwargs) -> None:
        super(BillingPeriodCostUnitDeltaChild, self).__init__(**kwargs)
        self.delta = delta
        self.cost = cost
        self.unit = unit
