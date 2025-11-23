from ..class_technos import Techno
from typing import Any


class Techno_Dispatchable(Techno):
# --------------------- Constructor ----------------------------------------------------------------------------------
    def __init__(self, name: str, subtype: str, eco_params: Any, tech_params: Any, dispatch_params: Any):
        """Dispatchable technology wrapper.

        Parameters
        ----------
        name : str
            Technology family name (e.g. 'gas').
        subtype : str
            Specific subtype (e.g. 'ccgt').
        eco_params : Any
            Economic parameter object.
        tech_params : Any
            Technical parameter object.
        dispatch_params : Any
            Dispatchable-specific parameter object (ramping, etc.).
        """
        super().__init__('dispatchable', name, subtype, eco_params, tech_params, dispatch_params)

# --------------------- End Of Constructor ----------------------------------------------------------------------------

    # Get methods
    def get_spec(self) -> Any:  # semantic alias
        return self._prm_spec

    # Set methods
    def set_spec(self, dispatch_params: Any) -> None:
        self._prm_spec = dispatch_params

    # PRINT keeps base implementation

