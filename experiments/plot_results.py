
import matplotlib.pyplot as plt

def plot_comparison(no_llm, llm):

    labels = ["Precision", "Recall", "Accuracy", "F1"]

    plt.figure()

    plt.plot(labels, no_llm, marker='o', label="No LLM")
    plt.plot(labels, llm, marker='o', label="With LLM")

    plt.title("LLM Impact on Cyber Defense Performance")
    plt.legend()

    plt.savefig("comparison.png")
    plt.show()
