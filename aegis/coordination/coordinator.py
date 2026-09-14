
class Coordinator:

    def aggregate(self, agent_results):

        scores = {
            "block": 0,
            "suspicious": 0,
            "safe": 0
        }

        for agent_name, result in agent_results:

            decision = result["decision"]
            confidence = result["confidence"]

            scores[decision] += confidence

        # Decision logic
        if scores["block"] > scores["suspicious"]:
            return "BLOCK"

        if scores["suspicious"] > 0:
            return "MONITOR"

        return "ALLOW"

