from dataclasses import dataclass
from datetime import datetime


@dataclass
class StudyError:
    subject: str
    topic: str
    error_type: str
    severity: int
    created_at: str = datetime.now().isoformat()
