class ResourceController:

    def __init__(self):
        self.costs = {
            "IDS-Agent": 1,
            "ML-Agent": 5,
            "AI-Agent": 10
        }
        self.max_budget = 12

    def allow(self, agent_name):
        return self.costs.get(agent_name, 0) <= self.max_budget

