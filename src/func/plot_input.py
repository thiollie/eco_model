import re
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

try:
    # Prefer package-relative import if available
    from .aff_analyse_fc import aff_analyse_fc
except Exception:
    # Fallback when executed via %run without package context
    from aff_analyse_fc import aff_analyse_fc

plot_input_flag = globals().get('plot_input', False)

if plot_input_flag:

    # Reference year for cost/use plots (falls back to first scenario year)
    reference_year = globals().get('year_start', years.start)

    # Shared layout primitives so that every plot uses the same visual grammar
    DEFAULT_FIG_W = globals().get('fig_w', 760)
    DEFAULT_FIG_H = globals().get('fig_h', 360)
    COMMON_MARGIN = dict(l=70, r=30, t=60, b=55)
    WIDE_MARGIN = dict(l=80, r=30, t=60, b=60)
    SUBPLOT_MARGIN = dict(l=70, r=30, t=50, b=40)

    def apply_layout(fig, *, title, x_title=None, y_title=None, width=None, height=None,
                     legend=True, margin=None, xaxis_extra=None, yaxis_extra=None):
        """Apply harmonised layout defaults to a Plotly figure."""
        layout_kwargs = dict(
            template="cineaste",
            title=dict(text=title, x=0.02, xanchor='left'),
            xaxis_title=x_title,
            yaxis_title=y_title,
            width=width or DEFAULT_FIG_W,
            height=height or DEFAULT_FIG_H,
            margin=margin or COMMON_MARGIN,
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.03,
                x=0,
                xanchor='left'
            )
        )
        if not legend:
            layout_kwargs['showlegend'] = False
        fig.update_layout(**layout_kwargs)
        if xaxis_extra:
            fig.update_xaxes(**xaxis_extra)
        if yaxis_extra:
            fig.update_yaxes(**yaxis_extra)
        return fig

    fig_input = {}
    
##########################################################################
# Demand
##########################################################################

    key = 'demand'
    if Display_input['demand']:
        demand_y = {}
        unique, counts = np.unique(group, return_counts=True)
        for y in years:
            demand_y_tmp = 0    
            for w in weeks:
                demand_y_tmp += counts[w-1] * sum(value for (yy, ww, hh), value in demand_dict.items() if yy == y and ww == w)
            demand_y[y] = demand_y_tmp / 1e6 # => to get TWh

        fig_input[key] = go.Figure()
        fig_input[key].add_trace(
            go.Scatter(
                x=list(demand_y.keys()),
                y=list(demand_y.values()),
                line=dict(width=2.5),
                mode='lines+markers',
                marker=dict(size=6)
            )
        )
        apply_layout(fig_input[key], title="Demand evolution", y_title='Demand [TWh]', x_title="Year")

##########################################################################
# Techno Costs
##########################################################################

    key = 'fix_costs'
    if Display_input[key] :
        fig_input[key] = go.Figure()
        for t in techno.keys():
            n = techno[t].get_name() + ' ' + techno[t].get_title()
            fig_input[key].add_trace(
                go.Scatter(
                    x=list(years_world),
                    y=list(techno[t].get_eco().get_cost_profile_fix().values()),
                    line=dict(width=2.0, shape='hv'),
                    mode='lines',
                    name=n
                )
            )
        apply_layout(fig_input[key], title="Fixed cost evolution", y_title='Total cost [€/MW/y]', x_title="Year")
        #fig_input[key].write_html(current_path + '/out/' + name_simulation + '/input' + '/' + key + '.html')
    
    key = 'tot_costs'
    if Display_input[key] :
        fig_input[key] = go.Figure()
        for t in techno.keys():
            U = np.arange(1, 8761, 1)
            n = techno[t].get_name() + ' ' + techno[t].get_title()
            fig_input[key].add_trace(
                go.Scatter(
                    x=U,
                    y=techno[t].get_eco().get_cost_profile_tot(reference_year),
                    line=dict(width=2.0, shape='hv'),
                    mode='lines',
                    name=n
                )
            )
        apply_layout(
            fig_input[key],
            title=f"Total cost profile — {reference_year}",
            y_title='Total cost [€/MW/y]',
            x_title="Use (h/y)"
        )
        #fig_input[key].write_html(current_path + '/out/' + name_simulation + '/input' + '/' + key + '.html')
    
