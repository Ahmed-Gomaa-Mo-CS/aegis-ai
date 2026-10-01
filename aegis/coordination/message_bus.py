<<<<<<< HEAD
class MessageBus:
    """Per-event shared context. Messages carry structured data only."""
=======

class MessageBus:
>>>>>>> 1a004f91eda03eafd4e26b1cf9dbdc33beff3bbb

    def __init__(self):
        self.messages = []

    def broadcast(self, sender, message_type, content):
<<<<<<< HEAD
        self.messages.append({"from": sender, "type": message_type, "content": content})

    def get_messages(self):
        return list(self.messages)

    def clear(self):
        self.messages = []
=======
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

>>>>>>> 1a004f91eda03eafd4e26b1cf9dbdc33beff3bbb
