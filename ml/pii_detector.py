
from model_loader import load_model

class PiiDetector:
    def __init__(self):
        self.pipeline = load_model()

    def detect(self, text):
        return self.pipeline(text)

    def filter_entities(self,entities: list[dict],threshold: float = 0.50) -> list[dict]:
        return [e for e in entities if float(e["score"]) >= threshold]

    def detect_and_filter(self, text: str, threshold: float=0.50) -> list[dict]:
        entities = self.detect(text)
        return self.filter_entities(entities, threshold)
