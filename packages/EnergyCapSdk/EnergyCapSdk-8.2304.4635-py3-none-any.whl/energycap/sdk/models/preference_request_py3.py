# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class PreferenceRequest(Model):
    """Preferences specific to the logged-in user.

    :param meters_show_inactive:  <span class='property-internal'>Required
     (defined)</span>
    :type meters_show_inactive: bool
    :param show_data_source: Indicates whether or not to show the datasource
     name <span class='property-internal'>Required (defined)</span>
    :type show_data_source: bool
    :param building_tree_display_setting:  <span class='property-internal'>One
     of name, code, namefirst, codefirst </span> <span
     class='property-internal'>Required (defined)</span>
    :type building_tree_display_setting: str
    :param accounts_show_inactive: Indicates whether or not to show inactive
     accounts in the Accounts tree <span class='property-internal'>Required
     (defined)</span>
    :type accounts_show_inactive: bool
    :param cost_center_tree_display_setting: Name/Code display settings for
     the Accounts tree <span class='property-internal'>One of name, code,
     namefirst, codefirst </span> <span class='property-internal'>Required
     (defined)</span>
    :type cost_center_tree_display_setting: str
    :param building_tree_group_to_display:  <span
     class='property-internal'>Required (defined)</span>
    :type building_tree_group_to_display: int
    :param vendor_tree_display_setting:  <span class='property-internal'>One
     of name, code, namefirst, codefirst </span> <span
     class='property-internal'>Required (defined)</span>
    :type vendor_tree_display_setting: str
    :param view_vendors_tree_by_commodity:  <span
     class='property-internal'>Required (defined)</span>
    :type view_vendors_tree_by_commodity: bool
    :param group_display_setting:
    :type group_display_setting: ~energycap.sdk.models.GroupDisplaySetting
    :param bill_list_rows_per_page: Number of rows to display in bill lists
     <span class='property-internal'>Required (defined)</span>
    :type bill_list_rows_per_page: int
    :param date_format: Date format for the user <span
     class='property-internal'>Required (defined)</span>
    :type date_format: str
    :param time_format: Time format for the user <span
     class='property-internal'>Required (defined)</span>
    :type time_format: str
    :param time_zone_code: Code of the default time zone configured for the
     user's owner <span class='property-internal'>Required (defined)</span>
    :type time_zone_code: str
    :param trend_chart_number_of_years: Number of years to display in trend
     charts when the user views them <span class='property-internal'>Required
     (defined)</span>
    :type trend_chart_number_of_years: int
    :param language: User's language preference <span
     class='property-internal'>Required (defined)</span>
    :type language: str
    :param building_and_organization_identifier: Value to use when displaying
     a single building or organization (name or code) <span
     class='property-internal'>Required (defined)</span>
    :type building_and_organization_identifier: str
    :param meter_identifier: Value to use when displaying a single meter (name
     or code) <span class='property-internal'>Required (defined)</span>
    :type meter_identifier: str
    :param account_identifier: Value to use when displaying a single account
     (name or code) <span class='property-internal'>Required (defined)</span>
    :type account_identifier: str
    :param other_identifier: Value to use when displaying generic items (name
     or code) <span class='property-internal'>Required (defined)</span>
    :type other_identifier: str
    :param help_open: Indicates whether or not in-app help is open <span
     class='property-internal'>Required (defined)</span>
    :type help_open: bool
    :param workflow_display_setting:
    :type workflow_display_setting:
     ~energycap.sdk.models.WorkflowDisplaySetting
    """

    _attribute_map = {
        'meters_show_inactive': {'key': 'metersShowInactive', 'type': 'bool'},
        'show_data_source': {'key': 'showDataSource', 'type': 'bool'},
        'building_tree_display_setting': {'key': 'buildingTreeDisplaySetting', 'type': 'str'},
        'accounts_show_inactive': {'key': 'accountsShowInactive', 'type': 'bool'},
        'cost_center_tree_display_setting': {'key': 'costCenterTreeDisplaySetting', 'type': 'str'},
        'building_tree_group_to_display': {'key': 'buildingTreeGroupToDisplay', 'type': 'int'},
        'vendor_tree_display_setting': {'key': 'vendorTreeDisplaySetting', 'type': 'str'},
        'view_vendors_tree_by_commodity': {'key': 'viewVendorsTreeByCommodity', 'type': 'bool'},
        'group_display_setting': {'key': 'groupDisplaySetting', 'type': 'GroupDisplaySetting'},
        'bill_list_rows_per_page': {'key': 'billListRowsPerPage', 'type': 'int'},
        'date_format': {'key': 'dateFormat', 'type': 'str'},
        'time_format': {'key': 'timeFormat', 'type': 'str'},
        'time_zone_code': {'key': 'timeZoneCode', 'type': 'str'},
        'trend_chart_number_of_years': {'key': 'trendChartNumberOfYears', 'type': 'int'},
        'language': {'key': 'language', 'type': 'str'},
        'building_and_organization_identifier': {'key': 'buildingAndOrganizationIdentifier', 'type': 'str'},
        'meter_identifier': {'key': 'meterIdentifier', 'type': 'str'},
        'account_identifier': {'key': 'accountIdentifier', 'type': 'str'},
        'other_identifier': {'key': 'otherIdentifier', 'type': 'str'},
        'help_open': {'key': 'helpOpen', 'type': 'bool'},
        'workflow_display_setting': {'key': 'workflowDisplaySetting', 'type': 'WorkflowDisplaySetting'},
    }

    def __init__(self, *, meters_show_inactive: bool=None, show_data_source: bool=None, building_tree_display_setting: str=None, accounts_show_inactive: bool=None, cost_center_tree_display_setting: str=None, building_tree_group_to_display: int=None, vendor_tree_display_setting: str=None, view_vendors_tree_by_commodity: bool=None, group_display_setting=None, bill_list_rows_per_page: int=None, date_format: str=None, time_format: str=None, time_zone_code: str=None, trend_chart_number_of_years: int=None, language: str=None, building_and_organization_identifier: str=None, meter_identifier: str=None, account_identifier: str=None, other_identifier: str=None, help_open: bool=None, workflow_display_setting=None, **kwargs) -> None:
        super(PreferenceRequest, self).__init__(**kwargs)
        self.meters_show_inactive = meters_show_inactive
        self.show_data_source = show_data_source
        self.building_tree_display_setting = building_tree_display_setting
        self.accounts_show_inactive = accounts_show_inactive
        self.cost_center_tree_display_setting = cost_center_tree_display_setting
        self.building_tree_group_to_display = building_tree_group_to_display
        self.vendor_tree_display_setting = vendor_tree_display_setting
        self.view_vendors_tree_by_commodity = view_vendors_tree_by_commodity
        self.group_display_setting = group_display_setting
        self.bill_list_rows_per_page = bill_list_rows_per_page
        self.date_format = date_format
        self.time_format = time_format
        self.time_zone_code = time_zone_code
        self.trend_chart_number_of_years = trend_chart_number_of_years
        self.language = language
        self.building_and_organization_identifier = building_and_organization_identifier
        self.meter_identifier = meter_identifier
        self.account_identifier = account_identifier
        self.other_identifier = other_identifier
        self.help_open = help_open
        self.workflow_display_setting = workflow_display_setting
