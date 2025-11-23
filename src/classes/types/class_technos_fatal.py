from ..class_technos import Techno
from typing import Any


class Techno_Fatal(Techno):
# --------------------- Constructor ----------------------------------------------------------------------------------
    def __init__(self, name: str, subtype: str, eco_params: Any, tech_params: Any, fatal_params: Any):
        """Fatal (non-dispatchable) technology wrapper."""
        super().__init__('fatal', name, subtype, eco_params, tech_params, fatal_params)

# --------------------- End Of Constructor ----------------------------------------------------------------------------

    # Get methods
    def get_spec(self) -> Any:
        return self._prm_spec

    # Set methods
    def set_spec(self, fatal_params: Any) -> None:
        self._prm_spec = fatal_params

    # PRINT inherits base


# --------------------- PRINT methods ---------------------------------------------------------------------------------
