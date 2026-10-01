"""Central configuration for Aegis-AI experiments."""
from dataclasses import dataclass, field, replace

# Relative cost units per invocation (LLM >> rule-based).
DEFAULT_COSTS = {"IDS-Agent": 1, "ML-Agent": 5, "AI-Agent": 10, "LLM-Agent": 30}


@dataclass(frozen=True)
class Config:
    # --- which agents exist -------------------------------------------------
    agents: tuple = ("ids", "ml", "ai", "llm")

    # --- resource awareness -------------------------------------------------
    costs: dict = field(default_factory=lambda: dict(DEFAULT_COSTS))
    budget: float = 46          # max cost units spendable on ONE event
    cascade: bool = True        # False -> run every affordable agent
    stop_share: float = 0.80    # early-stop: leading class must hold >= this share
    stop_weight: float = 0.80   # ...and total trust*confidence evidence >= this

    # --- LLM agent (few-shot) -----------------------------------------------
    k_shots: int = 3            # 0 = zero-shot; the research target is 2..5
    seed_pool_size: int = 10    # labelled examples available at t=0
    memory_update: bool = True  # add hard cases to the example store online
    llm_backend: str = "sim"    # "sim" (offline proxy) | "gemini"
    llm_failure_rate: float = 0.0  # fault injection for the sim backend

    llm_arbiter: bool = False   # LLM verdict overrides the vote when it ran and conf >= 0.7

    # --- adaptation ----------------------------------------------------------
    label_rate: float = 1.0     # fraction of events with delayed ground truth
    trust_decay: float = 0.99   # forgetting factor (adapts to drift)

    def with_(self, **kw):
        return replace(self, **kw)
