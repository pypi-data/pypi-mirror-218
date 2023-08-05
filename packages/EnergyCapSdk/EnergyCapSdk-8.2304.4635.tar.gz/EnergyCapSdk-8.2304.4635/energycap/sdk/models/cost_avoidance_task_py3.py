# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class CostAvoidanceTask(Model):
    """CostAvoidanceTask.

    :param has_attachments: Indicates whether or not the task has an output
     log available for download
    :type has_attachments: bool
    :param cost_avoidance_task_id: The task ID
    :type cost_avoidance_task_id: int
    :param task_gu_id: The task GUID
    :type task_gu_id: str
    :param task_type:
    :type task_type: ~energycap.sdk.models.TaskType
    :param begin_date: The date and time the task began
    :type begin_date: datetime
    :param end_date: The date and time the task finished. If the task is not
     finished, endDate will have no value
    :type end_date: datetime
    :param user:
    :type user: ~energycap.sdk.models.UserChild
    :param settings:
    :type settings: ~energycap.sdk.models.CostAvoidanceSettings
    :param filters: The task's filters
    :type filters: list[~energycap.sdk.models.FilterResponse]
    :param message: If there was a catastrophic error during task processing,
     it will go here
    :type message: str
    :param reason: The reason for the cost avoidance task. Will be one of the
     following:
     * ResetBaseline
     * SavedAndReprocessedMeter
     * ProcessSavings
     * SpecialAdjustmentAddedEditedRemoved
     * SpecialAdjustmentAddedEditedRemovedSetupSheet
     * MeterCostAvoidanceSettingsGloballyUpdated
     * AucRangeModified
     * OtherSavingsAddedEdited
     * OtherSavingsAddedEditedSetupSheet
    :type reason: str
    :param status: The status of the cost avoidance task. Will be one of the
     following:
     * Processing
     * Complete
     * Error
    :type status: str
    :param task_note: Notes added to the cost avoidance task by the user
    :type task_note: str
    :param baseline_log:
    :type baseline_log: ~energycap.sdk.models.BaselineLog
    :param savings_log:
    :type savings_log: ~energycap.sdk.models.SavingsLog
    """

    _attribute_map = {
        'has_attachments': {'key': 'hasAttachments', 'type': 'bool'},
        'cost_avoidance_task_id': {'key': 'costAvoidanceTaskId', 'type': 'int'},
        'task_gu_id': {'key': 'taskGUId', 'type': 'str'},
        'task_type': {'key': 'taskType', 'type': 'TaskType'},
        'begin_date': {'key': 'beginDate', 'type': 'iso-8601'},
        'end_date': {'key': 'endDate', 'type': 'iso-8601'},
        'user': {'key': 'user', 'type': 'UserChild'},
        'settings': {'key': 'settings', 'type': 'CostAvoidanceSettings'},
        'filters': {'key': 'filters', 'type': '[FilterResponse]'},
        'message': {'key': 'message', 'type': 'str'},
        'reason': {'key': 'reason', 'type': 'str'},
        'status': {'key': 'status', 'type': 'str'},
        'task_note': {'key': 'taskNote', 'type': 'str'},
        'baseline_log': {'key': 'baselineLog', 'type': 'BaselineLog'},
        'savings_log': {'key': 'savingsLog', 'type': 'SavingsLog'},
    }

    def __init__(self, *, has_attachments: bool=None, cost_avoidance_task_id: int=None, task_gu_id: str=None, task_type=None, begin_date=None, end_date=None, user=None, settings=None, filters=None, message: str=None, reason: str=None, status: str=None, task_note: str=None, baseline_log=None, savings_log=None, **kwargs) -> None:
        super(CostAvoidanceTask, self).__init__(**kwargs)
        self.has_attachments = has_attachments
        self.cost_avoidance_task_id = cost_avoidance_task_id
        self.task_gu_id = task_gu_id
        self.task_type = task_type
        self.begin_date = begin_date
        self.end_date = end_date
        self.user = user
        self.settings = settings
        self.filters = filters
        self.message = message
        self.reason = reason
        self.status = status
        self.task_note = task_note
        self.baseline_log = baseline_log
        self.savings_log = savings_log
