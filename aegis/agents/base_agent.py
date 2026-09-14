
class BaseAgent:

    def __init__(self, name, bus=None):
        self.name = name
        self.bus = bus

    def send_alert(self, message_type, content):

        if self.bus:
            self.bus.broadcast(self.name, message_type, content)

    def analyze(self, threat):
        raise NotImplementedError
