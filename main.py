
from aegis.core.system import AegisSystem


def run_demo():
    print("\n=== AEGIS-AI DEMO RUN ===\n")

    system = AegisSystem(use_llm=True)
    system.run_experiment(n=20)


def run_no_llm():
    print("\n=== RUN WITHOUT LLM ===\n")

    system = AegisSystem(use_llm=False)
    system.run_experiment(n=20)


if __name__ == "__main__":

    #  Any mode can be selected.
    run_demo()

    # Quick comparison:
    # run_no_llm()
