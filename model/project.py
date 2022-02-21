import enum
from enum import Enum
from sys import maxsize


class Project:
    def __init__(self, id=None, name=None, status=None, view_state=None, description=None, inherit_global=None,
                 enabled=True):
        self.id = id
        self.name = name
        self.status = status
        self.inherit_global = inherit_global
        self.view_state = view_state
        self.description = description
        self.enabled = enabled

    view_states = {10: "public", 50: "private"}

    statuses = {10: "development", 30: "release", 50: "stable", 70: "obsolete"}

    def __repr__(self):
        return "%s:::%s_%s_%s_%s_%s" % (self.id, self.name, self.status, self.view_state, self.description, self.enabled)

    def __eq__(self, other):
        return (self.id is None or other.id is None or self.id == other.id) and \
               (self.name == other.name or self.name is None or other.name is None) and \
               (self.status == other.status or self.status is None or other.status is None) and \
               (self.view_state == other.view_state or self.view_state is None or other.view_state is None) and \
               (self.description == other.description or self.description is None or other.description is None) and \
               (self.enabled == other.enabled or self.enabled is None or other.enabled is None)

    def id_or_max(self):
        if self.id:
            return int(self.id)
        else:
            return maxsize
