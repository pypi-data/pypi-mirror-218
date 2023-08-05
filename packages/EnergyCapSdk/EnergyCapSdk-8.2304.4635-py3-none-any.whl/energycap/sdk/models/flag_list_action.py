# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class FlagListAction(Model):
    """FlagListAction.

    :param entity_ids: The entities to update <span
     class='property-internal'>Required (defined)</span>
    :type entity_ids: list[int]
    :param flag_action:
    :type flag_action: ~energycap.sdk.models.FlagEdit
    """

    _attribute_map = {
        'entity_ids': {'key': 'entityIds', 'type': '[int]'},
        'flag_action': {'key': 'flagAction', 'type': 'FlagEdit'},
    }

    def __init__(self, **kwargs):
        super(FlagListAction, self).__init__(**kwargs)
        self.entity_ids = kwargs.get('entity_ids', None)
        self.flag_action = kwargs.get('flag_action', None)
