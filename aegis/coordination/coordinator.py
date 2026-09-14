
class Coordinator:

    def aggregate(self, agent_results):

        scores = {"block": 0, "suspicious": 0, "safe": 0}

        for _, result in agent_results:
            scores[result["decision"]] += result["confidence"]

        if scores["block"] > scores["safe"]:
            return "BLOCK"

        if scores["suspicious"] > 0:
            return "MONITOR"

        return "ALLOW"

