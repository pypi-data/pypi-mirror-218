from dataclasses import dataclass
from typing import List, Any

@dataclass
class WorkflowDispatchInputs:
    description: str = "self-descriptive"
    required: bool = False
    default: Any
    type: str = "environment"
    options: List[Any]

    def to_dict(self):
        result = {}
        for attr, value in vars(self).items():
            if value is not None:
                result[attr] = value
        return result

@dataclass
class WorkflowDispatch:
    inputs: List[WorkflowDispatchInputs]

    def to_dict(self):
        return [item.to_dict() for item in self.inputs]

    