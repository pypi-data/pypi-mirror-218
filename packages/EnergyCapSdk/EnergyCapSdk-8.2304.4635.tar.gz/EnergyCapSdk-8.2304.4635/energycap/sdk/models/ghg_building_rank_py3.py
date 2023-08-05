# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class GHGBuildingRank(Model):
    """GHGBuildingRank.

    :param place_info:
    :type place_info: ~energycap.sdk.models.PlaceInfo
    :param place_size: The place size
    :type place_size: int
    :param place_size_unit:
    :type place_size_unit: ~energycap.sdk.models.UnitChild
    :param emissions: The overall Greenhouse Gas emissions
    :type emissions: float
    :param scope1_emissions: The Greenhouse Gas emissions from Scope 1
    :type scope1_emissions: float
    :param scope2_emissions: The Greenhouse Gas emissions from Scope 2
    :type scope2_emissions: float
    :param scope3_emissions: The Greenhouse Gas emissions from Scope 3
    :type scope3_emissions: float
    :param emissions_unit:
    :type emissions_unit: ~energycap.sdk.models.UnitChild
    :param intensity: The Greenhouse Gas intensity. Emissions/Place Size
    :type intensity: float
    :param type: The item type
    :type type: str
    :param id: The item identifier
    :type id: int
    :param display: The item display name
    :type display: str
    :param secondary_display: The item formated value
    :type secondary_display: str
    :param value: The item value
    :type value: float
    """

    _attribute_map = {
        'place_info': {'key': 'placeInfo', 'type': 'PlaceInfo'},
        'place_size': {'key': 'placeSize', 'type': 'int'},
        'place_size_unit': {'key': 'placeSizeUnit', 'type': 'UnitChild'},
        'emissions': {'key': 'emissions', 'type': 'float'},
        'scope1_emissions': {'key': 'scope1Emissions', 'type': 'float'},
        'scope2_emissions': {'key': 'scope2Emissions', 'type': 'float'},
        'scope3_emissions': {'key': 'scope3Emissions', 'type': 'float'},
        'emissions_unit': {'key': 'emissionsUnit', 'type': 'UnitChild'},
        'intensity': {'key': 'intensity', 'type': 'float'},
        'type': {'key': 'type', 'type': 'str'},
        'id': {'key': 'id', 'type': 'int'},
        'display': {'key': 'display', 'type': 'str'},
        'secondary_display': {'key': 'secondaryDisplay', 'type': 'str'},
        'value': {'key': 'value', 'type': 'float'},
    }

    def __init__(self, *, place_info=None, place_size: int=None, place_size_unit=None, emissions: float=None, scope1_emissions: float=None, scope2_emissions: float=None, scope3_emissions: float=None, emissions_unit=None, intensity: float=None, type: str=None, id: int=None, display: str=None, secondary_display: str=None, value: float=None, **kwargs) -> None:
        super(GHGBuildingRank, self).__init__(**kwargs)
        self.place_info = place_info
        self.place_size = place_size
        self.place_size_unit = place_size_unit
        self.emissions = emissions
        self.scope1_emissions = scope1_emissions
        self.scope2_emissions = scope2_emissions
        self.scope3_emissions = scope3_emissions
        self.emissions_unit = emissions_unit
        self.intensity = intensity
        self.type = type
        self.id = id
        self.display = display
        self.secondary_display = secondary_display
        self.value = value
