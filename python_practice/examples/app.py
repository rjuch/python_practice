import dash
from dash import html, dcc, Input, Output, State
import numpy as np
import pandas as pd
from scipy.stats import norm
import plotly.graph_objs as go

# Pricing functions
def bs_price(S, K, T, r, q, sigma, option_type):
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if option_type == 'call':
        return np.exp(-q * T) * S * norm.cdf(d1) - np.exp(-r * T) * K * norm.cdf(d2)
    return np.exp(-r * T) * K * norm.cdf(-d2) - np.exp(-q * T) * S * norm.cdf(-d1)

def bs_greeks(S, K, T, r, q, sigma, option_type):
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    pdf = norm.pdf(d1)
    if option_type == 'call':
        delta = np.exp(-q * T) * norm.cdf(d1)
        theta = (-S * sigma * np.exp(-q * T) * pdf / (2 * np.sqrt(T))
                 - r * K * np.exp(-r * T) * norm.cdf(d2)
                 + q * S * np.exp(-q * T) * norm.cdf(d1))
    else:
        delta = -np.exp(-q * T) * norm.cdf(-d1)
        theta = (-S * sigma * np.exp(-q * T) * pdf / (2 * np.sqrt(T))
                 + r * K * np.exp(-r * T) * norm.cdf(-d2)
                 - q * S * np.exp(-q * T) * norm.cdf(-d1))
    gamma = np.exp(-q * T) * pdf / (S * sigma * np.sqrt(T))
    vega = S * np.exp(-q * T) * pdf * np.sqrt(T)
    rho = (1 if option_type=='call' else -1) * K * T * np.exp(-r * T) * norm.cdf(d2 if option_type=='call' else -d2)
    return {'Delta': delta, 'Gamma': gamma, 'Vega': vega, 'Theta': theta, 'Rho': rho}

# Monte Carlo functions for non-vanilla
def mc_digital(S, K, T, r, q, sigma, option_type, n_paths=100000):
    Z = np.random.randn(n_paths)
    ST = S * np.exp((r - q - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)
    pay = (ST > K).astype(float) if option_type=='call' else (ST < K).astype(float)
    return np.exp(-r * T) * pay.mean()

def mc_barrier_down_out(S, K, B, T, r, q, sigma, n_paths=50000, n_steps=50):
    dt = T / n_steps
    drift = (r - q - 0.5 * sigma**2) * dt
    diffusion = sigma * np.sqrt(dt)
    payoffs = []
    for _ in range(n_paths):
        path = S * np.exp(np.cumsum(drift + diffusion * np.random.randn(n_steps)))
        payoffs.append(max(path[-1] - K, 0) if path.min()>B else 0)
    return np.exp(-r * T) * np.mean(payoffs)

def mc_asian(S, K, T, r, q, sigma, option_type, n_paths=50000, n_steps=50):
    dt = T / n_steps
    drift = (r - q - 0.5 * sigma**2) * dt
    diffusion = sigma * np.sqrt(dt)
    payoffs = []
    for _ in range(n_paths):
        path = S * np.exp(np.cumsum(drift + diffusion * np.random.randn(n_steps)))
        avg = path.mean()
        payoffs.append(max(avg-K,0) if option_type=='call' else max(K-avg,0))
    return np.exp(-r * T) * np.mean(payoffs)

# Payoff data for plotting
def payoff_data(S0, K, option_key, B=None):
    S = np.linspace(0.5*S0, 1.5*S0, 200)
    if option_key in ['vanilla_call','vanilla_put']:
        payoff = np.maximum(S-K,0) if 'call' in option_key else np.maximum(K-S,0)
    elif option_key in ['digital_call','digital_put']:
        payoff = (S>K).astype(int) if 'call' in option_key else (S<K).astype(int)
    elif option_key=='barrier':
        payoff = np.where(S> B, np.maximum(S-K,0),0)
    else: # asian approx as vanilla for diagram
        payoff = np.maximum(S-K,0) if 'call' in option_key else np.maximum(K-S,0)
    return S, payoff

# Dash App
def serve_layout():
    return html.Div([
        html.H2('Option Pricing Dashboard'),
        dcc.Dropdown(
            id='opt-type',
            options=[
                {'label':'Vanilla Call','value':'vanilla_call'},
                {'label':'Vanilla Put','value':'vanilla_put'},
                {'label':'Digital Call','value':'digital_call'},
                {'label':'Digital Put','value':'digital_put'},
                {'label':'Barrier Down-and-Out','value':'barrier'},
                {'label':'Asian Call','value':'asian_call'},
                {'label':'Asian Put','value':'asian_put'}
            ], value='vanilla_call'
        ),
        html.Div([html.Label(p), dcc.Input(id=p, type='number', value=default, debounce=True)]
                 for p, default in [('S',100),( 'K',100),('T',1),( 'r',0.05),('q',0),( 'sigma',0.2)]),
        html.Div(id='barrier-input'),
        html.Button('Price', id='price-btn'),
        html.Div(id='output-price'),
        dcc.Graph(id='payoff-graph'),
        html.H4('Greeks'),
        html.Div(id='greeks-table')
    ], style={'width':'50%','margin':'auto'})

app = dash.Dash(__name__)
app.layout = serve_layout

# Show barrier field conditionally
@app.callback(
    Output('barrier-input','children'),
    Input('opt-type','value')
)
def show_barrier(opt):
    if opt=='barrier': return [html.Label('Barrier B'), dcc.Input(id='B', type='number', value=90, debounce=True)]
    return []

# Main pricing callback
@app.callback(
    [Output('output-price','children'),
     Output('greeks-table','children'),
     Output('payoff-graph','figure')],
    Input('price-btn','n_clicks'),
    [State('opt-type','value')] +
    [State(p,'value') for p in ['S','K','T','r','q','sigma','B']]
)
def update_output(n, opt, S,K,T,r,q,sigma,B):
    if not n: return ['','',{}]
    key = opt
    if 'vanilla' in key:
        direction= key.split('_')[1]
        price = bs_price(S,K,T,r,q,sigma,direction)
        greeks= bs_greeks(S,K,T,r,q,sigma,direction)
    elif 'digital' in key:
        direction= key.split('_')[1]
        price = mc_digital(S,K,T,r,q,sigma,direction)
        greeks={}
    elif key=='barrier':
        price = mc_barrier_down_out(S,K,B,T,r,q,sigma)
        greeks={}
    else:
        direction='call' if 'call' in key else 'put'
        price = mc_asian(S,K,T,r,q,sigma,direction)
        greeks={}
    price_str= f'Price: {price:.4f}'
    # Greeks
    table = []
    if greeks:
        df=pd.DataFrame.from_dict(greeks,orient='index',columns=['Value'])
        table = html.Table([html.Tr([html.Th(idx), html.Td(f"{val:.4f}")]) for idx,val in greeks.items()])
    # Payoff
    Sgrid, payoff= payoff_data(S,K,key,B)
    fig=go.Figure(data=go.Scatter(x=Sgrid, y=payoff, mode='lines'))
    fig.update_layout(xaxis_title='Underlying S', yaxis_title='Payoff')
    return price_str, table, fig

if __name__=='__main__':
    app.run(debug=True)
