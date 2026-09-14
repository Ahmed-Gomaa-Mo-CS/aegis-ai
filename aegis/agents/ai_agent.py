
from .base_agent import BaseAgent

class AIAgent(BaseAgent):

    def __init__(self):
        super().__init__("AI-Agent")

    def analyze(self, threat):
        payload = threat.get("payload", "").upper()

        signals = ["IGNORE", "BYPASS", "EXECUTE", "OVERRIDE"]

        score = sum(s in payload for s in signals)

        if score >= 2:
            return {"decision": "block", "confidence": 0.95}
        elif score == 1:
            return {"decision": "suspicious", "confidence": 0.6}
        else:
            return {"decision": "safe", "confidence": 0.2}

