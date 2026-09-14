
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

