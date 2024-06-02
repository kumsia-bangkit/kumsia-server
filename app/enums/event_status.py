from enum import Enum

class Status(str, Enum):
    DRAFT = "Draft"         # event can be edited
    OPEN = "Open"           # open for registration
    CLOSED = "Closed"       # registration is closed
    CANCELLED = "Cancelled" # an open event is cancelled