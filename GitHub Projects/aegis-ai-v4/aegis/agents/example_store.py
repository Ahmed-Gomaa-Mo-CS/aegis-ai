"""Few-shot memory: labelled examples retrieved by similarity (char-trigram cosine)."""
import math
from collections import Counter


def _vec(text):
    t = f" {text.lower()} "
    c = Counter(t[i:i + 3] for i in range(len(t) - 2))
    norm = math.sqrt(sum(v * v for v in c.values())) or 1.0
    return c, norm


def cosine(a, b):
    (ca, na), (cb, nb) = a, b
    if len(ca) > len(cb):
        ca, cb = cb, ca
    return sum(v * cb.get(g, 0) for g, v in ca.items()) / (na * nb)


class ExampleStore:
    def __init__(self, max_size=200):
        self.max_size = max_size
        self.items = []           # (payload, label, vec)
        self._seen = set()

    def __len__(self):
        return len(self.items)

    def add(self, payload, label):
        """label in {"block", "safe"}. Returns True if stored."""
        if payload in self._seen:
            return False
        if len(self.items) >= self.max_size:
            old = self.items.pop(0)   # FIFO eviction keeps memory adaptive
            self._seen.discard(old[0])
        self.items.append((payload, label, _vec(payload)))
        self._seen.add(payload)
        return True

    def retrieve(self, payload, k):
        """Top-k most similar examples, guaranteeing both labels appear when k>=2
        (reduces majority-label bias in few-shot prompts)."""
        if k <= 0 or not self.items:
            return []
        q = _vec(payload)
        ranked = sorted(((cosine(q, v), p, l) for p, l, v in self.items), reverse=True)
        chosen = []
        if k >= 2:
            for label in ("block", "safe"):
                best = next((r for r in ranked if r[2] == label), None)
                if best:
                    chosen.append(best)
        for r in ranked:
            if len(chosen) >= k:
                break
            if r not in chosen:
                chosen.append(r)
        chosen = sorted(chosen[:k], reverse=True)
        return [{"payload": p, "label": l, "sim": round(s, 3)} for s, p, l in chosen]
