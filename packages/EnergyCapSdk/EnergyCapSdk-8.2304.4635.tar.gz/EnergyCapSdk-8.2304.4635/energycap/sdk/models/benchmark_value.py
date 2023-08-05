# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class BenchmarkValue(Model):
    """BenchmarkValue.

    :param benchmark_value_id: Indicator for which benchmark factor <span
     class='property-internal'>Required (defined)</span>
    :type benchmark_value_id: int
    :param effective_date: Effective Date for the benchmark factor <span
     class='property-internal'>Required (defined)</span>
    :type effective_date: datetime
    :param end_date: End Date for the benchmark factor <span
     class='property-internal'>Required (defined)</span>
    :type end_date: datetime
    :param value: Value set for the benchmark factor <span
     class='property-internal'>Required (defined)</span>
    :type value: float
    """

    _attribute_map = {
        'benchmark_value_id': {'key': 'benchmarkValueId', 'type': 'int'},
        'effective_date': {'key': 'effectiveDate', 'type': 'iso-8601'},
        'end_date': {'key': 'endDate', 'type': 'iso-8601'},
        'value': {'key': 'value', 'type': 'float'},
    }

    def __init__(self, **kwargs):
        super(BenchmarkValue, self).__init__(**kwargs)
        self.benchmark_value_id = kwargs.get('benchmark_value_id', None)
        self.effective_date = kwargs.get('effective_date', None)
        self.end_date = kwargs.get('end_date', None)
        self.value = kwargs.get('value', None)
