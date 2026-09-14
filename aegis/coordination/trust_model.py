
class TrustModel:

    def __init__(self):

        # initial trust (can be tuned)
        self.trust_scores = {
            "IDS-Agent": 0.8,
            "ML-Agent": 0.7,
            "AI-Agent": 0.9
        }

        self.learning_rate = 0.05

    def get_trust(self, agent_name):
        return self.trust_scores.get(agent_name, 0.5)

    def update_trust(self, agent_name, correct):

        current = self.trust_scores.get(agent_name, 0.5)

        if correct:
            current += self.learning_rate
        else:
            current -= self.learning_rate

        # clamp between 0 and 1
        self.trust_scores[agent_name] = max(0.1, min(1.0, current))

    def report(self):

        print("\n=== TRUST SCORES ===")
        for agent, score in self.trust_scores.items():
            print(f"{agent}: {score:.2f}")

