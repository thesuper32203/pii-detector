import uuid

from flask import Flask, request, jsonify

from domain.case_file import create_case_file
from ml.pii_detector import PiiDetector
from uuid import UUID
from db.database_init import SessionLocal, Base, engine
from repositories import case_repository
from repositories.case_repository import CaseRepository

p = PiiDetector()
Base.metadata.create_all(bind=engine)

app = Flask(__name__)
db = SessionLocal()
key = uuid.UUID("2d690795-c2b6-42d7-a7b9-9e7ed9fa180d")

database = CaseRepository(db)

@app.route("/tokenize", methods=["POST"])
def tokenize():
    data = request.get_json()
    user_text = data["text"]
    scored_text = p.detect_and_filter(user_text,0.55)
    tokenized_text, sorted_entities = p.tokenize(entities=scored_text,text=user_text)
    new_case = create_case_file(original_text=user_text,tokenized_text=tokenized_text,entities=sorted_entities, case_id=uuid.uuid4())
    case_key = database.save_case(new_case,mappings=sorted_entities)
    return jsonify({
        "Status": "Success",
        "case_key": case_key,
        "Tokenized_Text": tokenized_text,
    }), 200

@app.route("/detokenize", methods=["GET"])
def detokenize():
    data = request.get_json()
    user_case_id = data["case_id"]
    case = database.find_case(case_id=user_case_id)
    case_mapping = database.find_case_all_mapping(case_id=user_case_id)
    return jsonify({
        "Status": "Success",
        "Case Info": case.tokenized_text,
    })

if __name__ == '__main__':
    app.run()
