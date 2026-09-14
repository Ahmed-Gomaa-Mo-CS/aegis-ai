
class EscalationEngine:

    def __init__(self, agents, resource_controller):
        self.agents = agents
        self.resource_controller = resource_controller

    def evaluate(self, threat):

        results = []

        # Step 1: Run all available agents
        for agent in self.agents:

            if self.resource_controller.allow(agent.name):
                result = agent.analyze(threat)
                results.append((agent.name, result))

        # Step 2: Aggregate decisions
        return self._decide(results)

    def _decide(self, results):

        block_score = 0
        monitor_score = 0
        allow_score = 0

        for _, result in results:

            if result["decision"] == "block":
                block_score += result["confidence"]

            elif result["decision"] == "suspicious":
                monitor_score += result["confidence"]

            else:
                allow_score += 1 - result["confidence"]

        if block_score > monitor_score and block_score > allow_score:
            return "BLOCK"

        if monitor_score > 0:
            return "MONITOR"

        return "ALLOW”
