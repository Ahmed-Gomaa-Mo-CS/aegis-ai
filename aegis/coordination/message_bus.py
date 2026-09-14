
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
        # تفريغ قائمة الرسائل بالكامل
        self.messages = []

