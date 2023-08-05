# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class DashboardGlobalSettingsEdit(Model):
    """DashboardGlobalSettingsEdit.

    :param show_links: Flag to indicate if public-facing links to the
     application should be displayed <span class='property-internal'>Required
     (defined)</span>
    :type show_links: bool
    :param show_info: Flag to indicate if title/description should be
     displayed <span class='property-internal'>Required (defined)</span>
    :type show_info: bool
    :param global_filter_visibility: Visibility of dashboard filter. Valid
     values are Show, Hide, or Fixed. If settings are applied to a Map
     dashboard, this is automatically set to Fixed, and any other filter
     settings are automatically nulled.
     Show - Filter controls will be show on the dashboard, filter can be
     temporarily set by anybody who can view the dashboard, including public
     viewers.
     Hide - Filter controls will be hidden, manual filtering will be disabled,
     dashboard will be filtered using the topmost place of the user who applies
     the settings
     Fixed - Filter controls will be hidden, dashboard will be filtered using
     the specified Topmost Place or Building Group. PlaceID or PlaceGroupID are
     required when this field is set to Fixed. <span
     class='property-internal'>One of Show, Hide, Fixed </span>
    :type global_filter_visibility: str
    :param place_id: The Identifier for the Topmost Place the dashboard should
     filter by.
     Required when GlobalFilterVisibility is Fixed. Set to null if
     GlobalFilterVisibility is set to Show or Hide.
    :type place_id: int
    :param place_group_id: The Identifier for the Building Group the dashboard
     should filter by.
     Required when GlobalFilterVisibility is Fixed. Set to null if
     GlobalFilterVisibility is set to Show or Hide.
    :type place_group_id: int
    """

    _attribute_map = {
        'show_links': {'key': 'showLinks', 'type': 'bool'},
        'show_info': {'key': 'showInfo', 'type': 'bool'},
        'global_filter_visibility': {'key': 'globalFilterVisibility', 'type': 'str'},
        'place_id': {'key': 'placeId', 'type': 'int'},
        'place_group_id': {'key': 'placeGroupId', 'type': 'int'},
    }

    def __init__(self, **kwargs):
        super(DashboardGlobalSettingsEdit, self).__init__(**kwargs)
        self.show_links = kwargs.get('show_links', None)
        self.show_info = kwargs.get('show_info', None)
        self.global_filter_visibility = kwargs.get('global_filter_visibility', None)
        self.place_id = kwargs.get('place_id', None)
        self.place_group_id = kwargs.get('place_group_id', None)
