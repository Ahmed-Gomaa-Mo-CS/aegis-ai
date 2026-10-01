import argparse
import logging

from config.settings import Config
from aegis.core.system import AegisSystem
from aegis.simulation.attacker import EventGenerator


def main():
    ap = argparse.ArgumentParser(description="Aegis-AI demo run")
    ap.add_argument("--n", type=int, default=300)
    ap.add_argument("--k", type=int, default=3, help="few-shot examples for the LLM agent (0,2..5)")
    ap.add_argument("--budget", type=float, default=46)
    ap.add_argument("--backend", choices=["sim", "gemini"], default="sim")
    ap.add_argument("--no-llm", action="store_true")
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()
    logging.basicConfig(level=logging.WARNING)

    agents = ("ids", "ml", "ai") if a.no_llm else ("ids", "ml", "ai", "llm")
    cfg = Config(agents=agents, k_shots=a.k, budget=a.budget, llm_backend=a.backend)
    system = AegisSystem(cfg, seed=a.seed)
    s = system.run(EventGenerator(seed=a.seed).stream(a.n))
    print({k: round(v, 3) for k, v in s.items()})
    system.coordinator.trust_model.report()
    if system.llm:
        print(f"LLM memory size: {len(system.llm.store)}")


if __name__ == "__main__":
    main()
