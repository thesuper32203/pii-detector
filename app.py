from datetime import datetime
from flask import Flask, request, jsonify
import json
from transformers import pipeline
from ml.pii_detector import PiiDetector
from domain.case_file import CaseFile,create_case_file
from repositories.case_repository import CaseRepository
import uuid
from db.database_init import SessionLocal, Base, engine
from db import models

p = PiiDetector()
Base.metadata.create_all(bind=engine)

app = Flask(__name__)
db = SessionLocal()
case_state = CaseRepository(db)

texts = [
    "My name is John Doe. Email: john.doe@gmail.com. Phone: (212) 555-0199. My friend Anthony Super's number is (516) 467-7941",
    "My name is Sarah Miller and you can reach me at sarah.miller@outlook.com or call 646-555-8821 after 6 PM.",
    "Please contact Michael Chen via email mchen23@yahoo.com or on his office line (917) 555-4402.",
    "Hi, this is Robert Johnson — my phone number is 718-555-3019 and my backup email is rjohnson.dev@gmail.com.",
    "Emily Davis submitted the form using emily.davis@company.org and listed her mobile as (347) 555-9982.",
    "For verification purposes, Alex Thompson can be reached at alex.thompson1992@gmail.com or by phone at 631-555-7764.",
    "Customer support spoke with Daniel Rodriguez, whose contact email is daniel.rodriguez@icloud.com and phone is 212-555-6631.",
    "Jessica Lee provided two contacts: jess.lee@gmail.com and her work number 516-555-8890.",
    "Please update the record for Kevin Patel — email kevin.patel@protonmail.com, phone (929) 555-1028.",
    "Laura Nguyen prefers email communication at laura.nguyen@fastmail.com but can also be reached at 347-555-4701."
]
# for text in texts:
#     filtered = p.detect_and_filter(text=text,threshold=0.50)
#     tokenized_text, entities = p.tokenize(text=text,entities=filtered)
#
#     print(entities)
#     case = create_case_file(original_text=text,tokenized_text=tokenized_text,entities=entities,case_id=uuid.uuid4())
#     saveCase = CaseRepository(db)
#     caseId = saveCase.save_case(case=case, mappings=filtered)
key = uuid.UUID("25c190f9-54c5-4839-af13-47afc69df990")
found_case = case_state.find_case(case_id=key)
if found_case:
    print("Case found")
    case_entities = case_state.find_case_mapping(case_id=key)
@app.route("/detect", methods=["POST"])
def detect_pii():
    print("hello")
if __name__ == '__main__':
    app.run()
