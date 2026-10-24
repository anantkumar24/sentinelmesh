
from enum import Enum

from fastapi import FastAPI
from pydantic import BaseModel, Field, IPvAnyAddress, model_validator

app = FastAPI(title="SentinelMesh API")


class EventType(str, Enum):
    LOGIN_SUCCESS = "LOGIN_SUCCESS"
    LOGIN_FAILED = "LOGIN_FAILED"
    ACCESS_DENIED = "ACCESS_DENIED"


class EventStatus(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"
    DENIED = "denied"



class SecurityEvent(BaseModel):
    event_type: EventType
    username: str = Field(min_length=1, max_length=100)
    ip_address: IPvAnyAddress
    status: EventStatus

    @model_validator(mode="after")
    def validate_event_consistency(self):
        expected_status = {
            EventType.LOGIN_SUCCESS: EventStatus.SUCCESS,
            EventType.LOGIN_FAILED: EventStatus.FAILED,
            EventType.ACCESS_DENIED: EventStatus.DENIED,
        }

        if self.status != expected_status[self.event_type]:
            raise ValueError(
                "Event status does not match the event type"
            )

        return self



@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "SentinelMesh"
    }


@app.post("/api/security-events")
def create_security_event(event: SecurityEvent):
    return {
        "message": "Security event validated successfully",
        "event": event
    }
