
class MessageBus:

    def __init__(self):
        self.messages = []

    def broadcast(self, sender, message_type, content):

        msg = {
            "from": sender,
            "type": message_type,
            "content": content
        }

        self.messages.append(msg)

    def get_messages(self):
        return self.messages

    def clear(self):
        self.messages = []

if self.bus:
    self.bus.broadcast(
        self.name,
        "LLM_ANALYSIS",
        f"LLM analyzed payload: {payload}"
    )
