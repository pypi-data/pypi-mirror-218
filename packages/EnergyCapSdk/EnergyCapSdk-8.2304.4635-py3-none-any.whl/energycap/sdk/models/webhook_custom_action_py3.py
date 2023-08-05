# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class WebhookCustomAction(Model):
    """DTO for Custom Actions.

    All required parameters must be populated in order to send to Azure.

    :param ids: The list of ids on which to perform the custom action <span
     class='property-internal'>Cannot be Empty</span> <span
     class='property-internal'>Required (defined)</span>
    :type ids: list[int]
    :param webhook_id: Required. The webhook identifier that represents the
     custom action <span class='property-internal'>Required</span>
    :type webhook_id: int
    """

    _validation = {
        'webhook_id': {'required': True},
    }

    _attribute_map = {
        'ids': {'key': 'ids', 'type': '[int]'},
        'webhook_id': {'key': 'webhookId', 'type': 'int'},
    }

    def __init__(self, *, webhook_id: int, ids=None, **kwargs) -> None:
        super(WebhookCustomAction, self).__init__(**kwargs)
        self.ids = ids
        self.webhook_id = webhook_id
