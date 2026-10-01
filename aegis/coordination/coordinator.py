<<<<<<< HEAD
from aegis.coordination.trust_model import TrustModel

LABEL = {"block": "BLOCK", "suspicious": "MONITOR", "safe": "ALLOW"}
SEVERITY = ["block", "suspicious", "safe"]   # tie-break: prefer the safer-for-defence outcome


class Coordinator:
    def __init__(self, trust_decay=0.99, arbiter=None, arbiter_min_conf=0.7):
        self.trust_model = TrustModel(decay=trust_decay)
        self.arbiter = arbiter              # e.g. "LLM-Agent": final word when it ran and is confident
        self.arbiter_min_conf = arbiter_min_conf

    def scores(self, agent_results):
        s = {"block": 0.0, "suspicious": 0.0, "safe": 0.0}
        for name, r in agent_results:
            s[r["decision"]] += r["confidence"] * self.trust_model.get_trust(name)
        return s

    def aggregate(self, agent_results):
        """Trust x confidence weighted vote. No evidence -> MONITOR (fail-safe)."""
        if not agent_results:
            return "MONITOR"
        if self.arbiter:
            for name, r in agent_results:
                if name == self.arbiter and r["confidence"] >= self.arbiter_min_conf:
                    return LABEL[r["decision"]]
        s = self.scores(agent_results)
        top = max(SEVERITY, key=lambda d: (s[d], -SEVERITY.index(d)))
        return LABEL[top]

    def is_decisive(self, agent_results, share, weight):
        """Early-stop test for the cascade: enough evidence AND a dominant class."""
        s = self.scores(agent_results)
        total = sum(s.values())
        return total >= weight and total > 0 and max(s.values()) / total >= share
=======

from aegis.coordination.trust_model import TrustModel


class Coordinator:

    def __init__(self):
        self.trust_model = TrustModel()

    def aggregate(self, agent_results):

        scores = {
            "block": 0,
            "suspicious": 0,
            "safe": 0
        }

        # apply trust-weighting
        for agent_name, result in agent_results:

            trust = self.trust_model.get_trust(agent_name)

            decision = result["decision"]
            confidence = result["confidence"]

            weighted_score = confidence * trust

            scores[decision] += weighted_score

        # final decision
        if scores["block"] > scores["safe"]:
            return "BLOCK"

        if scores["suspicious"] > 0:
            return "MONITOR"

        return "ALLOW"

>>>>>>> 1a004f91eda03eafd4e26b1cf9dbdc33beff3bbb
