from dataclasses import dataclass
from typing import List, Dict, Optional


@dataclass
class BranchEvent:
    branches: List[str]
    types: Optional[List[str]] = None

    def to_dict(self):
        return {k: v for k, v in self.__dict__.items() if v is not None}


@dataclass
class On:
    pull_request: Optional[BranchEvent] = None
    push: Optional[BranchEvent] = None
    workflow_dispatch: Optional[bool] = False
    repository_dispatch: Optional[Dict[str, str]] = None

    def to_dict(self):
        result = {}

        if self.pull_request is not None:
            result["pull_request"] = self.pull_request.to_dict()

        if self.push is not None:
            result["push"] = self.push.to_dict()

        if self.workflow_dispatch:
            result["workflow_dispatch"] = {}

        return result

    def __getstate__(self):
        return self.to_dict()
