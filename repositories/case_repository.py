from typing import Any

from sqlalchemy.orm import Session
from db.tables import CaseRow, PiiMappingRow
import uuid

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
                original_value=case.original_text[m.get("start"):m.get("end")],
                score=float(m.get("score")),
                start=m.get("start"),
                end=m.get("end"),
            ))

        self.db.commit()
        return str(case.case_id)


    def find_case(self, case_id: uuid) -> type[CaseFile] | None:
        case = self.db.get(CaseRow, case_id)
        return case

    def find_case_all_mapping(self, case_id: uuid):
        return self.db.query(PiiMappingRow).filter(PiiMappingRow.case_id == case_id).order_by(PiiMappingRow.id).all()
