
from aegis.core.system import AegisSystem

def run_experiment(use_llm):

    system = AegisSystem(use_llm=use_llm)
    system.run_experiment(n=50)

    return system.metrics.compute(), system.metrics.history


def main():

    print("\n=== RUNNING WITHOUT LLM ===")
    no_llm_metrics, no_llm_history = run_experiment(False)

    print("\n=== RUNNING WITH LLM ===")
    llm_metrics, llm_history = run_experiment(True)

    print("\n=== COMPARISON ===")

    print("No LLM:", no_llm_metrics)
    print("With LLM:", llm_metrics)


if __name__ == "__main__":
    main()

