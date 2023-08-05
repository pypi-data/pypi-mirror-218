# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class SystemSettingsResponse(Model):
    """SystemSettingsResponse.

    :param organization_name: The organization name
    :type organization_name: str
    :param display_organization_name_in_header: Indicates whether or not
     organization name should be displayed in the application header
    :type display_organization_name_in_header: bool
    :param organization_logo: The organization logo
     May be a base64-encoded PNG, JPG, or SVG image or a URI for an image
     hosted online
     A null value will clear the saved image
    :type organization_logo: str
    :param automatic_logout_minutes: Number of minutes after which users will
     be automatically logged out
    :type automatic_logout_minutes: int
    :param default_country: Default country for new users
    :type default_country: str
    :param default_meter_time_zone:
    :type default_meter_time_zone: ~energycap.sdk.models.TimeZoneResponse
    :param default_date_format: Default date format for new users
    :type default_date_format: str
    :param default_topmost_place:
    :type default_topmost_place: ~energycap.sdk.models.PlaceChild
    :param default_cost_center:
    :type default_cost_center: ~energycap.sdk.models.CostCenterChild
    :param default_user_role:
    :type default_user_role: ~energycap.sdk.models.SystemUserRoleChild
    :param months_to_exclude_from_charts: Number of months to exclude from
     powerview charts
    :type months_to_exclude_from_charts: int
    """

    _attribute_map = {
        'organization_name': {'key': 'organizationName', 'type': 'str'},
        'display_organization_name_in_header': {'key': 'displayOrganizationNameInHeader', 'type': 'bool'},
        'organization_logo': {'key': 'organizationLogo', 'type': 'str'},
        'automatic_logout_minutes': {'key': 'automaticLogoutMinutes', 'type': 'int'},
        'default_country': {'key': 'defaultCountry', 'type': 'str'},
        'default_meter_time_zone': {'key': 'defaultMeterTimeZone', 'type': 'TimeZoneResponse'},
        'default_date_format': {'key': 'defaultDateFormat', 'type': 'str'},
        'default_topmost_place': {'key': 'defaultTopmostPlace', 'type': 'PlaceChild'},
        'default_cost_center': {'key': 'defaultCostCenter', 'type': 'CostCenterChild'},
        'default_user_role': {'key': 'defaultUserRole', 'type': 'SystemUserRoleChild'},
        'months_to_exclude_from_charts': {'key': 'monthsToExcludeFromCharts', 'type': 'int'},
    }

    def __init__(self, *, organization_name: str=None, display_organization_name_in_header: bool=None, organization_logo: str=None, automatic_logout_minutes: int=None, default_country: str=None, default_meter_time_zone=None, default_date_format: str=None, default_topmost_place=None, default_cost_center=None, default_user_role=None, months_to_exclude_from_charts: int=None, **kwargs) -> None:
        super(SystemSettingsResponse, self).__init__(**kwargs)
        self.organization_name = organization_name
        self.display_organization_name_in_header = display_organization_name_in_header
        self.organization_logo = organization_logo
        self.automatic_logout_minutes = automatic_logout_minutes
        self.default_country = default_country
        self.default_meter_time_zone = default_meter_time_zone
        self.default_date_format = default_date_format
        self.default_topmost_place = default_topmost_place
        self.default_cost_center = default_cost_center
        self.default_user_role = default_user_role
        self.months_to_exclude_from_charts = months_to_exclude_from_charts
