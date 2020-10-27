from dataclasses import dataclass
from typing import Dict, List
from datetime import datetime


@dataclass
class CompletedBy:
    def __init__(self): pass
    name: str


@dataclass
class External:
    def __init__(self): pass
    data: str
    gid: str


@dataclass
class TaskToCreate:
    def __init__(self, name, workspace_gid, project_gid, assignee_gid):
        self.name= name
        self.workspace = workspace_gid
        self.projects = [project_gid]
        self.assignee = assignee_gid
    def to_dict(self) ->dict:
        return self.__dict__
    def fillByDefault(self):
        self.completed = False
        self.start_on = str(datetime.now())
        self.due_on = str(datetime(2021, 12, 26, 17, 18, 52, 167840))
    approval_status: str
    assignee: str
    assignee_status: str
    completed: bool
    completed_by: CompletedBy
    custom_fields: Dict[str, str]
    due_at: str
    due_on: str
    external: External
    followers: List[str]
    html_notes: str
    liked: bool
    name: str
    notes: str
    parent: str
    projects: List[str]
    resource_subtype: str
    start_on: str
    tags: List[str]
    workspace: str
