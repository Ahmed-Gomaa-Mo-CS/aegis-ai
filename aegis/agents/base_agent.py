
class BaseAgent:
    def __init__(self, name):
        self.name = name

    def analyze(self, threat):
        raise NotImplementedError
