# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class ItemRankResponse(Model):
    """ItemRankResponse.

    :param type: The item type
    :type type: str
    :param id: The item identifier
    :type id: int
    :param display: The item display name
    :type display: str
    :param secondary_display: The item formated value
    :type secondary_display: str
    :param value: The item value
    :type value: float
    """

    _attribute_map = {
        'type': {'key': 'type', 'type': 'str'},
        'id': {'key': 'id', 'type': 'int'},
        'display': {'key': 'display', 'type': 'str'},
        'secondary_display': {'key': 'secondaryDisplay', 'type': 'str'},
        'value': {'key': 'value', 'type': 'float'},
    }

    def __init__(self, **kwargs):
        super(ItemRankResponse, self).__init__(**kwargs)
        self.type = kwargs.get('type', None)
        self.id = kwargs.get('id', None)
        self.display = kwargs.get('display', None)
        self.secondary_display = kwargs.get('secondary_display', None)
        self.value = kwargs.get('value', None)
