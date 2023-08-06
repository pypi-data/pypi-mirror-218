from typing import List

from vessim.cosim._util import VessimSimulator, VessimModel
from vessim.sil.power_meter import PowerMeter


class ComputingSystemSim(VessimSimulator):
    """Computing System simulator that executes its model."""

    META = {
        "type": "time-based",
        "models": {
            "ComputingSystem": {
                "public": True,
                "params": ["power_meters", "pue"],
                "attrs": ["p"],
            },
        },
    }

    def __init__(self):
        self.step_size = None
        super().__init__(self.META, _ComputingSystemModel)

    def init(self, sid, time_resolution, step_size, eid_prefix=None):
        self.step_size = step_size
        return super().init(sid, time_resolution, eid_prefix=eid_prefix)

    def finalize(self) -> None:
        """Stops power meters' threads."""
        super().finalize()
        for model_instance in self.entities.values():
            for power_meter in model_instance.power_meters: # type: ignore
                power_meter.finalize()

    def next_step(self, time):
        return time + self.step_size


class _ComputingSystemModel(VessimModel):
    """Model of the computing system.

    This model considers the power usage effectiveness (PUE) and power
    consumption of a list of power meters.

    Args:
        power_meters: A list of PowerMeter objects
            representing power meters in the system.
        pue: The power usage effectiveness of the system.
    """

    def __init__(self, power_meters: List[PowerMeter], pue: float = 1):
        self.power_meters = power_meters
        self.pue = pue
        self.p = 0.0

    def step(self, time: int, inputs: dict) -> None:
        """Updates the power consumption of the system.

        The power consumption is calculated as the product of the PUE and the
        sum of the node power of all power meters.
        """
        self.p = -self.pue * sum(pm.measure() for pm in self.power_meters)
