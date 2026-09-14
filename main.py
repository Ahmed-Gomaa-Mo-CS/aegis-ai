
from aegis.agents.ai_agent import AIAgent
from aegis.core.escalation_engine import EscalationEngine
from aegis.core.resource_controller import ResourceController
from aegis.simulation.attacker import generate_attack
from aegis.core.system import AegisSystem

def run():

    ai_agent = AIAgent()
    controller = ResourceController()

    engine = EscalationEngine([ai_agent], controller)

    for _ in range(10):
        threat = generate_attack()
        decision = engine.evaluate(threat)

        print(threat, "→", decision)

if __name__ == "__main__":
    run()


if __name__ == "__main__":

    system = AegisSystem()

    system.run_experiment(n=30)
