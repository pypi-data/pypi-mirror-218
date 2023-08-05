# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class AccountCodeHistoryResponse(Model):
    """AccountCodeHistoryResponse.

    :param account_id: Account identifier <span
     class='property-internal'>Required (defined)</span>
    :type account_id: int
    :param account_code: Account code of the account <span
     class='property-internal'>Required (defined)</span>
    :type account_code: str
    :param account_info: Name of the account <span
     class='property-internal'>Required (defined)</span>
    :type account_info: str
    :param account_code_history:
    :type account_code_history: ~energycap.sdk.models.AccountCodeHistoryChild
    """

    _attribute_map = {
        'account_id': {'key': 'accountId', 'type': 'int'},
        'account_code': {'key': 'accountCode', 'type': 'str'},
        'account_info': {'key': 'accountInfo', 'type': 'str'},
        'account_code_history': {'key': 'accountCodeHistory', 'type': 'AccountCodeHistoryChild'},
    }

    def __init__(self, **kwargs):
        super(AccountCodeHistoryResponse, self).__init__(**kwargs)
        self.account_id = kwargs.get('account_id', None)
        self.account_code = kwargs.get('account_code', None)
        self.account_info = kwargs.get('account_info', None)
        self.account_code_history = kwargs.get('account_code_history', None)
