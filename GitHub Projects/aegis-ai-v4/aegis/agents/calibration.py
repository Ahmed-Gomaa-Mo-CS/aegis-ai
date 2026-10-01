class OnlineCalibrator:
    """Binned Beta calibration of a raw P(malicious), updated from feedback.

    Each bin of raw probability keeps pseudo-counts seeded at the raw value
    (prior_strength), then moves toward the observed malicious frequency.
    Fixes the failure seen in the experiments: Naive Bayes is confidently
    wrong on novel inputs, which let the cascade stop before the LLM ran."""

    def __init__(self, bins=10, prior_strength=4.0):
        self.bins = bins
        self.s = prior_strength
        self.mal = [0.0] * bins
        self.tot = [0.0] * bins

    def _bin(self, p):
        return min(self.bins - 1, int(p * self.bins))

    def update(self, raw_p, malicious):
        i = self._bin(raw_p)
        self.tot[i] += 1
        self.mal[i] += 1.0 if malicious else 0.0

    def calibrate(self, raw_p):
        i = self._bin(raw_p)
        centre = (i + 0.5) / self.bins
        return (self.mal[i] + self.s * centre) / (self.tot[i] + self.s)
