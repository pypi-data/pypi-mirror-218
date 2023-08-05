# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class GHGFactorCategory(Model):
    """GHGFactorCategory.

    :param factor_category_id: The Factor Category identifier
    :type factor_category_id: int
    :param factor_category_info: The Factor Category Info
    :type factor_category_info: str
    """

    _attribute_map = {
        'factor_category_id': {'key': 'factorCategoryId', 'type': 'int'},
        'factor_category_info': {'key': 'factorCategoryInfo', 'type': 'str'},
    }

    def __init__(self, **kwargs):
        super(GHGFactorCategory, self).__init__(**kwargs)
        self.factor_category_id = kwargs.get('factor_category_id', None)
        self.factor_category_info = kwargs.get('factor_category_info', None)
