from typing import Any


class TechnoError(Exception):
    """Custom exception raised for inconsistencies in technology parameter configuration."""
    pass


class Techno:
# --------------------- Constructor ----------------------------------------------------------------------------------
    def __init__(self, ttype: str, tname: str, ttitle: str, prm_eco: Any, prm_tech: Any, prm_spec: Any):

        self._type: str     = ttype     # family of the techno ('dispatchable', 'fatal', 'storage')
        self._name: str     = tname     # name of techno ('nuclear', 'gas', 'vre', etc.)
        self._title: str    = ttitle    # subtype ('new', 'hist', 'pv', 'wof', etc.)
        self._prm_eco       = prm_eco
        self._prm_tech      = prm_tech
        self._prm_spec      = prm_spec

        # Immediate consistency checks
        self.test_annuity()  # Test if capex OR depreciation defined (mutual exclusion)
        self.test_negative_cost_storage()  # If storage charge segment -> variable costs must be <= 0

# --------------------- End Of Constructor ----------------------------------------------------------------------------

# --------------------- Test Functions --------------------------------------------------------------------------------

    def test_annuity(self) -> None:
        """Ensure economic parameters define exactly one of CAPEX annuitization or depreciation.

        Raises:
            TechnoError: If both or none of is_cap / is_dep are True.
        """
        is_cap = getattr(self._prm_eco, "is_cap", lambda: False)()
        is_dep = getattr(self._prm_eco, "is_dep", lambda: False)()
        if is_cap and is_dep:
            raise TechnoError(f"is_cap and is_dep both True => {self._type} - {self._name} - {self._title}")
        if (not is_cap) and (not is_dep):
            raise TechnoError(f"is_cap and is_dep both False => {self._type} - {self._name} - {self._title}")

    def test_negative_cost_storage(self) -> None:
        """Validate that storage charging segment has non-positive variable costs if defined.

        For a charging techno (title == 'charge'), any defined variable cost profile (OM, fuel, CO2, MI)
        should have at least one non-positive value. Empty dicts are ignored.
        """
        if self._type == 'storage' and self._title == 'charge':
            eco = self._prm_eco
            def _has_only_positive(d: dict) -> bool:
                return isinstance(d, dict) and d and all(v > 0 for v in d.values())
            checks = [
                (eco.get_var_om(), "OM"),
                (eco.get_var_f(), "Fuel"),
                (eco.get_var_co2(), "CO2"),
                (eco.get_var_mi(), "MI"),
            ]
            for d, label in checks:
                if _has_only_positive(d):
                    raise TechnoError(f"Variable {label} cost should include non-positive values for storage charge => {self._type} - {self._name} - {self._title}")

# --------------------- GET/SET methods -------------------------------------------------------------------------------

    # Get methods
    def get_type(self) -> str:
        return self._type
    def get_name(self) -> str:
        return self._name
    def get_title(self) -> str:
        return self._title
    def get_eco(self) -> Any:
        return self._prm_eco
    def get_tech(self) -> Any:
        return self._prm_tech
    def get_spec(self) -> Any:
        return self._prm_spec

    # Set methods
    def set_type(self, ttype: str) -> None:
        self._type = ttype
    def set_name(self, tname: str) -> None:
        self._name = tname
    def set_title(self, ttitle: str) -> None:
        self._title = ttitle

    def set_eco(self, prm_eco: Any) -> None:
        self._prm_eco = prm_eco
    def set_tech(self, prm_tech: Any) -> None:
        self._prm_tech = prm_tech
    def set_spec(self, prm_spec: Any) -> None:
        self._prm_spec = prm_spec

# --------------------- PRINT methods ---------------------------------------------------------------------------------
    def Print(self) -> None:  # Keeping original name for backward compatibility
        """Human-readable summary of the technology."""
        print()
        print('#' * 69)
        print('### Technology Summary')
        print('#' * 69 + '\n')
        print(f"Name     : {self._name}")
        print(f"Family   : {self._type}")
        print(f"Subtype  : {self._title}")
        if hasattr(self._prm_eco, 'Print'):
            print('--- Eco Params (compact) ---')
            try:
                self._prm_eco.Print()
            except Exception:
                pass
        if hasattr(self._prm_tech, 'Print'):
            print('--- Tech Params (compact) ---')
            try:
                self._prm_tech.Print()
            except Exception:
                pass
        print('#' * 69)
        print()
    