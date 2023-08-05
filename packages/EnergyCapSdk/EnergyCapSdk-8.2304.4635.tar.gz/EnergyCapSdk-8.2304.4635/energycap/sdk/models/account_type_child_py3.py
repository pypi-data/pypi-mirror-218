# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class AccountTypeChild(Model):
    """AccountTypeChild.

    :param account_type_id: The account type identifier
    :type account_type_id: int
    :param account_type_code: The account type code
    :type account_type_code: str
    :param account_type_info: The account type info
    :type account_type_info: str
    """

    _attribute_map = {
        'account_type_id': {'key': 'accountTypeId', 'type': 'int'},
        'account_type_code': {'key': 'accountTypeCode', 'type': 'str'},
        'account_type_info': {'key': 'accountTypeInfo', 'type': 'str'},
    }

    def __init__(self, *, account_type_id: int=None, account_type_code: str=None, account_type_info: str=None, **kwargs) -> None:
        super(AccountTypeChild, self).__init__(**kwargs)
        self.account_type_id = account_type_id
        self.account_type_code = account_type_code
        self.account_type_info = account_type_info
