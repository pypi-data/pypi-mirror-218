# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class GHGFactorVersionHistoryResponse(Model):
    """GHGFactorVersionHistoryResponse.

    :param factor_id: Identifier for the factor
    :type factor_id: str
    :param factor_info: Name of the factor
    :type factor_info: str
    :param factor_description: Description of the factor
    :type factor_description: str
    :param factor_unit:
    :type factor_unit: ~energycap.sdk.models.UnitChild
    :param factor_co2_eunit:
    :type factor_co2_eunit: ~energycap.sdk.models.UnitChild
    :param commodity_unit:
    :type commodity_unit: ~energycap.sdk.models.UnitChild
    :param commodity:
    :type commodity: ~energycap.sdk.models.CommodityChild
    :param factor_category:
    :type factor_category: ~energycap.sdk.models.GHGFactorCategory
    :param versions: List of versions
    :type versions: list[~energycap.sdk.models.GHGVersion]
    """

    _attribute_map = {
        'factor_id': {'key': 'factorId', 'type': 'str'},
        'factor_info': {'key': 'factorInfo', 'type': 'str'},
        'factor_description': {'key': 'factorDescription', 'type': 'str'},
        'factor_unit': {'key': 'factorUnit', 'type': 'UnitChild'},
        'factor_co2_eunit': {'key': 'factorCO2EUnit', 'type': 'UnitChild'},
        'commodity_unit': {'key': 'commodityUnit', 'type': 'UnitChild'},
        'commodity': {'key': 'commodity', 'type': 'CommodityChild'},
        'factor_category': {'key': 'factorCategory', 'type': 'GHGFactorCategory'},
        'versions': {'key': 'versions', 'type': '[GHGVersion]'},
    }

    def __init__(self, *, factor_id: str=None, factor_info: str=None, factor_description: str=None, factor_unit=None, factor_co2_eunit=None, commodity_unit=None, commodity=None, factor_category=None, versions=None, **kwargs) -> None:
        super(GHGFactorVersionHistoryResponse, self).__init__(**kwargs)
        self.factor_id = factor_id
        self.factor_info = factor_info
        self.factor_description = factor_description
        self.factor_unit = factor_unit
        self.factor_co2_eunit = factor_co2_eunit
        self.commodity_unit = commodity_unit
        self.commodity = commodity
        self.factor_category = factor_category
        self.versions = versions