##########################################################################
# Historical Data
##########################################################################
    
    key = 'hist_data'
    if Display_input[key] :
        n_of_hist_data_to_plot = 0
        for i,t in techno.items():
            historic_data_capa = t.get_tech().get_historic_data("CAPA")
            if not (historic_data_capa is None) and (not all(value == 0 for value in historic_data_capa.values())) :
                n_of_hist_data_to_plot += 1
    
        fig_input[key] = make_subplots(cols=2,rows=n_of_hist_data_to_plot)
        n = 1
        for i,t in techno.items():
            historic_data_inv  = t.get_tech().get_historic_data("INV")
            historic_data_capa = t.get_tech().get_historic_data("CAPA")
            name=t.get_name() + ' ' + t.get_title()
            
            if historic_data_capa is not None and isinstance(historic_data_capa, dict) and any(value != 0 for value in historic_data_capa.values()):
                x,y = list(historic_data_inv.keys()),list(historic_data_inv.values())
                fig_input[key].add_trace(go.Bar(name=name, x=x, y=y, marker_line_width=0), col=1, row=n)
                x,y = list(historic_data_capa.keys()),list(historic_data_capa.values())
                fig_input[key].add_trace(go.Scatter(name=name, x=x, y=y, line=dict(width=2)), col=2, row=n)
                n += 1
    
        apply_layout(
            fig_input[key],
            title="Historic data — investment vs capacity",
            x_title="Year",
            y_title="MW",
            width=DEFAULT_FIG_W,
            height=max(DEFAULT_FIG_H, n_of_hist_data_to_plot * 220),
            margin=SUBPLOT_MARGIN
        )
        #fig_input[key].write_html(current_path + '/out/' + name_simulation + '/input' + '/' + key + '.html')
    
##########################################################################
# Carbon Trajectory
##########################################################################
    
    key = 'carbon_cost'
    if Display_input[key] :
    
        fig_input[key] = go.Figure()
        for t in techno.keys():
            n = techno[t].get_name() + ' ' + techno[t].get_title()
            if re.match('gas', n):
                fig_input[key].add_trace(
                    go.Scatter(
                        x=list(years_world),
                        y=list(techno[t].get_eco().get_var_co2().values()),
                        line=dict(width=2.0),
                        mode='lines',
                        name=n
                    )
                )
        apply_layout(fig_input[key], title="CO₂ price trajectory", y_title='CO₂ cost [€/MWh]', x_title="Year")
        #fig_input[key].write_html(current_path + '/out/' + name_simulation + '/input' + '/' + key + '.html')
    
##########################################################################
# Representative demand
##########################################################################
    
    key = 'week_demand'
    if Display_input[key]:
        fig_input[key] = go.Figure()
        for index, row in demand_average.iterrows():
            fig_input[key].add_trace(
                go.Scatter(
                    x=demand_average.columns,
                    y=row,
                    mode='lines',
                    name=f'Week {index}',
                    line=dict(width=2)
                )
            )
        apply_layout(
            fig_input[key],
            title=f"Representative weeks — demand ({reference_year})",
            y_title='Demand (MW)',
            x_title=f"Hour across {number_of_mean_weeks} weeks"
        )
     
        #fig_input[key].write_html(current_path + '/out/' + name_simulation + '/input' + '/' + key + '.html')
    
