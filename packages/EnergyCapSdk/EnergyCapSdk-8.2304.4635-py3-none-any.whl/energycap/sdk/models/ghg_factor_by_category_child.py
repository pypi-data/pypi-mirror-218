# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class GHGFactorByCategoryChild(Model):
    """GHGFactorByCategoryChild.

    :param commodity:
    :type commodity: ~energycap.sdk.models.CommodityChild
    :param factor_id: The Factor Identifier
    :type factor_id: int
    :param factor_info: The Factor Info
    :type factor_info: str
    :param factor_description: The Factor Description
    :type factor_description: str
    """

    _attribute_map = {
        'commodity': {'key': 'commodity', 'type': 'CommodityChild'},
        'factor_id': {'key': 'factorId', 'type': 'int'},
        'factor_info': {'key': 'factorInfo', 'type': 'str'},
        'factor_description': {'key': 'factorDescription', 'type': 'str'},
    }

    def __init__(self, **kwargs):
        super(GHGFactorByCategoryChild, self).__init__(**kwargs)
        self.commodity = kwargs.get('commodity', None)
        self.factor_id = kwargs.get('factor_id', None)
        self.factor_info = kwargs.get('factor_info', None)
        self.factor_description = kwargs.get('factor_description', None)
