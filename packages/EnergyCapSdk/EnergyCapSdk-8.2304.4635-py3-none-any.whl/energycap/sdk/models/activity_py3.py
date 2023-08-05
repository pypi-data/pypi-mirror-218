# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class Activity(Model):
    """Activity.

    :param id:
    :type id: int
    :param reason:
    :type reason: str
    """

    _attribute_map = {
        'id': {'key': 'id', 'type': 'int'},
        'reason': {'key': 'reason', 'type': 'str'},
    }

    def __init__(self, *, id: int=None, reason: str=None, **kwargs) -> None:
        super(Activity, self).__init__(**kwargs)
        self.id = id
        self.reason = reason
