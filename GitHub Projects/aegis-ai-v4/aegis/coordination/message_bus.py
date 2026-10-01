class MessageBus:
    """Per-event shared context. Messages carry structured data only."""

    def __init__(self):
        self.messages = []

    def broadcast(self, sender, message_type, content):
        self.messages.append({"from": sender, "type": message_type, "content": content})

    def get_messages(self):
        return list(self.messages)

    def clear(self):
        self.messages = []
