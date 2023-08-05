# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class ChargebackWorkflowStepEdit(Model):
    """ChargebackWorkflowStepEdit.

    All required parameters must be populated in order to send to Azure.

    :param chargeback_workflow_step_id: Identifier for the chargeback workflow
     step
     If calculateBillWorkflowStepId has a value it will be updated
     If calculateBillWorkflowStepId is null, a new step will be created <span
     class='property-internal'>Required (defined)</span>
    :type chargeback_workflow_step_id: int
    :param chargeback_workflow_step_info: Required. Name given to the
     chargeback workflow step
     Must be unique for a particular type (split or calculation) across all
     workflows <span class='property-internal'>Required</span> <span
     class='property-internal'>Must be between 0 and 64 characters</span>
    :type chargeback_workflow_step_info: str
    :param chargeback_workflow_step_description: Required. Description for the
     chargeback workflow step <span class='property-internal'>Required</span>
     <span class='property-internal'>Must be between 0 and 255
     characters</span>
    :type chargeback_workflow_step_description: str
    :param chargeback_workflow_step_type: The chargeback type that can be
     assign to this chargeback workflow step.
     When editing a step you cannot change the type <span
     class='property-internal'>One of Split, Calculation </span> <span
     class='property-internal'>Required (defined)</span>
    :type chargeback_workflow_step_type: str
    """

    _validation = {
        'chargeback_workflow_step_info': {'required': True, 'max_length': 64, 'min_length': 0},
        'chargeback_workflow_step_description': {'required': True, 'max_length': 255, 'min_length': 0},
    }

    _attribute_map = {
        'chargeback_workflow_step_id': {'key': 'chargebackWorkflowStepId', 'type': 'int'},
        'chargeback_workflow_step_info': {'key': 'chargebackWorkflowStepInfo', 'type': 'str'},
        'chargeback_workflow_step_description': {'key': 'chargebackWorkflowStepDescription', 'type': 'str'},
        'chargeback_workflow_step_type': {'key': 'chargebackWorkflowStepType', 'type': 'str'},
    }

    def __init__(self, **kwargs):
        super(ChargebackWorkflowStepEdit, self).__init__(**kwargs)
        self.chargeback_workflow_step_id = kwargs.get('chargeback_workflow_step_id', None)
        self.chargeback_workflow_step_info = kwargs.get('chargeback_workflow_step_info', None)
        self.chargeback_workflow_step_description = kwargs.get('chargeback_workflow_step_description', None)
        self.chargeback_workflow_step_type = kwargs.get('chargeback_workflow_step_type', None)
