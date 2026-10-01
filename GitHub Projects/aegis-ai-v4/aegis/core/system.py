import logging
import random

from config.settings import Config
from aegis.agents.ids_agent import IDSAgent
from aegis.agents.ml_agent import MLAgent
from aegis.agents.ai_agent import AIAgent
from aegis.agents.llm_agent import LLMAgent
from aegis.agents.example_store import ExampleStore
from aegis.agents.llm_backends import make_backend
from aegis.coordination.coordinator import Coordinator
from aegis.coordination.message_bus import MessageBus
from aegis.core.escalation_engine import EscalationEngine
from aegis.core.resource_controller import ResourceController
from aegis.evaluation.metrics import Metrics
from aegis.simulation.attacker import EventGenerator

log = logging.getLogger(__name__)


class AegisSystem:
    def __init__(self, config=None, seed=0, day0_events=None):
        self.cfg = cfg = config or Config()
        self.rng = random.Random(seed * 7919 + 13)
        gen = EventGenerator(seed=10_000 + seed)       # day-0 knowledge generator
        # day0_events: labelled real data ({"payload","malicious"}) replacing the synthetic day-0 knowledge
        ml_train = day0_events if day0_events is not None else gen.labelled_pool(300)
        seed_pool = (day0_events[:cfg.seed_pool_size] if day0_events is not None
                     else gen.labelled_pool(cfg.seed_pool_size))
        self.bus = MessageBus()

        agents = []
        self.llm = None
        for name in cfg.agents:
            if name == "ids":
                agents.append(IDSAgent(self.bus))
            elif name == "ml":
                agents.append(MLAgent(self.bus, train_events=ml_train,
                                    calibrate=cfg.calibrate_ml,
                                    novelty_penalty=cfg.novelty_penalty))
            elif name == "ai":
                agents.append(AIAgent(self.bus))
            elif name == "llm":
                store = ExampleStore()
                for e in seed_pool:
                    store.add(e["payload"], "block" if e["malicious"] else "safe")
                backend = make_backend(cfg.llm_backend, seed=seed, failure_rate=cfg.llm_failure_rate)
                self.llm = LLMAgent(self.bus, backend, store, k=cfg.k_shots,
                                    memory_update=cfg.memory_update)
                agents.append(self.llm)
            else:
                raise ValueError(f"unknown agent '{name}'")
        self.agents = {a.name: a for a in agents}

        self.rc = ResourceController(cfg.costs, cfg.budget)
        self.coordinator = Coordinator(trust_decay=cfg.trust_decay,
                                    arbiter="LLM-Agent" if cfg.llm_arbiter else None)
        self.engine = EscalationEngine(agents, self.coordinator, self.rc, self.bus,
                                       cascade=cfg.cascade, stop_share=cfg.stop_share,
                                       stop_weight=cfg.stop_weight)
        self.m_block = Metrics(("BLOCK",))
        self.m_flag = Metrics(("BLOCK", "MONITOR"))
        self.n = 0
        self.llm_calls = 0

    def run_cycle(self, event):
        threat = {"payload": event["payload"]}          # ground truth never reaches agents
        decision, results = self.engine.evaluate(threat)
        malicious = event["malicious"]
        self.n += 1
        self.llm_calls += "LLM-Agent" in self.engine.last_attempted

        # evaluation always uses the true label; *learning* only when feedback arrives
        self.m_block.update(decision, malicious)
        self.m_flag.update(decision, malicious)
        if self.rng.random() < self.cfg.label_rate:
            for name, res in results:
                self.coordinator.trust_model.update_trust(
                    name, (res["decision"] != "safe") == malicious)
                self.agents[name].learn(event["payload"], malicious, res)
        return decision, results

    def run(self, events):
        for e in events:
            self.run_cycle(e)
        return self.summary()

    def summary(self):
        b, f = self.m_block.compute(), self.m_flag.compute()
        n = max(self.n, 1)
        return {"precision": b["precision"], "recall": b["recall"], "f1": b["f1"],
                "flag_f1": f["f1"], "flag_recall": f["recall"],
                "cost": self.rc.total_spent / n, "llm_rate": self.llm_calls / n,
                "failures": self.engine.failures / n}
