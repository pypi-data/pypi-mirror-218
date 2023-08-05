# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class WidgetSavingsYearlyResponse(Model):
    """WidgetSavingsYearlyResponse.

    :param billing_period_range:
    :type billing_period_range: ~energycap.sdk.models.PeriodRange
    :param fiscal_period_range:
    :type fiscal_period_range: ~energycap.sdk.models.PeriodRange
    :param all_time_batcc_use: Program to Date BATCC (Baseline Adjusted to
     Current Conditions) Use
    :type all_time_batcc_use: float
    :param all_time_use: Program to Date Use
    :type all_time_use: float
    :param all_time_savings_use: Program to Date Savings Use = allTimeBATCCUse
     - allTimeUse
    :type all_time_savings_use: float
    :param all_time_batcc_total_cost: Program to Date BATCC (Baseline Adjusted
     to Current Conditions) Total Cost
    :type all_time_batcc_total_cost: float
    :param all_time_total_cost: Program to Date Savings Total Cost
    :type all_time_total_cost: float
    :param all_time_savings_total_cost: Program to Date Savings Total Cost =
     allTimeBATCCTotalCost - allTimeTotalCost
    :type all_time_savings_total_cost: float
    :param results: An array of savings yearly data
    :type results:
     list[~energycap.sdk.models.WidgetSavingsYearlyResponseResults]
    :param updated: The date and time the data was updated
    :type updated: datetime
    :param use_unit:
    :type use_unit: ~energycap.sdk.models.UnitChild
    :param cost_unit:
    :type cost_unit: ~energycap.sdk.models.UnitChild
    :param commodities: An array of savings yearly data per commodity
    :type commodities:
     list[~energycap.sdk.models.WidgetSavingsYearlyResponseCommodityData]
    """

    _attribute_map = {
        'billing_period_range': {'key': 'billingPeriodRange', 'type': 'PeriodRange'},
        'fiscal_period_range': {'key': 'fiscalPeriodRange', 'type': 'PeriodRange'},
        'all_time_batcc_use': {'key': 'allTimeBATCCUse', 'type': 'float'},
        'all_time_use': {'key': 'allTimeUse', 'type': 'float'},
        'all_time_savings_use': {'key': 'allTimeSavingsUse', 'type': 'float'},
        'all_time_batcc_total_cost': {'key': 'allTimeBATCCTotalCost', 'type': 'float'},
        'all_time_total_cost': {'key': 'allTimeTotalCost', 'type': 'float'},
        'all_time_savings_total_cost': {'key': 'allTimeSavingsTotalCost', 'type': 'float'},
        'results': {'key': 'results', 'type': '[WidgetSavingsYearlyResponseResults]'},
        'updated': {'key': 'updated', 'type': 'iso-8601'},
        'use_unit': {'key': 'useUnit', 'type': 'UnitChild'},
        'cost_unit': {'key': 'costUnit', 'type': 'UnitChild'},
        'commodities': {'key': 'commodities', 'type': '[WidgetSavingsYearlyResponseCommodityData]'},
    }

    def __init__(self, *, billing_period_range=None, fiscal_period_range=None, all_time_batcc_use: float=None, all_time_use: float=None, all_time_savings_use: float=None, all_time_batcc_total_cost: float=None, all_time_total_cost: float=None, all_time_savings_total_cost: float=None, results=None, updated=None, use_unit=None, cost_unit=None, commodities=None, **kwargs) -> None:
        super(WidgetSavingsYearlyResponse, self).__init__(**kwargs)
        self.billing_period_range = billing_period_range
        self.fiscal_period_range = fiscal_period_range
        self.all_time_batcc_use = all_time_batcc_use
        self.all_time_use = all_time_use
        self.all_time_savings_use = all_time_savings_use
        self.all_time_batcc_total_cost = all_time_batcc_total_cost
        self.all_time_total_cost = all_time_total_cost
        self.all_time_savings_total_cost = all_time_savings_total_cost
        self.results = results
        self.updated = updated
        self.use_unit = use_unit
        self.cost_unit = cost_unit
        self.commodities = commodities
