class Ctx:
    def __init__(self, world, log, stub, run_id, phase, fault_point, marker, statedir, budget=3):
        self.world, self.log, self.stub = world, log, stub
        self.run_id, self.phase, self.fault_point = run_id, phase, fault_point
        self.marker, self.statedir, self.budget = marker, statedir, budget

class Adapter:
    name = "?"; version = "?"; population_role = "agent-runtime"
    def applicability(self): raise NotImplementedError
    def run_c2r(self, ctx): raise NotImplementedError
    def run_c3w(self, ctx): raise NotImplementedError
    def run_c3c(self, ctx): raise NotImplementedError
