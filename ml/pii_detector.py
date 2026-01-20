from ml.model_loader import load_model

class PiiDetector:
    def __init__(self):
        self.pipeline = load_model()

    def detect(self, text):
        return self.pipeline(text)

    def filter_entities(self,entities: list[dict],threshold: float = 0.50) -> list[dict]:
        return [e for e in entities if float(e["score"]) >= threshold]


    def detect_and_filter(self, text: str, threshold: float=0.50) -> list[dict]:
        print("Filtering")
        entities = self.detect(text)
        print("Filter completed")
        return self.filter_entities(entities, threshold)

    def tokenize(self, entities: list[dict],text: str):
        print("Tokenizing")
        # Step 1: assign counters LEFT -> RIGHT (natural order)
        entities_lr = sorted(entities, key=lambda e: e["start"])
        counters = {}

        for e in entities_lr:
            label = e["entity_group"]
            counters[label] = counters.get(label, 0) + 1
            e["token"] = f"{{{{{label}_{counters[label]}}}}}"

            # Step 2: replace RIGHT -> LEFT (preserve indices)
        entities_rl = sorted(entities_lr, key=lambda e: e["start"], reverse=True)

        for e in entities_rl:
            start = int(e["start"])
            end = int(e["end"])
            start, end = clean_span(text, start, end)
            text = text[:start] + e["token"] + text[end:]
        tokenized_text = text
        sorted_entities = entities_rl.copy()
        print("Tokenizing completed")
        return tokenized_text, sorted_entities

def clean_span(text, start, end):
    # Trim leading spaces
    while start < end and text[start].isspace():
        start += 1

    # Trim trailing spaces / punctuation
    while end > start and text[end - 1].isspace():
        end -= 1

    return start, end
