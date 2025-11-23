from typing import Sequence, Mapping
import numpy as np

def create_val_dictionary(known_vals: Sequence[float] | None,
                          known_years: Sequence[int] | None,
                          all_years: Sequence[int]) -> Mapping[int, float]:
    """Return a dictionary mapping years to values, interpolating if partial data provided.

    Parameters
    ----------
    known_vals : sequence of float | None
        Known numeric values corresponding to known_years. If None or empty -> zeros for all years.
    known_years : sequence of int | None
        Years for which values are provided. Must be same length as known_vals.
    all_years : sequence of int
        Target year vector to populate.

    Returns
    -------
    dict[int, float]
        Mapping year -> value (interpolated or zero).
    """
    if not known_vals or not known_years:
        return {y: 0.0 for y in all_years}
    if len(known_vals) != len(known_years):
        raise ValueError("known_vals and known_years must have same length")
    # Linear interpolation over the domain of all_years
    interpolated_vals = np.interp(all_years, known_years, known_vals)
    return dict(zip(all_years, interpolated_vals))