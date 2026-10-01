<<<<<<< HEAD
class TrustModel:
    """Beta-Bernoulli reliability per agent with exponential forgetting.

    trust = alpha / (alpha + beta). Priors encode initial belief; `strength`
    is the pseudo-count weight of that prior. `decay` < 1 lets the model track
    drifting agent quality (e.g. when attackers shift to novel techniques).
    """

    PRIORS = {"IDS-Agent": 0.8, "ML-Agent": 0.7, "AI-Agent": 0.6, "LLM-Agent": 0.7}

    def __init__(self, decay=0.99, strength=5.0):
        self.decay = decay
        self.ab = {n: [p * strength, (1 - p) * strength] for n, p in self.PRIORS.items()}

    def _get(self, name):
        return self.ab.setdefault(name, [2.5, 2.5])

    def get_trust(self, name):
        a, b = self._get(name)
        return a / (a + b)

    def update_trust(self, name, correct):
        ab = self._get(name)
        ab[0] *= self.decay
        ab[1] *= self.decay
        ab[0 if correct else 1] += 1.0

    @property
    def trust_scores(self):
        return {n: round(self.get_trust(n), 3) for n in self.ab}

    def report(self):
        print("\n=== TRUST SCORES ===")
        for n, s in self.trust_scores.items():
            print(f"{n}: {s:.2f}")
=======

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

>>>>>>> 1a004f91eda03eafd4e26b1cf9dbdc33beff3bbb
