# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class UpdateResult(Model):
    """UpdateResult.

    :param selected:  <span class='property-internal'>Required
     (defined)</span>
    :type selected: int
    :param updated:  <span class='property-internal'>Required (defined)</span>
    :type updated: int
    """

    _attribute_map = {
        'selected': {'key': 'selected', 'type': 'int'},
        'updated': {'key': 'updated', 'type': 'int'},
    }

    def __init__(self, **kwargs):
        super(UpdateResult, self).__init__(**kwargs)
        self.selected = kwargs.get('selected', None)
        self.updated = kwargs.get('updated', None)
