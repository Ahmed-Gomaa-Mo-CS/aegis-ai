
from aegis.simulation.attacker import generate_attack
from aegis.agents.ids_agent import IDSAgent
from aegis.agents.ml_agent import MLAgent
from aegis.agents.ai_agent import AIAgent
from aegis.core.escalation_engine import EscalationEngine
from aegis.core.resource_controller import ResourceController
from aegis.coordination.coordinator import Coordinator
from aegis.evaluation.metrics import Metrics


class AegisSystem:

    def __init__(self):

        self.agents = [
            IDSAgent(),
            MLAgent(),
            AIAgent()
        ]

        self.resource_controller = ResourceController()
        self.coordinator = Coordinator()

        self.engine = EscalationEngine(
            agents=self.agents,
            coordinator=self.coordinator,
            resource_controller=self.resource_controller
        )

        self.metrics = Metrics()

    def run_cycle(self):

        threat = generate_attack()
        decision = self.engine.evaluate(threat)

        self.metrics.update(decision)

        print(f"[THREAT] {threat}")
        print(f"[DECISION] {decision}")
        print("-" * 50)

    def run_experiment(self, n=20):

        for _ in range(n):
            self.run_cycle()

        print("\n=== FINAL REPORT ===")
        self.metrics.report()

