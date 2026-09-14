
def run_cycle(self):

    self.bus.clear()

    threat = generate_attack()

    decision, results = self.engine.evaluate(threat)

    # Ground truth (simulated)
    actual_malicious = threat["type"] in ["malware", "ai_attack"]

    # update trust
    for agent_name, result in results:

        predicted_block = result["decision"] == "block"

        correct = (predicted_block == actual_malicious)

        self.coordinator.trust_model.update_trust(agent_name, correct)

    self.metrics.update(decision)

    print(f"[THREAT] {threat}")
    print(f"[MESSAGES] {self.bus.get_messages()}")
    print(f"[DECISION] {decision}")
    print(f"[TRUST] {self.coordinator.trust_model.trust_scores}")
    print("-" * 50)
