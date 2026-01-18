from transformers import pipeline
from functools import lru_cache
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent  # project root
CONFIG_PATH = BASE_DIR / "facehugging" / "config.json"

# Function to load configuration from JSON file
def load_config():
    with open(CONFIG_PATH, "r") as f:
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

@lru_cache(maxsize=1)
def load_model():
    config = load_config()
    return initialize_pipeline(config)
