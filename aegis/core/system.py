
from aegis.simulation.attacker import generate_attack
from aegis.agents.ids_agent import IDSAgent
from aegis.agents.ml_agent import MLAgent
from aegis.agents.ai_agent import AIAgent
from aegis.agents.llm_agent import LLMAgent
from aegis.core.escalation_engine import EscalationEngine
from aegis.core.resource_controller import ResourceController
from aegis.coordination.coordinator import Coordinator
from aegis.coordination.message_bus import MessageBus
from aegis.evaluation.metrics import Metrics


class AegisSystem:

    def __init__(self, use_llm=True):

        #  communication layer
        self.bus = MessageBus()

        #  agents
        self.agents = [
            IDSAgent(self.bus),
            MLAgent(self.bus),
            AIAgent(self.bus),
        ]
        
        if use_llm:
            self.agents.append(LLMAgent(self.bus))

        self.resource_controller = ResourceController()
        self.coordinator = Coordinator()

        self.engine = EscalationEngine(
            agents=self.agents,
            coordinator=self.coordinator,
            resource_controller=self.resource_controller
        )

        self.metrics = Metrics()

    def run_cycle(self):

        # clear previous messages
        self.bus.clear()

        # generate attack
        threat = generate_attack()

        # run system
        decision, results = self.engine.evaluate(threat)

        # simulated ground truth
        actual_malicious = threat["type"] in ["malware", "ai_attack"]

        # update trust
        for agent_name, result in results:

            predicted_block = result["decision"] == "block"
            correct = (predicted_block == actual_malicious)

            self.coordinator.trust_model.update_trust(agent_name, correct)

        # update metrics
        self.metrics.update(decision)

        # logs
        print(f"[THREAT] {threat}")
        print(f"[MESSAGES] {self.bus.get_messages()}")
        print(f"[DECISION] {decision}")
        print(f"[TRUST] {self.coordinator.trust_model.trust_scores}")
        print("-" * 50)

    def run_experiment(self, n=20):

        for _ in range(n):
            self.run_cycle()

        print("\n=== FINAL REPORT ===")
        self.metrics.report()

        # Trust report
        self.coordinator.trust_model.report()