##########################################################################
# PV representative week
##########################################################################
    
    key = 'week_pv'
    if Display_input[key] :
        fig_input[key] = go.Figure()
        for index, row in pv_lf_new.iterrows():
            fig_input[key].add_trace(
                go.Scatter(
                    x=pv_lf_new.columns,
                    y=row,
                    mode='lines',
                    name=f'Week {index}',
                    line=dict(width=1.8)
                )
            )
        apply_layout(
            fig_input[key],
            title=f"Representative weeks — PV load factor ({reference_year})",
            y_title='Load factor',
            x_title=f"Hour across {number_of_mean_weeks} weeks"
        )
     
        #fig_input[key].write_html(current_path + '/out/' + name_simulation + '/input' + '/' + key + '.html')
    
##########################################################################
# WON representative week
##########################################################################

    key = 'week_won'
    if Display_input[key] :
        fig_input[key] = go.Figure()
        for index, row in won_lf_new.iterrows():
            fig_input[key].add_trace(
                go.Scatter(
                    x=won_lf_new.columns,
                    y=row,
                    mode='lines',
                    name=f'Week {index}',
                    line=dict(width=1.8)
                )
            )
        apply_layout(
            fig_input[key],
            title=f"Representative weeks — onshore wind load factor ({reference_year})",
            y_title='Load factor',
            x_title=f"Hour across {number_of_mean_weeks} weeks"
        )
     
        #fig_input[key].write_html(current_path + '/out/' + name_simulation + '/input' + '/' + key + '.html')

##########################################################################
# WOF representative week
##########################################################################
    
    key = 'week_wof'
    if Display_input[key] :
    
        fig_input[key] = go.Figure()
        for index, row in wof_lf_new.iterrows():
            fig_input[key].add_trace(
                go.Scatter(
                    x=wof_lf_new.columns,
                    y=row,
                    mode='lines',
                    name=f'Week {index}',
                    line=dict(width=1.8)
                )
            )
        apply_layout(
            fig_input[key],
            title=f"Representative weeks — offshore wind load factor ({reference_year})",
            y_title='Load factor',
            x_title=f"Hour across {number_of_mean_weeks} weeks"
        )
     
        #fig_input[key].write_html(current_path + '/out/' + name_simulation + '/input' + '/' + key + '.html')

##########################################################################
# Wind Load Factor average on the simulation
##########################################################################
    
    key = 'load_factor_total'
    if Display_input[key] :
        # Deterministic load factor analysis (uses first scenario year by default)
        aff_analyse_fc(dict_won_lf, weight_week_dict, 'EOLIEN ONSHORE', weeks, hours, years, fig_input)
        aff_analyse_fc(dict_wof_lf, weight_week_dict, 'EOLIEN OFFSHORE', weeks, hours, years, fig_input)
        aff_analyse_fc(dict_pv_lf,  weight_week_dict, 'PV',              weeks, hours, years, fig_input)
        aff_analyse_fc(dict_lake_lf,weight_week_dict, 'LAKE',            weeks, hours, years, fig_input)
        aff_analyse_fc(dict_ror_lf, weight_week_dict, 'ROR',             weeks, hours, years, fig_input)
        
