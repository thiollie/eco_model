import numpy as np
import copy
import plotly.graph_objects as go


def aff_analyse_fc(dict_lf,
                   weight_week_dict,
                   type_energy: str,
                   weeks,
                   hours,
                   years,
                   fig_input,
                   year: int | None = None):
    """Analyse & plot load factor statistics deterministically.

    Parameters
    ----------
    dict_lf : dict[(int,int,int), float]
        Mapping (year, week, hour) -> load factor.
    weight_week_dict : dict[int,int]
        Representative week weights.
    type_energy : str
        Label for figure names.
    year : int | None
        Year to display weekly average. If None, first year in global 'years' sequence is used.
    """
    dict1 = copy.deepcopy(dict_lf)

    # Select deterministic year
    year_number = year if year is not None else (years[0] if hasattr(years, '__getitem__') else list(years)[0])
    average_week_values = [
        np.sum(dict1[(year_number, w, h)] for h in hours) / 168 for w in weeks
    ]

    fig_input[type_energy + 'plot 1'] = go.Figure()
    fig_input[type_energy + 'plot 1'].add_trace(
        go.Scatter(x=list(weeks), y=average_week_values, mode='lines', name="week average")
    )
    fig_input[type_energy + 'plot 1'].update_layout(
        title=f'Load factor week average of {type_energy} for the year {year_number}',
        xaxis_title='Representative week',
        yaxis_title='Load factor average',
        width=750, height=350, margin=dict(l=50, r=150, b=30, t=50), font=dict(size=15), showlegend=True
    )

    # Annual averages over scenario years
    average_years_values = [
        np.sum(dict1[(y, w, h)] * weight_week_dict[w] for w in weeks for h in hours) / (52 * 168)
        for y in years
    ]
    total_average = float(np.mean(average_years_values))

    fig_input[type_energy + 'plot 2'] = go.Figure()
    fig_input[type_energy + 'plot 2'].add_trace(
        go.Scatter(x=list(years), y=average_years_values, mode='lines', name="Annual average")
    )
    fig_input[type_energy + 'plot 2'].add_trace(
        go.Scatter(x=[years[0], years[-1]], y=[total_average, total_average], name="total average",
                   line=dict(color="Red", width=2, dash="dot"))
    )
    fig_input[type_energy + 'plot 2'].update_layout(
        title=f"Load factor of {type_energy}", yaxis_title='Load Factor', xaxis_title="",
        width=750, height=350, margin=dict(l=50, r=150, b=30, t=50), font=dict(size=15), showlegend=True
    )
    fig_input[type_energy + 'plot 2'].add_annotation(
        x=0.5,
        y=total_average * 1.05,
        xref="paper",
        yref="y",
        text="Moyenne totale " + str(round(total_average, 3)),
        showarrow=False,
        font=dict(color="Red", size=12)
    )
 