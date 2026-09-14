
class AIAgent:

    def __init__(self):
        self.name = "AI-Agent"

    def analyze(self, threat):

        payload = threat.get("payload", "").upper()

        signals = ["IGNORE", "BYPASS", "EXECUTE", "OVERRIDE"]

        score = sum(s in payload for s in signals)

        if score >= 2:
            return {"decision": "block", "confidence": 0.95}

        elif score == 1:
            return {"decision": "suspicious", "confidence": 0.6}

        return {"decision": "safe", "confidence": 0.2}

