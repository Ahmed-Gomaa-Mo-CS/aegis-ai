import re
from .base_agent import BaseAgent

SIGNATURES = [r"\.exe\b", r"trojan", r"powershell\s+-enc", r"cve-\d{4}-\d+", r"\bexploit\b", r"\bmalware\b"]


class IDSAgent(BaseAgent):
    """Cheap signature matching: fast on known threats, blind to novel ones."""

    def __init__(self, bus=None):
        super().__init__("IDS-Agent", bus)
        self._sigs = [re.compile(s, re.I) for s in SIGNATURES]

    def analyze(self, threat):
        payload = threat.get("payload", "")
        if any(s.search(payload) for s in self._sigs):
            # structured alert only: never forward raw attacker text to other agents
            self.send_alert("SECURITY_ALERT", {"source": self.name, "kind": "signature_match"})
            return {"decision": "block", "confidence": 0.9}
        return {"decision": "safe", "confidence": 0.3}
