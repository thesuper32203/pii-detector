from sqlalchemy.orm import Session
from db.models import CaseRow, PiiMappingRow
from domain.case_file import CaseFile

class CaseRepository:
    def __init__(self, db: Session):
        self.db = db

    def save_case(self, case: CaseFile, mappings: list[dict]) -> str:
        case_row = CaseRow(
            id=case.case_id,
            owner_id=case.owner_id,
            original_text=case.original_text,
            tokenized_text=case.tokenized_text,
        )
        self.db.add(case_row)

        for m in mappings:
            self.db.add(PiiMappingRow(
                case_id=case.case_id,
                token=m["token"],
                entity_type=m["entity_group"],
                original_value=m["value"],
                score=m.get("score"),
                start=m.get("start"),
                end=m.get("end"),
            ))

        self.db.commit()
        return str(case.case_id)