from db.database_init import SessionLocal
from db.tables import PiiMappingRow
from repositories.case_repository import CaseRepository
from uuid import UUID
import re

db = SessionLocal()
case_state = CaseRepository(db)


def get_case_file_and_entities(case_id: UUID):

    case = case_state.find_case(case_id=case_id)

    if case:
        mapping = case_state.find_case_all_mapping(case_id=case_id)
        if not mapping:
            mapping.append(["No mappings found"])
    else:
        return "Case not found"

    return case, mapping

def detokenize_case(tokenized_text: str,mappings: list[PiiMappingRow]):
    TOKEN_RE = re.compile(r"\{\{[A-Z0-9_]+_\d+\}\}")
    token_to_value = {
        m.token:m.original_value
        for m in mappings
    }
    def repl(match):
        token = match.group(0)
        return token_to_value.get(token)
    return TOKEN_RE.sub(repl, tokenized_text)
