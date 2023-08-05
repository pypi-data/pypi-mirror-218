# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class BillSplitDetailsResponse(Model):
    """Details of the bill split
    FixedPercentageSplit, FloorAreaSplit, and DynamicPercentageSplit are
    mutually exclusive
    Only 1 of these properties will have a value.

    :param version:
    :type version: ~energycap.sdk.models.DistributionVersionResponse
    :param fixed_percentage_split: Populate if setting up a fixed percentage
     split.
    :type fixed_percentage_split:
     list[~energycap.sdk.models.FixedPercentageResponse]
    :param floor_area_split: Populate if setting up a dynamic percentage split
     based on the building floor area with weighting factor applied.
    :type floor_area_split: list[~energycap.sdk.models.FloorAreaSplitResponse]
    :param dynamic_percentage_split:
    :type dynamic_percentage_split:
     ~energycap.sdk.models.DynamicPercentageBillSplitResponse
    """

    _attribute_map = {
        'version': {'key': 'version', 'type': 'DistributionVersionResponse'},
        'fixed_percentage_split': {'key': 'fixedPercentageSplit', 'type': '[FixedPercentageResponse]'},
        'floor_area_split': {'key': 'floorAreaSplit', 'type': '[FloorAreaSplitResponse]'},
        'dynamic_percentage_split': {'key': 'dynamicPercentageSplit', 'type': 'DynamicPercentageBillSplitResponse'},
    }

    def __init__(self, *, version=None, fixed_percentage_split=None, floor_area_split=None, dynamic_percentage_split=None, **kwargs) -> None:
        super(BillSplitDetailsResponse, self).__init__(**kwargs)
        self.version = version
        self.fixed_percentage_split = fixed_percentage_split
        self.floor_area_split = floor_area_split
        self.dynamic_percentage_split = dynamic_percentage_split
