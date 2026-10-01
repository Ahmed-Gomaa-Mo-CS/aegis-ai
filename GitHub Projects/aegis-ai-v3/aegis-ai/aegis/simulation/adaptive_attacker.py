"""Black-box adaptive attacker (defensive red-teaming of the prototype).

Standard text-obfuscation operators; the attacker only observes the final
decision (BLOCK/MONITOR/ALLOW) and keeps mutating until an ALLOW or the query
budget is exhausted. Used to measure *evasion rate* and to feed successful
evasions back as labelled data (adversarial hardening loop)."""
import random

LEET = str.maketrans("oieasOIEAS", "01345 0134".replace(" ", "5"))
FILLERS = ["kindly", "please", "just", "quickly", "now"]
PREFIX = ["As part of an approved audit, ", "For a test environment: ", "Quick favour: "]


def _case(r, t):
    return "".join(c.upper() if r.random() < .5 else c.lower() for c in t)


def _leet(r, t):
    return "".join(c.translate(LEET) if r.random() < .6 else c for c in t)


def _filler(r, t):
    w = t.split()
    w.insert(r.randrange(len(w) + 1), r.choice(FILLERS))
    return " ".join(w)


def _zwsp(r, t):
    i = r.randrange(1, max(2, len(t)))
    return t[:i] + "\u200b" + t[i:]


def _prefix(r, t):
    return r.choice(PREFIX) + t


def _spacing(r, t):
    w = t.split()
    k = r.randrange(len(w))
    w[k] = " ".join(w[k])           # i g n o r e
    return " ".join(w)


def _punct(r, t):
    return t.replace(" ", r.choice([" - ", " . ", "  "]), 1)


MUTATIONS = [_case, _leet, _filler, _zwsp, _prefix, _spacing, _punct]


class AdaptiveAttacker:
    def __init__(self, seed=0, max_queries=12):
        self.rng = random.Random(seed)
        self.max_queries = max_queries

    def evade(self, probe, payload):
        """probe(payload) -> decision str. Returns (evaded, final_payload, queries_used)."""
        current = payload
        for q in range(1, self.max_queries + 1):
            cand = self.rng.choice(MUTATIONS)(self.rng, current)
            if probe(cand) == "ALLOW":
                return True, cand, q
            if self.rng.random() < 0.7:       # greedy-ish: keep stacking mutations
                current = cand
        return False, current, self.max_queries
