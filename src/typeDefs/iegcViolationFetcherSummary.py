from typing import TypedDict
import datetime as dt


class IViolationMessageFetcherSummary(TypedDict):
    msgId: str
    date: dt.datetime
    entity: str
    schedule: int
    drawal: int
    deviation: int