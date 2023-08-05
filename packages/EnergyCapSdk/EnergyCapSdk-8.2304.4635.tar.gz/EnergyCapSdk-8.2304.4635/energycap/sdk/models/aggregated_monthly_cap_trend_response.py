# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class AggregatedMonthlyCAPTrendResponse(Model):
    """AggregatedMonthlyCAPTrendResponse.

    :param fiscal_period_range:
    :type fiscal_period_range: ~energycap.sdk.models.PeriodRange
    :param data_details: The data details
    :type data_details: list[~energycap.sdk.models.MonthlyCAPTrend]
    """

    _attribute_map = {
        'fiscal_period_range': {'key': 'fiscalPeriodRange', 'type': 'PeriodRange'},
        'data_details': {'key': 'dataDetails', 'type': '[MonthlyCAPTrend]'},
    }

    def __init__(self, **kwargs):
        super(AggregatedMonthlyCAPTrendResponse, self).__init__(**kwargs)
        self.fiscal_period_range = kwargs.get('fiscal_period_range', None)
        self.data_details = kwargs.get('data_details', None)
