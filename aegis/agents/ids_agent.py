
from .base_agent import BaseAgent

class IDSAgent(BaseAgent):

    def __init__(self, bus):
        super().__init__("IDS-Agent", bus)

    def analyze(self, threat):

        payload = threat.get("payload", "").lower()

        if "malware" in payload or "exploit" in payload:

            self.send_alert(
                "SECURITY_ALERT",
                f"IDS detected threat: {payload}"
            )

            return {
                "decision": "block",
                "confidence": 0.9
            }

        return {
            "decision": "safe",
            "confidence": 0.3
        }

