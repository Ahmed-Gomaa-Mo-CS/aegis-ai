
class EscalationEngine:

    def __init__(self, agents, coordinator, resource_controller):
        self.agents = agents
        self.coordinator = coordinator
        self.resource_controller = resource_controller

    def evaluate(self, threat):

        results = []

        for agent in self.agents:
            if self.resource_controller.allow(agent.name):
                result = agent.analyze(threat)
                results.append((agent.name, result))

        decision = self.coordinator.aggregate(results)

        return decision, results

