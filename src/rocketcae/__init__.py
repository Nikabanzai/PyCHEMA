"""RocketCAE: preliminary liquid rocket engine trade studies via NASA CEA."""

from rocketcae.models import EngineInputs, EngineResult, SweepResult
from rocketcae.cea_runner import run_rocket
from rocketcae.propellants import list_propellant_pairs, get_pair

__all__ = [
    "EngineInputs",
    "EngineResult",
    "SweepResult",
    "run_rocket",
    "list_propellant_pairs",
    "get_pair",
]

__version__ = "0.1.0"
