from pydantic import BaseModel
from datetime import datetime

class ReservationCreate(BaseModel):
    customer_name: str
    table_id: int
    reservation_time: datetime
    duration_minutes: int

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class ReservationResponse(ReservationCreate):
    id: int
