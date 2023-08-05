# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class AccountingSettingsRequest(Model):
    """AccountingSettingsRequest.

    :param fiscal_year_start_month: First month of fiscal year <span
     class='property-internal'>Must be between 1 and 12</span> <span
     class='property-internal'>Required (defined)</span>
    :type fiscal_year_start_month: int
    :param fiscal_year_defined_at_year: Fiscal year reflects the calendar year
     in which it Begins or Ends <span class='property-internal'>One of
     beginning, ending </span> <span class='property-internal'>Required
     (defined)</span>
    :type fiscal_year_defined_at_year: str
    :param calendarization_method: Calendarization method
     Value will be one of "monthly", "user-defined" <span
     class='property-internal'>One of monthly, user-defined </span> <span
     class='property-internal'>Required (defined)</span>
    :type calendarization_method: str
    :param account_periods: List of accounting period names <span
     class='property-internal'>Required (defined)</span>
    :type account_periods: list[~energycap.sdk.models.AccountPeriodRequest]
    """

    _validation = {
        'fiscal_year_start_month': {'maximum': 12, 'minimum': 1},
    }

    _attribute_map = {
        'fiscal_year_start_month': {'key': 'fiscalYearStartMonth', 'type': 'int'},
        'fiscal_year_defined_at_year': {'key': 'fiscalYearDefinedAtYear', 'type': 'str'},
        'calendarization_method': {'key': 'calendarizationMethod', 'type': 'str'},
        'account_periods': {'key': 'accountPeriods', 'type': '[AccountPeriodRequest]'},
    }

    def __init__(self, *, fiscal_year_start_month: int=None, fiscal_year_defined_at_year: str=None, calendarization_method: str=None, account_periods=None, **kwargs) -> None:
        super(AccountingSettingsRequest, self).__init__(**kwargs)
        self.fiscal_year_start_month = fiscal_year_start_month
        self.fiscal_year_defined_at_year = fiscal_year_defined_at_year
        self.calendarization_method = calendarization_method
        self.account_periods = account_periods
