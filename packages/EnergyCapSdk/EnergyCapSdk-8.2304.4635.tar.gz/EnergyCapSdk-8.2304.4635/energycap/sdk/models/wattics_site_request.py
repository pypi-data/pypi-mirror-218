# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class WatticsSiteRequest(Model):
    """WatticsSiteRequest.

    :param wattics_site_id: The identifier for a Wattics site
     Set to null to remove the link <span class='property-internal'>Required
     (defined)</span>
    :type wattics_site_id: int
    """

    _attribute_map = {
        'wattics_site_id': {'key': 'watticsSiteId', 'type': 'int'},
    }

    def __init__(self, **kwargs):
        super(WatticsSiteRequest, self).__init__(**kwargs)
        self.wattics_site_id = kwargs.get('wattics_site_id', None)
