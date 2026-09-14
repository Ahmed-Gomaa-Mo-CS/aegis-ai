
class IDSAgent:

    def __init__(self):
        self.name = "IDS-Agent"

    def analyze(self, threat):

        payload = threat.get("payload", "").lower()

        signatures = ["trojan", "malware", "exploit"]

        if any(sig in payload for sig in signatures):
            return {
                "decision": "block",
                "confidence": 0.9
            }

        return {
            "decision": "safe",
            "confidence": 0.3
        }
