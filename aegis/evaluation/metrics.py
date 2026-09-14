
class Metrics:

    def __init__(self):
        self.total = 0
        self.blocked = 0
        self.monitored = 0
        self.allowed = 0

    def update(self, decision):

        self.total += 1

        if "BLOCK" in decision:
            self.blocked += 1
        elif "MONITOR" in decision:
            self.monitored += 1
        else:
            self.allowed += 1

    def report(self):

        print(f"Total Threats: {self.total}")
        print(f"Blocked: {self.blocked}")
        print(f"Monitored: {self.monitored}")
        print(f"Allowed: {self.allowed}")

        if self.total > 0:
            print(f"Block Rate: {self.blocked/self.total:.2f}")

