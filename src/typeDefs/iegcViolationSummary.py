from typing import TypedDict
import datetime as dt


class IViolationMessageSummary(TypedDict):
    StartDate: dt.datetime
    EndDate: dt.datetime
    corridor: str
    seasonAntecedent: str
    description: str