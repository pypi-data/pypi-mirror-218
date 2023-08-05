# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class GHGCarbonFootprintResponse(Model):
    """GHGCarbonFootprintResponse.

    :param period_range:
    :type period_range: ~energycap.sdk.models.PeriodRange
    :param target_data:
    :type target_data: ~energycap.sdk.models.GHGTargetEmissions
    :param yearly_data: GHG Emissions data, split by year, then by group and
     gas type.
    :type yearly_data: list[~energycap.sdk.models.GHGYearlyEmissions]
    """

    _attribute_map = {
        'period_range': {'key': 'periodRange', 'type': 'PeriodRange'},
        'target_data': {'key': 'targetData', 'type': 'GHGTargetEmissions'},
        'yearly_data': {'key': 'yearlyData', 'type': '[GHGYearlyEmissions]'},
    }

    def __init__(self, **kwargs):
        super(GHGCarbonFootprintResponse, self).__init__(**kwargs)
        self.period_range = kwargs.get('period_range', None)
        self.target_data = kwargs.get('target_data', None)
        self.yearly_data = kwargs.get('yearly_data', None)
