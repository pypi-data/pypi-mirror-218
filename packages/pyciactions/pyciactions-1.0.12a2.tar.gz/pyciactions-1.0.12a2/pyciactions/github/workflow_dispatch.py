from dataclasses import dataclass, field
from typing import List, Any, Union

@dataclass
class WorkflowDispatchInputs:
    description: str = "self-descriptive"
    required: bool = False
    default_: Union[str, bool, int] = None
    type: str = "environment"
    options: list = field(default_factory=list)

    def to_dict(self):
        result = {}
        for attr, value in vars(self).items():
            if value is not None:
                if attr == "default_":
                    result["default"] = value
                else:
                    result[attr] = value
        return result

@dataclass
class WorkflowDispatch:
    inputs: List[WorkflowDispatchInputs] = []

    def to_dict(self):
        return [item.to_dict() for item in self.inputs]

    