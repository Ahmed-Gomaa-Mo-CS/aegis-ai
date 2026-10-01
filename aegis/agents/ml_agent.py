import math
from collections import Counter
from .base_agent import BaseAgent


def char_ngrams(text, n=3):
    t = f" {text.lower()} "
    return [t[i:i + n] for i in range(len(t) - n + 1)]


class MLAgent(BaseAgent):
    """Char-trigram Naive Bayes (pure python). Replace the training source with
    real data (e.g. CIC-IDS2017 features, deepset/prompt-injections) later."""

    def __init__(self, bus=None, train_events=()):
        super().__init__("ML-Agent", bus)
        self.counts = {True: Counter(), False: Counter()}
        self.docs = {True: 0, False: 0}
        self.vocab = set()
        for e in train_events:
            self.fit_one(e["payload"], e["malicious"])

    def fit_one(self, payload, malicious):
        grams = char_ngrams(payload)
        self.counts[malicious].update(grams)
        self.docs[malicious] += 1
        self.vocab.update(grams)

    def p_malicious(self, payload):
        if not self.vocab or min(self.docs.values()) == 0:
            return 0.5
        total_docs = sum(self.docs.values())
        logp = {}
        for label in (True, False):
            denom = sum(self.counts[label].values()) + len(self.vocab)
            lp = math.log(self.docs[label] / total_docs)
            for g in char_ngrams(payload):
                lp += math.log((self.counts[label][g] + 1) / denom)
            logp[label] = lp
        m = max(logp.values())
        e = {k: math.exp(v - m) for k, v in logp.items()}
        return e[True] / (e[True] + e[False])

    def analyze(self, threat):
        p = self.p_malicious(threat.get("payload", ""))
        if p > 0.85:
            return {"decision": "block", "confidence": p}
        if p > 0.5:
            return {"decision": "suspicious", "confidence": p}
        return {"decision": "safe", "confidence": 1 - p}
