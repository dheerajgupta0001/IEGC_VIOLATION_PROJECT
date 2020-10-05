from typing import TypedDict
import datetime as dt


class IViolationMessageSummary(TypedDict):
    Message: str
    Date: dt.datetime
    Entity1: str
    Schedule1: float
    Drawal1: float
    Deviation1: float