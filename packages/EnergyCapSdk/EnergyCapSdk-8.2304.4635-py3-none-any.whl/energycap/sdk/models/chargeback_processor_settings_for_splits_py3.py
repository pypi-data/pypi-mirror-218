# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class ChargebackProcessorSettingsForSplits(Model):
    """ChargebackProcessorSettingsForSplits.

    :param note: Optional note/comment
    :type note: str
    :param batch_settings:
    :type batch_settings: ~energycap.sdk.models.BatchCreate
    """

    _attribute_map = {
        'note': {'key': 'note', 'type': 'str'},
        'batch_settings': {'key': 'batchSettings', 'type': 'BatchCreate'},
    }

    def __init__(self, *, note: str=None, batch_settings=None, **kwargs) -> None:
        super(ChargebackProcessorSettingsForSplits, self).__init__(**kwargs)
        self.note = note
        self.batch_settings = batch_settings
