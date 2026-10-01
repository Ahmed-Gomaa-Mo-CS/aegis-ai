import math
from collections import Counter
from .base_agent import BaseAgent
from .calibration import OnlineCalibrator


def char_ngrams(text, n=3):
    t = f" {text.lower()} "
    return [t[i:i + n] for i in range(len(t) - n + 1)]


class MLAgent(BaseAgent):
    """Char-trigram Naive Bayes (pure python). Replace the training source with
    real data (e.g. CIC-IDS2017 features, deepset/prompt-injections) later."""

    def __init__(self, bus=None, train_events=(), calibrate=False, novelty_penalty=0.0):
        super().__init__("ML-Agent", bus)
        self.calibrator = OnlineCalibrator() if calibrate else None
        self.novelty_penalty = novelty_penalty
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

    def learn(self, payload, malicious, result):
        if self.calibrator:
            self.calibrator.update(self.p_malicious(payload), malicious)

    def novelty(self, payload):
        """Share of the input's trigrams never seen in training (cheap OOD signal)."""
        g = char_ngrams(payload)
        return sum(x not in self.vocab for x in g) / len(g) if g and self.vocab else 0.0

    def analyze(self, threat):
        """Decision from the raw score; calibration only rescales the *confidence*
        (how much the cascade/vote should trust this verdict)."""
        raw = self.p_malicious(threat.get("payload", ""))
        decision = "block" if raw > 0.85 else "suspicious" if raw > 0.5 else "safe"
        p = self.calibrator.calibrate(raw) if self.calibrator else raw
        if decision == "safe":
            conf = 1 - p
        else:
            conf = p
        conf *= 1.0 - self.novelty_penalty * self.novelty(threat.get("payload", ""))
        return {"decision": decision, "confidence": max(0.0, min(1.0, conf))}
