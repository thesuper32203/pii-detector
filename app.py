from datetime import datetime
from flask import Flask, request, jsonify
import json
from transformers import pipeline
from ml.pii_detector import PiiDetector
from domain.case_file import CaseFile
from repositories.case_repository import CaseRepository
import uuid
from db.database_init import SessionLocal, Base, engine
from db import models
Base.metadata.create_all(bind=engine)

app = Flask(__name__)
db = SessionLocal()

text = "My name is John Doe. Email: john.doe@gmail.com. Phone: (212) 555-0199. My friend Anthony Super's number is (516) 467-7941"
p = PiiDetector()
filtered = p.detect_and_filter(text=text,threshold=0.50)
tokenized_text, entities = p.tokenize(text=text,entities=filtered)

case = CaseFile(
    original_text=text,
    tokenized_text=tokenized_text,
    entities=entities,case_id=uuid.uuid4(),
    created_at=datetime.now(),
    owner_id="Anthony"
)
saveCase = CaseRepository(db)
caseId = saveCase.save_case(case=case, mappings=filtered)



@app.route("/detect", methods=["POST"])
def detect_pii():
    print("hello")
if __name__ == '__main__':
    app.run()
