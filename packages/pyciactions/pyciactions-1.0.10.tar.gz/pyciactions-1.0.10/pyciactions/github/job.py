from dataclasses import dataclass
from typing import List, Dict, Optional, Union, Any


@dataclass
class Step:
    name: str
    uses: Optional[str] = None
    run: Optional[Union[str, List[str]]] = None
    working_directory: Optional[str] = None
    shell: Optional[str] = None
    with_: Optional[Dict[str, Any]] = None
    if_: Optional[str] = None
    id: Optional[str] = None
    env: Optional[Dict[str, Any]] = None

    def to_dict(self):
        result = {"name": self.name}
        for attr, value in vars(self).items():
            if value is not None:
                if attr == "with_":
                    result["with"] = value
                else:
                    result[attr] = value
        return result

    def __getstate__(self):
        return self.to_dict()


@dataclass
class Job:
    id: str
    runs_on: str
    steps: List[Step]
    needs: Optional[List[str]] = None
    if_: Optional[str] = None

    def to_dict(self):
        result = {"steps": [step.to_dict() for step in self.steps]}
        for attr, value in vars(self).items():
            if attr in ["steps"]:
                continue

            if value is not None:
                if attr == "if_":
                    result["if"] = value
                else:
                    result[attr] = value
        return result

    def __getstate__(self):
        return self.to_dict()
