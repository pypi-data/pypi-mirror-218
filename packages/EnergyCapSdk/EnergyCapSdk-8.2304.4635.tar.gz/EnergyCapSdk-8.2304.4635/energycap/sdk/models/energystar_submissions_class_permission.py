# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class ENERGYSTARSubmissionsClassPermission(Model):
    """ENERGYSTARSubmissionsClassPermission.

    :param run:
    :type run: bool
    :param manage:
    :type manage: bool
    """

    _attribute_map = {
        'run': {'key': 'run', 'type': 'bool'},
        'manage': {'key': 'manage', 'type': 'bool'},
    }

    def __init__(self, **kwargs):
        super(ENERGYSTARSubmissionsClassPermission, self).__init__(**kwargs)
        self.run = kwargs.get('run', None)
        self.manage = kwargs.get('manage', None)
