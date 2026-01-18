from flask import Flask, request, jsonify
import json
from transformers import pipeline

app = Flask(__name__)

# Function to load configuration from JSON file
def load_config(config_path):
    with open(config_path, "r") as f:
        return json.load(f)

# Function to initialize the hugging face pipeline
def initialize_pipeline(config_pii):
    tasks = config_pii.get("task", "token-classification")
    model = config_pii.get("model")
    aggregation_strategy = config_pii.get("aggregation_strategy")
    tokenizer = config_pii.get("tokenizer", None)
    if tokenizer:
        return pipeline(tasks,model=model,tokenizer=tokenizer,aggregation_strategy=aggregation_strategy)
    return pipeline(tasks,model=model,aggregation_strategy=aggregation_strategy)

# Load the config file and initialize the pipeline
config = load_config("config.json")
pii = initialize_pipeline(config)
text = "My name is John Doe. Email: john.doe@gmail.com. Phone: (212) 555-0199."
results = pii(text)
for r in results:
    if r["score"] > 0.65:
        #print(f"Token: {r}")
        start = int(json.dumps(r["start"]))
        end = int(json.dumps(r["end"]))
        entity_group = json.dumps(r["entity_group"])
        print(text)
        text = text[:start] + entity_group + text[end:]
        print(text[start:end])
        #print(f"Before tokenization\n {text}")
        #text[start:end] = entity_group
        #print(f"After tokenization\n {text}")
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
