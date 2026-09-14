
from .base_agent import BaseAgent
import random

class MLAgent(BaseAgent):

    def __init__(self, bus):
        super().__init__("ML-Agent", bus)

    def analyze(self, threat):

        messages = self.bus.get_messages() if self.bus else []

        # communication influence
        alert_boost = any(
            msg["type"] == "SECURITY_ALERT"
            for msg in messages
        )

        score = random.random()

        if alert_boost:
            score += 0.2  # shared intelligence effect

        if score > 0.8:
            return {"decision": "block", "confidence": score}

        elif score > 0.5:
            return {"decision": "suspicious", "confidence": score}

        return {"decision": "safe", "confidence": 1 - score}

