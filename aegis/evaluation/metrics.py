
class Metrics:

    def __init__(self):

        self.tp = 0  # true positive
        self.fp = 0  # false positive
        self.fn = 0  # false negative
        self.tn = 0  # true negative

        self.history = []

    def update_metrics(self, decision, actual_malicious):
        
        self.metrics.update(decision, actual_malicious)
        predicted = decision == "BLOCK"

        if predicted and actual_malicious:
            self.tp += 1
        elif predicted and not actual_malicious:
            self.fp += 1
        elif not predicted and actual_malicious:
            self.fn += 1
        else:
            self.tn += 1

        self.history.append((self.tp, self.fp, self.fn, self.tn))

    def compute(self):

        precision = self.tp / (self.tp + self.fp + 1e-6)
        recall = self.tp / (self.tp + self.fn + 1e-6)
        accuracy = (self.tp + self.tn) / (self.tp + self.fp + self.fn + self.tn + 1e-6)

        f1 = 2 * precision * recall / (precision + recall + 1e-6)

        return precision, recall, accuracy, f1

    def report(self):

        p, r, a, f1 = self.compute()

        print(f"Precision: {p:.3f}")
        print(f"Recall: {r:.3f}")
        print(f"Accuracy: {a:.3f}")
        print(f"F1-score: {f1:.3f}")
