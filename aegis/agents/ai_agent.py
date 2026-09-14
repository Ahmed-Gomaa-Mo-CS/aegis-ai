
from .base_agent import BaseAgent

class AIAgent(BaseAgent):

    def __init__(self, bus):
        super().__init__("AI-Agent", bus)

    def analyze(self, threat):

        messages = self.bus.get_messages() if self.bus else []

        payload = threat.get("payload", "").upper()

        signals = ["IGNORE", "BYPASS", "EXECUTE", "OVERRIDE"]

        score = sum(s in payload for s in signals)

        # communication awareness
        if any(msg["type"] == "SECURITY_ALERT" for msg in messages):
            score += 1

        if score >= 2:
            return {"decision": "block", "confidence": 0.95}

        elif score == 1:
            return {"decision": "suspicious", "confidence": 0.6}

        return {"decision": "safe", "confidence": 0.2}

