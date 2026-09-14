
from aegis.simulation.attacker import generate_attack
from aegis.agents.ai_agent import AIAgent
from aegis.core.escalation_engine import EscalationEngine
from aegis.core.resource_controller import ResourceController
from aegis.evaluation.metrics import Metrics


class AegisSystem:

    def __init__(self):

        # Initialize components
        self.ai_agent = AIAgent()
        self.resource_controller = ResourceController()

        self.engine = EscalationEngine(
            agents=[self.ai_agent],
            resource_controller=self.resource_controller
        )

        self.metrics = Metrics()

    def run_cycle(self):

        # 1. Generate attack
        threat = generate_attack()

        # 2. Process through system
        decision = self.engine.evaluate(threat)

        # 3. Update metrics
        self.metrics.update(decision)

        # 4. Log result
        print(f"[THREAT] {threat}")
        print(f"[DECISION] {decision}")
        print("-" * 50)

    def run_experiment(self, n=20):

        for _ in range(n):
            self.run_cycle()

        print("\n=== FINAL REPORT ===")
        self.metrics.report() 
