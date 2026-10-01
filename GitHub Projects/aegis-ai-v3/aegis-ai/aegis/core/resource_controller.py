class ResourceController:
    """Cumulative per-event budget (the old version compared each agent's cost
    to the cap in isolation, so it never restricted anything)."""

    def __init__(self, costs, budget):
        self.costs = costs
        self.budget = budget
        self.spent = 0.0
        self.total_spent = 0.0

    def start_event(self):
        self.spent = 0.0

    def cost(self, name):
        return self.costs.get(name, 1)

    def can_afford(self, name):
        return self.spent + self.cost(name) <= self.budget

    def spend(self, name):
        c = self.cost(name)
        self.spent += c
        self.total_spent += c
