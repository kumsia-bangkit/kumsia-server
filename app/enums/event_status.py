from enum import Enum

class Status(str, Enum):
    draft = "draft"         # event can be edited
    submitted = "submitted" # event can't be edited
    open = "open"           # open for registration
    closed = "closed"       # registration is closed