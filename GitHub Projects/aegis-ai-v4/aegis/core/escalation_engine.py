import logging

log = logging.getLogger(__name__)


class EscalationEngine:
    """Cheapest-first cascade under a per-event budget.

    Stops early once the coordinator deems the evidence decisive; skips agents
    that do not fit the remaining budget; survives agent failures (the failed
    call is still paid for, as it would be in reality)."""

    def __init__(self, agents, coordinator, resource_controller, bus,
                 cascade=True, stop_share=0.8, stop_weight=0.8):
        rc = resource_controller
        self.agents = sorted(agents, key=lambda a: rc.cost(a.name))
        self.coordinator = coordinator
        self.rc = rc
        self.bus = bus
        self.cascade = cascade
        self.stop_share = stop_share
        self.stop_weight = stop_weight
        self.failures = 0
        self.last_attempted = []

    def evaluate(self, threat):
        self.rc.start_event()
        self.bus.clear()
        results = []
        self.last_attempted = []
        for agent in self.agents:
            if not self.rc.can_afford(agent.name):
                break                      # sorted ascending: nothing later fits either
            self.rc.spend(agent.name)
            self.last_attempted.append(agent.name)
            try:
                res = agent.analyze(threat)
            except Exception as e:         # resilience: a broken agent must not stop defence
                self.failures += 1
                log.warning("%s failed: %s", agent.name, e)
                continue
            results.append((agent.name, res))
            self.bus.broadcast(agent.name, "EVIDENCE", {
                "agent": agent.name, "decision": res["decision"],
                "confidence": round(res["confidence"], 2)})
            if self.cascade and self.coordinator.is_decisive(results, self.stop_share, self.stop_weight):
                break
        return self.coordinator.aggregate(results), results
