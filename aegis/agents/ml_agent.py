
import random

class MLAgent:

    def __init__(self):
        self.name = "ML-Agent"

    def analyze(self, threat):

        score = random.random()

        if score > 0.8:
            return {
                "decision": "block",
                "confidence": score
            }

        elif score > 0.5:
            return {
                "decision": "suspicious",
                "confidence": score
            }

        return {
            "decision": "safe",
            "confidence": 1 - score
        }

