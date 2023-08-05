# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class AccountResponse(Model):
    """AccountResponse.

    :param account_id: The account identifier
    :type account_id: int
    :param account_meter_id: The accountmeter identifier for the account
    :type account_meter_id: int
    :param account_code: The account code
    :type account_code: str
    :param account_info: The account info
    :type account_info: str
    :param account_type:
    :type account_type: ~energycap.sdk.models.AccountTypeChild
    :param cost_center:
    :type cost_center: ~energycap.sdk.models.CostCenterChild
    :param vendor:
    :type vendor: ~energycap.sdk.models.VendorChild
    :param contact:
    :type contact: ~energycap.sdk.models.ContactChild
    :param customer:
    :type customer: ~energycap.sdk.models.CustomerChild
    :param active: Indicates whether the Account is active or inactive
    :type active: bool
    :param accrual_enabled: Indicates if this account is used with accruals
    :type accrual_enabled: bool
    :param address:
    :type address: ~energycap.sdk.models.AddressChild
    :param deposit_paid: The date and time a deposit was paid
    :type deposit_paid: datetime
    :param deposit_return: The date and time the account deposit was returned
    :type deposit_return: datetime
    :param deposit_note: A note related to the account deposit
    :type deposit_note: str
    :param deposit_amount: The account deposit amount
    :type deposit_amount: float
    :param memo: The account memo
    :type memo: str
    :param service_start: The account's service begin date and time
    :type service_start: datetime
    :param service_end: The account's service end date and time
    :type service_end: datetime
    :param account_general_ledger:
    :type account_general_ledger: ~energycap.sdk.models.GeneralLedgerChild
    :param meters: An array of identifiers for meters attached to this account
    :type meters:
     list[~energycap.sdk.models.AccountMeterChildWithSerialNumber]
    :param created_by:
    :type created_by: ~energycap.sdk.models.UserChild
    :param created_date: The date and time the account was created
    :type created_date: datetime
    :param modified_by:
    :type modified_by: ~energycap.sdk.models.UserChild
    :param modified_date: The date and time of the most recent modification
    :type modified_date: datetime
    :param cost_unit:
    :type cost_unit: ~energycap.sdk.models.UnitChild
    :param has_calculated_meter: Indicates whether the Account has a child
     calculated meter
    :type has_calculated_meter: bool
    :param has_split_parent_meter: Indicates whether the Account is a
     recipient of a split
    :type has_split_parent_meter: bool
    :param has_split_child_meter: Indicates whether the Account has a child
     split meter
    :type has_split_child_meter: bool
    :param account_code_history:
    :type account_code_history: ~energycap.sdk.models.AccountCodeHistoryChild
    :param account_description: A description of the account
    :type account_description: str
    :param audit_enabled: When true, bills for this account will be audited
    :type audit_enabled: bool
    :param data_access_release_id: The data access release identifier for this
     Account, null if there is no release.
    :type data_access_release_id: int
    :param data_access_release_approved: Indicates if the DataAccessRelease is
     approved
     null if there is no release
    :type data_access_release_approved: bool
    """

    _attribute_map = {
        'account_id': {'key': 'accountId', 'type': 'int'},
        'account_meter_id': {'key': 'accountMeterId', 'type': 'int'},
        'account_code': {'key': 'accountCode', 'type': 'str'},
        'account_info': {'key': 'accountInfo', 'type': 'str'},
        'account_type': {'key': 'accountType', 'type': 'AccountTypeChild'},
        'cost_center': {'key': 'costCenter', 'type': 'CostCenterChild'},
        'vendor': {'key': 'vendor', 'type': 'VendorChild'},
        'contact': {'key': 'contact', 'type': 'ContactChild'},
        'customer': {'key': 'customer', 'type': 'CustomerChild'},
        'active': {'key': 'active', 'type': 'bool'},
        'accrual_enabled': {'key': 'accrualEnabled', 'type': 'bool'},
        'address': {'key': 'address', 'type': 'AddressChild'},
        'deposit_paid': {'key': 'depositPaid', 'type': 'iso-8601'},
        'deposit_return': {'key': 'depositReturn', 'type': 'iso-8601'},
        'deposit_note': {'key': 'depositNote', 'type': 'str'},
        'deposit_amount': {'key': 'depositAmount', 'type': 'float'},
        'memo': {'key': 'memo', 'type': 'str'},
        'service_start': {'key': 'serviceStart', 'type': 'iso-8601'},
        'service_end': {'key': 'serviceEnd', 'type': 'iso-8601'},
        'account_general_ledger': {'key': 'accountGeneralLedger', 'type': 'GeneralLedgerChild'},
        'meters': {'key': 'meters', 'type': '[AccountMeterChildWithSerialNumber]'},
        'created_by': {'key': 'createdBy', 'type': 'UserChild'},
        'created_date': {'key': 'createdDate', 'type': 'iso-8601'},
        'modified_by': {'key': 'modifiedBy', 'type': 'UserChild'},
        'modified_date': {'key': 'modifiedDate', 'type': 'iso-8601'},
        'cost_unit': {'key': 'costUnit', 'type': 'UnitChild'},
        'has_calculated_meter': {'key': 'hasCalculatedMeter', 'type': 'bool'},
        'has_split_parent_meter': {'key': 'hasSplitParentMeter', 'type': 'bool'},
        'has_split_child_meter': {'key': 'hasSplitChildMeter', 'type': 'bool'},
        'account_code_history': {'key': 'accountCodeHistory', 'type': 'AccountCodeHistoryChild'},
        'account_description': {'key': 'accountDescription', 'type': 'str'},
        'audit_enabled': {'key': 'auditEnabled', 'type': 'bool'},
        'data_access_release_id': {'key': 'dataAccessReleaseId', 'type': 'int'},
        'data_access_release_approved': {'key': 'dataAccessReleaseApproved', 'type': 'bool'},
    }

    def __init__(self, **kwargs):
        super(AccountResponse, self).__init__(**kwargs)
        self.account_id = kwargs.get('account_id', None)
        self.account_meter_id = kwargs.get('account_meter_id', None)
        self.account_code = kwargs.get('account_code', None)
        self.account_info = kwargs.get('account_info', None)
        self.account_type = kwargs.get('account_type', None)
        self.cost_center = kwargs.get('cost_center', None)
        self.vendor = kwargs.get('vendor', None)
        self.contact = kwargs.get('contact', None)
        self.customer = kwargs.get('customer', None)
        self.active = kwargs.get('active', None)
        self.accrual_enabled = kwargs.get('accrual_enabled', None)
        self.address = kwargs.get('address', None)
        self.deposit_paid = kwargs.get('deposit_paid', None)
        self.deposit_return = kwargs.get('deposit_return', None)
        self.deposit_note = kwargs.get('deposit_note', None)
        self.deposit_amount = kwargs.get('deposit_amount', None)
        self.memo = kwargs.get('memo', None)
        self.service_start = kwargs.get('service_start', None)
        self.service_end = kwargs.get('service_end', None)
        self.account_general_ledger = kwargs.get('account_general_ledger', None)
        self.meters = kwargs.get('meters', None)
        self.created_by = kwargs.get('created_by', None)
        self.created_date = kwargs.get('created_date', None)
        self.modified_by = kwargs.get('modified_by', None)
        self.modified_date = kwargs.get('modified_date', None)
        self.cost_unit = kwargs.get('cost_unit', None)
        self.has_calculated_meter = kwargs.get('has_calculated_meter', None)
        self.has_split_parent_meter = kwargs.get('has_split_parent_meter', None)
        self.has_split_child_meter = kwargs.get('has_split_child_meter', None)
        self.account_code_history = kwargs.get('account_code_history', None)
        self.account_description = kwargs.get('account_description', None)
        self.audit_enabled = kwargs.get('audit_enabled', None)
        self.data_access_release_id = kwargs.get('data_access_release_id', None)
        self.data_access_release_approved = kwargs.get('data_access_release_approved', None)
