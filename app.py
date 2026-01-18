from flask import Flask, request, jsonify
import json
from transformers import pipeline

app = Flask(__name__)


# Load the config file and initialize the pipeline

text = "My name is John Doe. Email: john.doe@gmail.com. Phone: (212) 555-0199."
results = pii(text)
print(f"Processing: {text}")
print(f"Results: {results}")
shift = 0
filtered = [result for result in results if float(result["score"]) > 0.55]
for r in filtered:
    entity_group = r["entity_group"]
    start = int(r["start"]) + 1
    end = int(r["end"])

    if r["score"] > 0.55:
        text = text[:start+shift] + entity_group +text[end+shift:]
        shift += len(entity_group) - (end - start)
    print(f"Result: {text}")


@app.route("/detect", methods=["POST"])
def detect_pii():
    data = request.json
    text = data.get("text")
    if not text:
        return jsonify({"Error": "No text provided"})
    pii_result = pii(text)




@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