##########################################################################
# Load Factor data
##########################################################################

    key = 'load_factor_data'
    if Display_input[key] :
        won_lf_weekmean=won_lf_reshape.mean(axis=1)
        won_lf_yearmean=won_lf_weekmean.mean()
     
        wof_lf_weekmean=wof_lf_reshape.mean(axis=1)
        wof_lf_yearmean=wof_lf_weekmean.mean()
     
        pv_lf_weekmean=pv_lf_reshape.mean(axis=1)
        pv_lf_yearmean=pv_lf_weekmean.mean()
     
        ##"##### Eolien Onshore ### 
     
        fig_input[key + 'plot 1'] = go.Figure()
        fig_input[key + 'plot 1'].add_trace(go.Scatter(x=list(range(1,52)), y=np.array(won_lf_weekmean), mode='lines', name="Weekly mean", line=dict(width=2)))

        fig_input[key + 'plot 1'].add_trace(
            go.Scatter(
                x=[0,52],
                y=[won_lf_yearmean, won_lf_yearmean],
                name="Annual mean",
                line=dict(color="#ef4444", width=2, dash="dot")
            )
        )

        apply_layout(
            fig_input[key + 'plot 1'],
            title="Load factor — onshore wind",
            y_title='Load factor',
            x_title="Week",
            legend=True
        )
        fig_input[key + 'plot 1'].add_annotation(
            x=0.5,
            y=won_lf_yearmean*1.05,
            xref="paper",
            yref="y",
            text=f"Annual mean: {won_lf_yearmean:.3f}",
            showarrow=False,
            font=dict(color="#ef4444", size=12)
        )
    
        #fig_input[key].write_html(current_path + '/out/' + name_simulation + '/input' + '/' + key + '.html')
    
        ##### Eolien Offshore ## 
     
        fig_input[key + 'plot 2'] = go.Figure()
        fig_input[key + 'plot 2'].add_trace(go.Scatter(x=list(range(1,52)), y=np.array(wof_lf_weekmean), mode='lines', name="Weekly mean", line=dict(width=2)))

        fig_input[key + 'plot 2'].add_trace(
            go.Scatter(
                x=[0,52],
                y=[wof_lf_yearmean, wof_lf_yearmean],
                name="Annual mean",
                line=dict(color="#ef4444", width=2, dash="dot")
            )
        )

        apply_layout(
            fig_input[key + 'plot 2'],
            title="Load factor — offshore wind",
            y_title='Load factor',
            x_title="Week",
            legend=True
        )
        fig_input[key + 'plot 2'].add_annotation(
            x=0.5,
            y=wof_lf_yearmean*1.05,
            xref="paper",
            yref="y",
            text=f"Annual mean: {wof_lf_yearmean:.3f}",
            showarrow=False,
            font=dict(color="#ef4444", size=12)
        )
    
        #fig_input[key].write_html(current_path + '/out/' + name_simulation + '/input' + '/' + key + '.html')
    
    ##### Eolien Onshore ## 
    
        fig_input[key + 'plot 3'] = go.Figure()
        fig_input[key + 'plot 3'].add_trace(go.Scatter(x=list(range(1, len(pv_lf_weekmean))), y=np.array(pv_lf_weekmean), mode='lines', name="Weekly mean", line=dict(width=2)))

        fig_input[key + 'plot 3'].add_trace(
            go.Scatter(
                x=[0, len(pv_lf_weekmean)],
                y=[pv_lf_yearmean, pv_lf_yearmean],
                name="Annual mean",
                line=dict(color="#ef4444", width=2, dash="dot")
            )
        )

        apply_layout(
            fig_input[key + 'plot 3'],
            title="Load factor — PV",
            y_title='Load factor',
            x_title="Week",
            legend=True
        )
        fig_input[key + 'plot 3'].add_annotation(
            x=0.5,
            y=pv_lf_yearmean*1.05,
            xref="paper",
            yref="y",
            text=f"Annual mean: {pv_lf_yearmean:.3f}",
            showarrow=False,
            font=dict(color="#ef4444", size=12)
        )
     
        #fig_input[key].write_html(current_path + '/out/' + name_simulation + '/input' + '/' + key + '.html')
        
    ################# Nuclear Historic ###########
    
    key = 'nuclear_hist'
    if Display_input[key] :
        
        fig_input[key] = go.Figure()

        fig_input[key].add_trace(
            go.Scatter(
                x=list(pt_nuclear_hist.get_P().keys()),
                y=list(pt_nuclear_hist.get_P().values()),
                line=dict(width=2.0),
                mode='lines'
            )
        )
        apply_layout(fig_input[key], title="Historic nuclear capacity", y_title='Capacity (GW)', x_title="Year")
        