<<<<<<< HEAD
class AgentError(Exception):
    """Raised by an agent when it cannot produce a verdict (timeout, API error...)."""


class BaseAgent:
    """Contract: analyze(threat) -> {"decision": block|suspicious|safe, "confidence": 0..1}.

    `threat` contains ONLY the payload -- never ground truth.
    """

    def __init__(self, name, bus=None):
        self.name = name
        self.bus = bus

    def send_alert(self, message_type, content):
        if self.bus:
            self.bus.broadcast(self.name, message_type, content)

    def analyze(self, threat):
        raise NotImplementedError

    def learn(self, payload, malicious, result):
        """Optional online-learning hook; called only when a label is available."""
=======

class BaseAgent:

    def __init__(self, name, bus=None):
        self.name = name
        self.bus = bus

    def send_alert(self, message_type, content):

        if self.bus:
            self.bus.broadcast(self.name, message_type, content)

    def analyze(self, threat):
        raise NotImplementedError
>>>>>>> 1a004f91eda03eafd4e26b1cf9dbdc33beff3bbb
