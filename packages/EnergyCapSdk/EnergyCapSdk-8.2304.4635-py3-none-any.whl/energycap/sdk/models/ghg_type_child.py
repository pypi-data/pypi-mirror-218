# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class GHGTypeChild(Model):
    """GHGTypeChild.

    :param ghg_type_id: The identifier for the ghg type
    :type ghg_type_id: int
    :param ghg_type_code: The ghg type code
    :type ghg_type_code: str
    :param ghg_type_info: The ghg type info
    :type ghg_type_info: str
    """

    _attribute_map = {
        'ghg_type_id': {'key': 'ghgTypeId', 'type': 'int'},
        'ghg_type_code': {'key': 'ghgTypeCode', 'type': 'str'},
        'ghg_type_info': {'key': 'ghgTypeInfo', 'type': 'str'},
    }

    def __init__(self, **kwargs):
        super(GHGTypeChild, self).__init__(**kwargs)
        self.ghg_type_id = kwargs.get('ghg_type_id', None)
        self.ghg_type_code = kwargs.get('ghg_type_code', None)
        self.ghg_type_info = kwargs.get('ghg_type_info', None)
