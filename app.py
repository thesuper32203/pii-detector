from flask import Flask, request, jsonify
import json
from transformers import pipeline
from ml.pii_detector import PiiDetector
app = Flask(__name__)
text = "My name is John Doe. Email: john.doe@gmail.com. Phone: (212) 555-0199. My friend Anthony Super's number is (516) 467-7941"
p = PiiDetector()
filtered = p.detect_and_filter(text=text,threshold=0.50)
print(p.tokenize(filtered,text))
@app.route("/detect", methods=["POST"])
def detect_pii():
    print("hello")
if __name__ == '__main__':
    app.run()
