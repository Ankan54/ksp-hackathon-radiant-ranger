from pydantic import BaseModel
from enum import Enum
from datetime import datetime
from typing import Optional


class Sentiment(Enum):
    Positive = "Positive"
    Negative = "Negative"
    Neutral = "Neutral"


class EventType(Enum):
    Accident = 'Accident'
    Violence = 'Violence'
    Riot = 'Riot'


class Severity(Enum):
    High = 'High'
    Medium = 'Medium'
    Low = 'Low'


class Event(BaseModel):
    post_content: str
    event_place: str
    timestamp: datetime
    sentiment: Sentiment
    event_type: EventType
    severity: Severity
    hashtags: Optional[str] = None