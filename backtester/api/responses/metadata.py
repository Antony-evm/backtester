from datetime import datetime, timezone
from pydantic import BaseModel


class Metadata(BaseModel):
    call_time: float
    created_at: str

    @classmethod
    def from_start_time(cls, start_time: datetime) -> "Metadata":
        now = datetime.now(timezone.utc)
        return cls(
            call_time=(now - start_time).total_seconds(),
            created_at=start_time.strftime("%Y-%m-%d %H:%M:%S")
        )
