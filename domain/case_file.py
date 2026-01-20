from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


@dataclass
class CaseFile:

    original_text: str
    tokenized_text: str
    entities: list[dict] = field(default_factory=list)

    case_id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.now)
    owner_id: str | None=None

def create_case_file(original_text: str, tokenized_text: str, entities: list[dict], case_id: UUID) -> CaseFile:
    return CaseFile(
        original_text=original_text,
        tokenized_text=tokenized_text,
        entities=entities,
        case_id=case_id,
        owner_id="Anthony"
    )