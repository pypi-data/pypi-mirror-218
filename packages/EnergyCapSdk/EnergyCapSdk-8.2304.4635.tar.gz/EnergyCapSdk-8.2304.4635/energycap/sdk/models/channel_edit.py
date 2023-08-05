# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class ChannelEdit(Model):
    """ChannelEdit.

    All required parameters must be populated in order to send to Azure.

    :param interval_minutes: Required. The interval of the channel. The
     interval is measured in minutes
     Standard intervals are
     15 = FifteenMinute,
     30 = ThirtyMinute,
     60 = Hourly,
     1440 = Daily,
     10080 = Weekly,
     43200 = Monthly <span class='property-internal'>Required</span> <span
     class='property-internal'>Must be between 1 and 2147483647</span>
    :type interval_minutes: int
    :param observation_type_code: Required. The observation type of the
     channel <span class='property-internal'>Required</span>
    :type observation_type_code: str
    :param channel_description: Description of the channel <span
     class='property-internal'>Must be between 0 and 4000 characters</span>
     <span class='property-internal'>Required (defined)</span>
    :type channel_description: str
    :param channel_import_id: The import identifier for the channel. <span
     class='property-internal'>Must be between 0 and 255 characters</span>
     <span class='property-internal'>Required (defined)</span>
    :type channel_import_id: str
    :param channel_version:
    :type channel_version: ~energycap.sdk.models.ChannelVersionRequest
    """

    _validation = {
        'interval_minutes': {'required': True, 'maximum': 2147483647, 'minimum': 1},
        'observation_type_code': {'required': True},
        'channel_description': {'max_length': 4000, 'min_length': 0},
        'channel_import_id': {'max_length': 255, 'min_length': 0},
    }

    _attribute_map = {
        'interval_minutes': {'key': 'intervalMinutes', 'type': 'int'},
        'observation_type_code': {'key': 'observationTypeCode', 'type': 'str'},
        'channel_description': {'key': 'channelDescription', 'type': 'str'},
        'channel_import_id': {'key': 'channelImportId', 'type': 'str'},
        'channel_version': {'key': 'channelVersion', 'type': 'ChannelVersionRequest'},
    }

    def __init__(self, **kwargs):
        super(ChannelEdit, self).__init__(**kwargs)
        self.interval_minutes = kwargs.get('interval_minutes', None)
        self.observation_type_code = kwargs.get('observation_type_code', None)
        self.channel_description = kwargs.get('channel_description', None)
        self.channel_import_id = kwargs.get('channel_import_id', None)
        self.channel_version = kwargs.get('channel_version', None)
