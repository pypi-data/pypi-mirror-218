# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class ReportGroupsClassPermission(Model):
    """ReportGroupsClassPermission.

    :param manage:
    :type manage: bool
    """

    _attribute_map = {
        'manage': {'key': 'manage', 'type': 'bool'},
    }

    def __init__(self, *, manage: bool=None, **kwargs) -> None:
        super(ReportGroupsClassPermission, self).__init__(**kwargs)
        self.manage = manage
