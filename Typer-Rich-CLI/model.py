import datetime
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Todo:
    task: str
    category: str
    date_added: str = field(default_factory=lambda: datetime.datetime.now().isoformat())
    date_completed: Optional[str] = None
    status: int = 1  # 1 = open, 2 = completed
    position: Optional[int] = None

    def __repr__(self) -> str:
        return (
            f"({self.task}, {self.category}, {self.date_added}, "
            f"{self.date_completed}, {self.status}, {self.position})"
        )
