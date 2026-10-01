<<<<<<< HEAD
import logging
import random

from config.settings import Config
=======

from aegis.simulation.attacker import generate_attack
>>>>>>> 1a004f91eda03eafd4e26b1cf9dbdc33beff3bbb
from aegis.agents.ids_agent import IDSAgent
from aegis.agents.ml_agent import MLAgent
from aegis.agents.ai_agent import AIAgent
from aegis.agents.llm_agent import LLMAgent
<<<<<<< HEAD
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
    def __init__(self, config=None, seed=0):
        self.cfg = cfg = config or Config()
        self.rng = random.Random(seed * 7919 + 13)
        gen = EventGenerator(seed=10_000 + seed)       # day-0 knowledge generator
        self.bus = MessageBus()

        agents = []
        self.llm = None
        for name in cfg.agents:
            if name == "ids":
                agents.append(IDSAgent(self.bus))
            elif name == "ml":
                agents.append(MLAgent(self.bus, train_events=gen.labelled_pool(300)))
            elif name == "ai":
                agents.append(AIAgent(self.bus))
            elif name == "llm":
                store = ExampleStore()
                for e in gen.labelled_pool(cfg.seed_pool_size):
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
        self.llm_calls += any(n == "LLM-Agent" for n, _ in results)

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
=======
from aegis.core.escalation_engine import EscalationEngine
from aegis.core.resource_controller import ResourceController
from aegis.coordination.coordinator import Coordinator
from aegis.coordination.message_bus import MessageBus
from aegis.evaluation.metrics import Metrics


class AegisSystem:

    def __init__(self, use_llm=True):

        #  communication layer
        self.bus = MessageBus()

        #  agents
        self.agents = [
            IDSAgent(self.bus),
            MLAgent(self.bus),
            AIAgent(self.bus),
        ]
        
        if use_llm:
            self.agents.append(LLMAgent(self.bus))

        self.resource_controller = ResourceController()
        self.coordinator = Coordinator()

        self.engine = EscalationEngine(
            agents=self.agents,
            coordinator=self.coordinator,
            resource_controller=self.resource_controller
        )

        self.metrics = Metrics()

    def run_cycle(self):

        # clear previous messages
        self.bus.clear()

        # generate attack
        threat = generate_attack()

        # run system
        decision, results = self.engine.evaluate(threat)

        # simulated ground truth
        actual_malicious = threat["type"] in ["malware", "ai_attack"]

        # update trust
        for agent_name, result in results:

            predicted_block = result["decision"] == "block"
            correct = (predicted_block == actual_malicious)

            self.coordinator.trust_model.update_trust(agent_name, correct)

        # update metrics
        self.metrics.update(decision, actual_malicious)

        # logs
        print(f"[THREAT] {threat}")
        print(f"[MESSAGES] {self.bus.get_messages()}")
        print(f"[DECISION] {decision}")
        print(f"[TRUST] {self.coordinator.trust_model.trust_scores}")
        print("-" * 50)

    def run_experiment(self, n=20):

        for _ in range(n):
            self.run_cycle()

        print("\n=== FINAL REPORT ===")
        self.metrics.report()

        # Trust report
        self.coordinator.trust_model.report()

>>>>>>> 1a004f91eda03eafd4e26b1cf9dbdc33beff3bbb
