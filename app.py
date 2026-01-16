from flask import Flask, request, jsonify
import json
from transformers import pipeline

app = Flask(__name__)

# Function to load configuration from JSON file
def load_config(config_path):
    with open(config_path, "r") as f:
        return json.load(f)

# Function to initialize the hugging face pipeline
def initialize_pipeline(config):
    tasks = config.get("task","personal-information")
    model = config.get("model")
    tokenizer = config.get("tokenizer", None)
    if tokenizer:
        return pipeline(tasks,model=model,tokenizer=tokenizer)
    return pipeline(tasks,model=model)

config = load_config("config.json")
pii_pipeline = initialize_pipeline(config)



@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
