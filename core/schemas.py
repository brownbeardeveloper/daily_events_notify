from pydantic import BaseModel, Field, model_validator
from typing import Optional
from datetime import datetime, time
import enum


class ScheduleType(enum.Enum):
    ONCE = "once"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"

class BaseEvents(BaseModel):
    id: Optional[int] = None
    message: str
    schedule: ScheduleType
    once: Optional[datetime] = None
    dailytime: Optional[time] = None
    weekly: Optional[int] = Field(None, ge=0, le=6)
    monthly: Optional[int] = Field(None, ge=1, le=31)
    yearly: Optional[str] = Field(None, pattern=r"^\d{2}-\d{2}$")

    @model_validator(mode="after")
    def validate_schedule_fields(self):
        "Validate that the required field is not None"
        required = {
            ScheduleType.ONCE: "once",
            ScheduleType.DAILY: "dailytime",
            ScheduleType.WEEKLY: "weekly",
            ScheduleType.MONTHLY: "monthly",
            ScheduleType.YEARLY: "yearly",
        }
        field = required[self.schedule]
        if getattr(self, field) is None:
            raise ValueError(f"'{field}' is required when schedule is '{self.schedule}'")
        return self
