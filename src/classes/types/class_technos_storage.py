from ..class_technos import Techno
from typing import Any


class Techno_Storage(Techno):
# --------------------- Constructor ----------------------------------------------------------------------------------
    def __init__(self, name: str, subtype: str, eco_params: Any, tech_params: Any, storage_params: Any):
        """Storage technology wrapper (charge/discharge pairs, battery, STEP, etc.)."""
        super().__init__('storage', name, subtype, eco_params, tech_params, storage_params)

# --------------------- End Of Constructor ----------------------------------------------------------------------------

    # Get methods
    def get_spec(self) -> Any:
        return self._prm_spec

    # Set methods
    def set_spec(self, storage_params: Any) -> None:
        self._prm_spec = storage_params

    # PRINT inherits base


# --------------------- PRINT methods ---------------------------------------------------------------------------------
