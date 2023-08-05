# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class PlaceCreate(Model):
    """PlaceCreate.

    All required parameters must be populated in order to send to Azure.

    :param place_code: Required. The place code <span
     class='property-internal'>Required</span> <span
     class='property-internal'>Must be between 0 and 32 characters</span>
    :type place_code: str
    :param place_info: Required. The place info <span
     class='property-internal'>Required</span> <span
     class='property-internal'>Must be between 0 and 50 characters</span>
    :type place_info: str
    :param parent_place_id: Required. The identifier for the parent of the
     place. The parent is the place directly above the current place on the
     buildings and meters tree <span class='property-internal'>Required</span>
     <span class='property-internal'>Topmost (Place)</span>
    :type parent_place_id: int
    :param place_type_id: Required. The identifier for the place type <span
     class='property-internal'>Required</span>
    :type place_type_id: int
    :param primary_use_id: The identifier for the place's primary use
     If this is a building and PrimaryUseId is null this will be set to Unknown
     (PrimaryUseId 55)
    :type primary_use_id: int
    :param build_date: The date and time the place was built
    :type build_date: datetime
    :param address:
    :type address: ~energycap.sdk.models.AddressChild
    :param weather_station_code: The code for the weather station the place is
     assigned to <span class='property-internal'>Must be between 0 and 32
     characters</span>
    :type weather_station_code: str
    :param place_description: A description of the place <span
     class='property-internal'>Must be between 0 and 4000 characters</span>
    :type place_description: str
    """

    _validation = {
        'place_code': {'required': True, 'max_length': 32, 'min_length': 0},
        'place_info': {'required': True, 'max_length': 50, 'min_length': 0},
        'parent_place_id': {'required': True},
        'place_type_id': {'required': True},
        'weather_station_code': {'max_length': 32, 'min_length': 0},
        'place_description': {'max_length': 4000, 'min_length': 0},
    }

    _attribute_map = {
        'place_code': {'key': 'placeCode', 'type': 'str'},
        'place_info': {'key': 'placeInfo', 'type': 'str'},
        'parent_place_id': {'key': 'parentPlaceId', 'type': 'int'},
        'place_type_id': {'key': 'placeTypeId', 'type': 'int'},
        'primary_use_id': {'key': 'primaryUseId', 'type': 'int'},
        'build_date': {'key': 'buildDate', 'type': 'iso-8601'},
        'address': {'key': 'address', 'type': 'AddressChild'},
        'weather_station_code': {'key': 'weatherStationCode', 'type': 'str'},
        'place_description': {'key': 'placeDescription', 'type': 'str'},
    }

    def __init__(self, **kwargs):
        super(PlaceCreate, self).__init__(**kwargs)
        self.place_code = kwargs.get('place_code', None)
        self.place_info = kwargs.get('place_info', None)
        self.parent_place_id = kwargs.get('parent_place_id', None)
        self.place_type_id = kwargs.get('place_type_id', None)
        self.primary_use_id = kwargs.get('primary_use_id', None)
        self.build_date = kwargs.get('build_date', None)
        self.address = kwargs.get('address', None)
        self.weather_station_code = kwargs.get('weather_station_code', None)
        self.place_description = kwargs.get('place_description', None)
