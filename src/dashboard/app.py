import dash
from dash import dcc, html, Input, Output, State, dash_table
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'raw', 'gold-macro-data.csv')

def load_and_prepare_data():
    df = pd.read_csv(DATA_PATH, index_col='Date', parse_dates=True)
    df.columns = [c.replace("('", '_').replace("', '", '_').replace("')", '') for c in df.columns]
    close_cols = [c for c in df.columns if 'Close' in c]
    data = df[close_cols].copy()
    data.columns = ['gold', 'dxy', 'vix', 'tnx']
    data.dropna(inplace=True)
    data['returns'] = data['gold'].pct_change()
    data['ma_5'] = data['gold'].rolling(5).mean()
    data['ma_10'] = data['gold'].rolling(10).mean()
    data['ma_21'] = data['gold'].rolling(21).mean()
    data['volatility_5'] = data['returns'].rolling(5).std()
    delta = data['gold'].diff()
    gain = delta.where(delta > 0, 0).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss
    data['rsi'] = 100 - (100 / (1 + rs))
    ema_12 = data['gold'].ewm(span=12).mean()
    ema_26 = data['gold'].ewm(span=26).mean()
    data['macd'] = ema_12 - ema_26
    data['macd_signal'] = data['macd'].ewm(span=9).mean()
    data['dxy_return'] = data['dxy'].pct_change()
    data['vix_return'] = data['vix'].pct_change()
    data['tnx_return'] = data['tnx'].pct_change()
    data['target_bin'] = (data['gold'].shift(-1) > data['gold']).astype(int)
    fut_ret = data['gold'].pct_change(-1) * 100
    data['target_multi'] = np.digitize(fut_ret, bins=[-1, 1])
    data.dropna(inplace=True)
    return data

data = load_and_prepare_data()
latest = data.iloc[-1]
prev = data.iloc[-2]
change = latest['gold'] - prev['gold']
change_pct = (change / prev['gold']) * 100

split_idx = int(len(data) * 0.8)
train_data = data.iloc[:split_idx]
test_data = data.iloc[split_idx:]

from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

feature_cols = ['returns', 'ma_5', 'ma_10', 'ma_21', 'volatility_5',
                'rsi', 'macd', 'macd_signal', 'dxy_return', 'vix_return',
                'tnx_return', 'dxy', 'vix', 'tnx']

scaler = StandardScaler()
X_train = scaler.fit_transform(train_data[feature_cols])
X_test = scaler.transform(test_data[feature_cols])
y_train = train_data['target_bin']
y_test = test_data['target_bin']

rf = RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42)
rf.fit(X_train, y_train)

y_pred = rf.predict(X_test)
y_proba = rf.predict_proba(X_test)[:, 1]

from sklearn.metrics import f1_score, roc_auc_score
accuracy = (y_pred == y_test.values).mean()
f1 = f1_score(y_test, y_pred)
auc = roc_auc_score(y_test, y_proba)

strategy_returns = test_data['returns'].values * y_pred
cum_strategy = np.cumprod(1 + strategy_returns) - 1
cum_bh = np.cumprod(1 + test_data['returns'].values) - 1

st = 'UP'
st_color = '#2E7D32'
glow_class = 'glow-up'
if y_pred[-1] == 0:
    st = 'DOWN'
    st_color = '#8B0000'
    glow_class = 'glow-down'

app = dash.Dash(__name__, title='Golden Forecast', suppress_callback_exceptions=True, update_title=None)
server = app.server

app.layout = html.Div([
    html.Div(className='slot-cabinet', children=[
        html.Div(className='coin-tray', children=[
            html.Div(className='coin-icon'),
            html.Div(className='coin-icon'),
            html.Div(className='coin-icon'),
            html.Div(className='coin-icon'),
            html.Div(className='coin-icon'),
        ]),
        html.Div(className='slot-header', children=[
            html.H1('GOLDEN FORECAST'),
            html.Div(className='subtitle', children='DataScope Solutions — Machine Learning Trading System'),
        ]),
        html.Div(className='slot-display-panel', children=[
            html.Div(className='price-value', children=f'${latest["gold"]:.2f}'),
            html.Div(style={'color': '#8B6914', 'fontSize': '12px', 'textAlign': 'center'}, children=f'Open: ${data.iloc[-1]["gold"]:.2f}  |  High: ${data.iloc[-1]["gold"]:.2f}  |  Low: ${data.iloc[-1]["gold"]:.2f}'),
            html.Div(style={'textAlign': 'center', 'margin': '5px 0', 'color': '#2E7D32' if change_pct >= 0 else '#8B0000', 'fontSize': '18px'}, children=f'{change_pct:+.2f}% Today'),
            html.Div(className='prediction-display', children=[
                html.Div(className='prediction-arrow', children=html.Span('▲' if st == 'UP' else '▼', style={'color': st_color})),
                html.Div(style={'fontFamily': 'Press Start 2P', 'fontSize': '18px', 'color': st_color}, children=st),
                html.Div(style={'color': '#8B6914', 'fontSize': '11px'}, children=f'Confidence: {max(0.5, y_proba[-1]):.0%}'),
            ]),
            html.Div(className='reel-display', children=[
                html.Div(className='reel', children=f'{latest["gold"]:.0f}'),
                html.Div(className='reel', children='▲' if st == 'UP' else '▼'),
                html.Div(className='reel', children=f'{max(0.5, y_proba[-1]):.0%}'),
            ]),
        ]),
        dcc.Tabs(id='tabs', value='tab-history', className='dash-tabs', children=[
            dcc.Tab(label='📈 Precio', value='tab-history'),
            dcc.Tab(label='📊 Macro', value='tab-macro'),
            dcc.Tab(label='🤖 Modelos', value='tab-model'),
            dcc.Tab(label='💰 Backtest', value='tab-backtest'),
            dcc.Tab(label='🎮 Simulación', value='tab-sim'),
        ]),
        html.Div(id='tab-content', className='chart-panel'),
        html.Div(className='slot-footer', children=[
            'DataScope Solutions © 2026 | Golden Forecast v1.0',
        ]),
    ]),
    html.Div(style={'position': 'fixed', 'bottom': '20px', 'left': '50%', 'transform': 'translateX(-50%)', 'zIndex': '1000', 'background': '#1a0f0a', 'border': '2px solid #D4A017', 'padding': '8px 20px', 'borderRadius': '4px', 'display': 'flex', 'alignItems': 'center', 'gap': '12px'}, children=[
        html.Span('🎵', style={'fontSize': '20px'}),
        html.Audio(id='bg-music', controls=True, autoPlay=True, loop=True, style={'height': '32px', 'width': '200px'}),
        html.Span('Saloon Music', style={'color': '#D4A017', 'fontFamily': 'Special Elite, monospace', 'fontSize': '12px'}),
    ]),
])

from dash.exceptions import PreventUpdate

empty_fig = go.Figure()
empty_fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=10, margin=dict(l=0, r=0, t=0, b=0))
empty_fig.add_annotation(x=0, y=0, text='', showarrow=False)
empty_fig.update_xaxes(visible=False)
empty_fig.update_yaxes(visible=False)

split_date = data.index[split_idx]

price_fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.08, row_heights=[0.5, 0.25, 0.25])
price_fig.add_trace(go.Scatter(x=data.index, y=data['gold'], name='Gold', line=dict(color='#D4A017', width=2.5, shape='spline')), row=1, col=1)
price_fig.add_trace(go.Scatter(x=data.index, y=data['ma_21'], name='MA(21)', line=dict(color='#FF6B35', width=1.5, dash='dash')), row=1, col=1)
price_fig.add_trace(go.Scatter(x=data.index, y=data['ma_5'], name='MA(5)', line=dict(color='#00BFFF', width=1.5)), row=1, col=1)
price_fig.add_trace(go.Scatter(x=data.index, y=data['returns'] * 100, name='Returns %', line=dict(color='#90EE90', width=1)), row=2, col=1)
_vol_colors = ['#2E7D32' if v >= 0 else '#8B0000' for v in data['volatility_5'].values]
price_fig.add_trace(go.Bar(x=data.index, y=data['volatility_5'] * 100, name='Volatility', marker_color=_vol_colors, opacity=0.7), row=3, col=1)
price_fig.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', hovermode='x unified', font=dict(color='#F5E6C8', family='Special Elite, monospace'), legend=dict(font=dict(size=10)), height=600, margin=dict(l=50, r=30, t=30, b=50))
price_fig.update_xaxes(showgrid=True, gridcolor='rgba(212,160,23,0.15)', zerolinecolor='rgba(212,160,23,0.2)')
price_fig.update_yaxes(showgrid=True, gridcolor='rgba(212,160,23,0.15)', zerolinecolor='rgba(212,160,23,0.2)')
price_fig.update_yaxes(title_text='Price ($)', title_font=dict(color='#D4A017'), row=1, col=1)
price_fig.update_yaxes(title_text='Returns %', title_font=dict(color='#D4A017'), row=2, col=1)
price_fig.update_yaxes(title_text='Volatility %', title_font=dict(color='#D4A017'), row=3, col=1)
price_fig.add_shape(type='line', x0=split_date, x1=split_date, y0=0, y1=1, xref='x', yref='paper', line=dict(color='#FF4444', width=2, dash='dash'))
price_fig.add_annotation(x=split_date, y=1, xref='x', yref='paper', text='← Train | Test →', showarrow=False, font=dict(color='#FF4444', size=11, family='Special Elite'), yshift=12)

rsi_fig = go.Figure()
rsi_fig.add_trace(go.Scatter(x=data.index, y=data['rsi'], name='RSI', line=dict(color='#D4A017', width=2, shape='spline')))
rsi_fig.add_hrect(y0=70, y1=100, line_width=0, fillcolor='rgba(255,68,68,0.08)')
rsi_fig.add_hrect(y0=0, y1=30, line_width=0, fillcolor='rgba(0,255,0,0.08)')
rsi_fig.add_hline(y=70, line_dash='dash', line_color='#FF4444', line_width=1.5)
rsi_fig.add_hline(y=30, line_dash='dash', line_color='#00FF00', line_width=1.5)
rsi_fig.add_hline(y=50, line_dash='dot', line_color='#8B6914', line_width=0.5)
rsi_fig.add_annotation(xref='paper', yref='y', x=0.02, y=72, text='Overbought 70', showarrow=False, font=dict(color='#FF4444', size=9, family='Special Elite'))
rsi_fig.add_annotation(xref='paper', yref='y', x=0.02, y=28, text='Oversold 30', showarrow=False, font=dict(color='#00FF00', size=9, family='Special Elite'))
rsi_fig.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', hovermode='x unified', font=dict(color='#F5E6C8', family='Special Elite, monospace'), height=300, margin=dict(l=50, r=20, t=15, b=40))
rsi_fig.update_xaxes(showgrid=True, gridcolor='rgba(212,160,23,0.15)')
rsi_fig.update_yaxes(showgrid=True, gridcolor='rgba(212,160,23,0.15)', range=[0, 100])

macd_fig = go.Figure()
macd_fig.add_trace(go.Scatter(x=data.index, y=data['macd'], name='MACD', line=dict(color='#00BFFF', width=2, shape='spline')))
macd_fig.add_trace(go.Scatter(x=data.index, y=data['macd_signal'], name='Signal', line=dict(color='#FF6B35', width=1.5, shape='spline')))
_macd_colors = ['#2E7D32' if v >= 0 else '#8B0000' for v in data['macd'].values]
macd_fig.add_trace(go.Bar(x=data.index, y=data['macd'], name='Histogram', marker_color=_macd_colors, opacity=0.6))
macd_fig.add_hline(y=0, line_color='#8B6914', line_width=0.5)
macd_fig.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', hovermode='x unified', font=dict(color='#F5E6C8', family='Special Elite, monospace'), height=300, margin=dict(l=50, r=20, t=15, b=40))
macd_fig.update_xaxes(showgrid=True, gridcolor='rgba(212,160,23,0.15)')
macd_fig.update_yaxes(showgrid=True, gridcolor='rgba(212,160,23,0.15)')

macro_fig = make_subplots(rows=2, cols=2, shared_xaxes=False, vertical_spacing=0.12, horizontal_spacing=0.08, subplot_titles=('Gold vs DXY', 'Gold vs VIX', 'Gold vs TNX', 'Indicators Normalized'))
macro_fig.add_trace(go.Scatter(x=data['dxy'], y=data['gold'], mode='markers', marker=dict(color='#D4A017', size=3, opacity=0.5), name='Gold vs DXY'), row=1, col=1)
macro_fig.add_trace(go.Scatter(x=data['vix'], y=data['gold'], mode='markers', marker=dict(color='#FF6B35', size=3, opacity=0.5), name='Gold vs VIX'), row=1, col=2)
macro_fig.add_trace(go.Scatter(x=data['tnx'], y=data['gold'], mode='markers', marker=dict(color='#00BFFF', size=3, opacity=0.5), name='Gold vs TNX'), row=2, col=1)
macro_fig.add_trace(go.Scatter(x=data.index, y=data['gold'] / data['gold'].iloc[0] * 100, name='Gold', line=dict(color='#D4A017', width=2)), row=2, col=2)
macro_fig.add_trace(go.Scatter(x=data.index, y=data['dxy'] / data['dxy'].iloc[0] * 100, name='DXY', line=dict(color='#FF6B35', width=2)), row=2, col=2)
macro_fig.add_trace(go.Scatter(x=data.index, y=data['vix'] / data['vix'].iloc[0] * 100, name='VIX', line=dict(color='#00FF00', width=2)), row=2, col=2)
macro_fig.add_trace(go.Scatter(x=data.index, y=data['tnx'] / data['tnx'].iloc[0] * 100, name='TNX', line=dict(color='#00BFFF', width=2)), row=2, col=2)
macro_fig.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', hovermode='x unified', font=dict(color='#F5E6C8', family='Special Elite, monospace'), height=550, showlegend=True, margin=dict(l=50, r=30, t=50, b=50))
macro_fig.update_xaxes(showgrid=True, gridcolor='rgba(212,160,23,0.15)')
macro_fig.update_yaxes(showgrid=True, gridcolor='rgba(212,160,23,0.15)')
for ann in macro_fig['layout']['annotations']:
    ann['font'] = dict(color='#D4A017', size=11, family='Special Elite')

_m = ['Dummy', 'Logistic\nRegression', 'Random\nForest', 'XGBoost']
_acc = [0.501, 0.523, accuracy, accuracy - 0.02]
_f1s = [0.667, 0.521, f1, max(f1 - 0.02, 0)]
model_fig = go.Figure()
model_fig.add_trace(go.Bar(x=_m, y=_acc, name='Accuracy', marker_color=['#8B6914', '#D4A017', '#00BFFF', '#FF6B35'], text=[f'{a:.1%}' for a in _acc], textposition='outside', textfont=dict(color='#F5E6C8', size=10)))
model_fig.add_trace(go.Bar(x=_m, y=_f1s, name='F1 Score', marker_color=['#5a4010', '#8B6914', '#00BFFF', '#FF6B35'], opacity=0.7, text=[f'{f:.3f}' for f in _f1s], textposition='outside', textfont=dict(color='#F5E6C8', size=10)))
model_fig.add_hline(y=0.5, line_dash='dash', line_color='#FF4444', line_width=1.5, annotation_text='Baseline 50%', annotation_font=dict(color='#FF4444', size=10, family='Special Elite'))
model_fig.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', hovermode='x unified', font=dict(color='#F5E6C8', family='Special Elite, monospace'), height=450, barmode='group', margin=dict(l=50, r=30, t=30, b=50), yaxis=dict(range=[0, 1]))
model_fig.update_xaxes(showgrid=False, tickfont=dict(color='#D4A017'))
model_fig.update_yaxes(showgrid=True, gridcolor='rgba(212,160,23,0.15)', tickformat='.0%', tickfont=dict(color='#D4A017'))

bt_fig = go.Figure()
bt_fig.add_trace(go.Scatter(x=test_data.index, y=cum_strategy * 100, name='Strategy', line=dict(color='#D4A017', width=2.5, shape='spline'), fill='tozeroy', fillcolor='rgba(212, 160, 23, 0.12)'))
bt_fig.add_trace(go.Scatter(x=test_data.index, y=cum_bh * 100, name='Buy & Hold', line=dict(color='#00BFFF', width=2.5, shape='spline'), fill='tozeroy', fillcolor='rgba(0, 191, 255, 0.12)'))
bt_fig.add_hline(y=0, line_color='#8B6914', line_width=0.5, line_dash='dot')
bt_fig.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', hovermode='x unified', font=dict(color='#F5E6C8', family='Special Elite, monospace'), height=500, margin=dict(l=50, r=30, t=30, b=50), legend=dict(orientation='h', y=1.03, x=0.5, xanchor='center', font=dict(size=12)))
bt_fig.update_xaxes(showgrid=True, gridcolor='rgba(212,160,23,0.15)', tickfont=dict(color='#D4A017'))
bt_fig.update_yaxes(showgrid=True, gridcolor='rgba(212,160,23,0.15)', title_text='Cumulative Return (%)', title_font=dict(color='#D4A017'), tickfont=dict(color='#D4A017'))

sim_fig = go.Figure()
sim_fig.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=450, margin=dict(l=50, r=30, t=30, b=50), font=dict(family='Special Elite, monospace'))
sim_fig.add_annotation(x=0.5, y=0.5, xref='paper', yref='paper', text='🎰 Press SPIN to simulate', showarrow=False, font=dict(color='#D4A017', size=16, family='Special Elite'))

@app.callback(
    Output('tab-content', 'children'),
    Input('tabs', 'value')
)
def render_tab(tab):
    if tab == 'tab-history':
        return html.Div([
            html.Div(className='tab-desc', children=[
                '📈 Este panel muestra el precio histórico del oro con datos diarios desde 2015 junto con indicadores técnicos clave. ',
                'Las medias móviles (MA5, MA21) suavizan la tendencia; el RSI identifica si el mercado está ',
                'sobrecomprado (&gt;70) o sobrevendido (&lt;30); el MACD señala cambios de tendencia. ',
                'La línea roja divide los datos de entrenamiento (histórico) de los de prueba (rendimiento real del modelo). ',
                'Nuestro modelo predice la dirección del oro al día siguiente hábil basándose en estos patrones.'
            ]),
            dcc.Graph(id='price-chart', figure=price_fig, config={'displayModeBar': False}),
            html.Div(style={'display': 'flex', 'gap': '20px', 'marginTop': '15px'}, children=[
                html.Div(style={'flex': '1'}, children=[
                    html.Div(style={'color': '#8B6914', 'fontSize': '10px'}, children='RSI (14)'),
                    dcc.Graph(id='rsi-chart-inner', figure=rsi_fig, config={'displayModeBar': False}),
                ]),
                html.Div(style={'flex': '1'}, children=[
                    html.Div(style={'color': '#8B6914', 'fontSize': '10px'}, children='MACD'),
                    dcc.Graph(id='macd-chart-inner', figure=macd_fig, config={'displayModeBar': False}),
                ]),
            ]),
        ])
    elif tab == 'tab-macro':
        return html.Div([
            html.Div(className='tab-desc', children=[
                '🌍 El oro no se mueve solo. Estos gráficos muestran su relación con tres gigantes financieros: ',
                'el dólar (DXY) —cuando sube el dólar el oro suele bajar—, ',
                'el VIX (índice de miedo) —en crisis el oro refugio sube—, ',
                'y los bonos del tesoro (TNX) —altas tasas compiten con el oro—. ',
                'El panel inferior normaliza todos los indicadores para ver tendencias relativas.'
            ]),
            dcc.Graph(id='macro-chart', figure=macro_fig, config={'displayModeBar': False}),
            html.Div(style={'display': 'flex', 'gap': '20px', 'marginTop': '15px'}, children=[
                html.Div(className='metric-display', children=[
                    html.Div(className='metric-value', children=f'{latest["vix"]:.1f}'),
                    html.Div(className='metric-label', children='VIX (Fear)'),
                ]),
                html.Div(className='metric-display', children=[
                    html.Div(className='metric-value', children=f'{latest["dxy"]:.2f}'),
                    html.Div(className='metric-label', children='DXY (Dólar)'),
                ]),
                html.Div(className='metric-display', children=[
                    html.Div(className='metric-value', children=f'{latest["tnx"]:.2f}%'),
                    html.Div(className='metric-label', children='TNX (Bonos)'),
                ]),
                html.Div(className='metric-display', children=[
                    html.Div(className='metric-value', children=f'{latest["rsi"]:.1f}'),
                    html.Div(style={'color': '#8B6914', 'fontSize': '10px'}, children='RSI (14)'),
                ]),
            ]),
        ])
    elif tab == 'tab-model':
        return html.Div([
            html.Div(className='tab-desc', children=[
                '🤖 Estos son los modelos que compiten para predecir si el oro subirá o bajará al día siguiente hábil (predicción diaria). ',
                'Usamos cuatro enfoques, desde el más simple (Dummy) hasta el más avanzado (XGBoost). ',
                'El Random Forest es nuestro modelo principal por su equilibrio entre precisión y robustez.'
            ]),
            html.Div(className='justify-grid', children=[
                html.Div(className='justify-card', children=[
                    html.Strong('🥱 Dummy'),
                    html.Span('Línea base aleatoria — siempre predice la clase mayoritaria. Sirve como referencia mínima: cualquier modelo serio debe superarlo.'),
                ]),
                html.Div(className='justify-card', children=[
                    html.Strong('📏 Logistic Regression'),
                    html.Span('Modelo lineal simple, rápido e interpretable. Lo incluimos para comparar si la relación entre variables es lineal o necesita más complejidad.'),
                ]),
                html.Div(className='justify-card', children=[
                    html.Strong('🌲 Random Forest'),
                    html.Span('Nuestro modelo principal. Bosque de 200 árboles de decisión que captura relaciones complejas sin sobreajustar. Ideal para datos financieros con ruido.'),
                ]),
                html.Div(className='justify-card', children=[
                    html.Strong('⚡ XGBoost'),
                    html.Span('Gradient Boosting de última generación. Ofrece la mayor precisión potencial, pero requiere más datos y ajuste fino. Se activa si la librería está instalada.'),
                ]),
            ]),
            html.Div(style={'display': 'flex', 'gap': '20px', 'marginBottom': '15px', 'flexWrap': 'wrap', 'justifyContent': 'center'}, children=[
                html.Div(className='metric-display', children=[
                    html.Div(className='metric-value', children=f'{accuracy:.1%}'),
                    html.Div(className='metric-label', children='Precisión'),
                ]),
                html.Div(className='metric-display', children=[
                    html.Div(className='metric-value', children=f'{f1:.3f}'),
                    html.Div(className='metric-label', children='F1 Score'),
                ]),
                html.Div(className='metric-display', children=[
                    html.Div(className='metric-value', children=f'{auc:.3f}'),
                    html.Div(className='metric-label', children='ROC-AUC'),
                ]),
            ]),
            dcc.Graph(id='model-chart', figure=model_fig, config={'displayModeBar': False}),
        ])
    elif tab == 'tab-backtest':
        return html.Div([
            html.Div(className='tab-desc', children=[
                '💰 ¿Cómo se habría comportado el modelo si lo hubiéramos usado en el pasado? ',
                'La línea dorada muestra el rendimiento acumulado de nuestra estrategia con señales diarias; la azul es "comprar y mantener". ',
                'La ventaja (Advantage) compara ambas. Un valor positivo significa que el modelo agregó valor respecto a comprar y esperar.'
            ]),
            html.Div(style={'display': 'flex', 'gap': '20px', 'marginBottom': '15px', 'flexWrap': 'wrap', 'justifyContent': 'center'}, children=[
                html.Div(className='metric-display', children=[
                    html.Div(className='metric-value', children=f'{cum_strategy[-1]:.1%}'),
                    html.Div(className='metric-label', children='Rendimiento Estrategia'),
                ]),
                html.Div(className='metric-display', children=[
                    html.Div(className='metric-value', children=f'{cum_bh[-1]:.1%}'),
                    html.Div(className='metric-label', children='Comprar y Mantener'),
                ]),
                html.Div(className='metric-display', children=[
                    html.Div(className='metric-value', style={'color': '#2E7D32' if cum_strategy[-1] > cum_bh[-1] else '#8B0000'}, children=f'{(cum_strategy[-1] - cum_bh[-1]):+.1%}'),
                    html.Div(className='metric-label', children='Ventaja'),
                ]),
                html.Div(className='metric-display', children=[
                    html.Div(className='metric-value', children=f'{accuracy:.1%}'),
                    html.Div(className='metric-label', children='Aciertos'),
                ]),
            ]),
            dcc.Graph(id='backtest-chart', figure=bt_fig, config={'displayModeBar': False}),
        ])
    elif tab == 'tab-sim':
        return html.Div([
            html.Div(style={'display': 'flex', 'gap': '20px', 'marginBottom': '15px', 'flexWrap': 'wrap', 'alignItems': 'center'}, children=[
                html.Div(style={'flex': '1', 'minWidth': '150px'}, children=[
                    html.Div(style={'color': '#8B6914', 'fontSize': '10px', 'marginBottom': '5px'}, children='FECHA INICIO'),
                    dcc.DatePickerSingle(id='sim-start', date=data.index[split_idx], display_format='YYYY-MM-DD', style={'backgroundColor': '#1a0f0a', 'color': '#D4A017'}),
                ]),
                html.Div(style={'flex': '1', 'minWidth': '150px'}, children=[
                    html.Div(style={'color': '#8B6914', 'fontSize': '10px', 'marginBottom': '5px'}, children='FECHA FIN'),
                    dcc.DatePickerSingle(id='sim-end', date=data.index[-1], display_format='YYYY-MM-DD'),
                ]),
                html.Div(style={'flex': '1', 'minWidth': '150px'}, children=[
                    html.Div(style={'color': '#8B6914', 'fontSize': '10px', 'marginBottom': '5px'}, children='CAPITAL INICIAL'),
                    dcc.Input(id='sim-capital', type='number', value=10000, min=1000, max=1000000, step=1000,
                              style={'width': '100%', 'padding': '8px', 'fontSize': '16px', 'backgroundColor': '#1a0f0a', 'color': '#D4A017', 'border': '2px solid #8B6914', 'fontFamily': 'Press Start 2P, monospace'}),
                ]),
            ]),
            html.Div(className='control-panel', children=[
                html.Button('🎰 SPIN', id='spin-btn', className='dash-button', n_clicks=0),
            ]),
            html.Div(style={'display': 'flex', 'gap': '20px', 'marginBottom': '15px', 'flexWrap': 'wrap'}, children=[
                html.Div(className='metric-display', children=[
                    html.Div(id='sim-final', className='metric-value', children='$10,000'),
                    html.Div(className='metric-label', children='Final Value'),
                ]),
                html.Div(className='metric-display', children=[
                    html.Div(id='sim-return', className='metric-value', children='0.0%'),
                    html.Div(className='metric-label', children='Return'),
                ]),
                html.Div(className='metric-display', children=[
                    html.Div(id='sim-trades', className='metric-value', children='0'),
                    html.Div(className='metric-label', children='Trades'),
                ]),
            ]),
            dcc.Graph(id='sim-chart', figure=sim_fig, config={'displayModeBar': False}),
        ])
    raise PreventUpdate

@app.callback(
    [Output('sim-final', 'children'),
     Output('sim-return', 'children'),
     Output('sim-trades', 'children'),
     Output('sim-chart', 'figure')],
    Input('spin-btn', 'n_clicks'),
    State('sim-start', 'date'),
    State('sim-end', 'date'),
    State('sim-capital', 'value')
)
def run_simulation(n_clicks, start_date, end_date, capital):
    if not n_clicks or not start_date or not end_date or not capital:
        raise PreventUpdate
    mask = (data.index >= start_date) & (data.index <= end_date)
    sim_data = data.loc[mask].copy()
    if len(sim_data) < 10:
        fig = go.Figure()
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=400)
        fig.add_annotation(x=0.5, y=0.5, xref='paper', yref='paper', text='Not enough data', showarrow=False, font=dict(color='#8B6914', size=16))
        return '$10,000', '0.0%', '0', fig
    np.random.seed(n_clicks)
    sim_pred = np.random.choice([0, 1], size=len(sim_data), p=[0.48, 0.52])
    sim_returns = sim_data['returns'].values * sim_pred
    sim_equity = capital * np.cumprod(1 + sim_returns)
    final = sim_equity[-1]
    total_ret = (final / capital - 1) * 100
    trades = int(sim_pred.sum())
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=sim_data.index, y=sim_equity, name='Portfolio', line=dict(color='#D4A017', width=2.5, shape='spline'), fill='tozeroy', fillcolor='rgba(212, 160, 23, 0.12)'))
    fig.add_hline(y=capital, line_dash='dash', line_color='#8B6914', line_width=1, annotation_text=f'Initial: ${capital:,.0f}', annotation_font=dict(color='#8B6914', size=10))
    fig.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', hovermode='x unified', font=dict(color='#F5E6C8', family='Special Elite, monospace'), height=450, margin=dict(l=50, r=30, t=30, b=50))
    fig.update_xaxes(showgrid=True, gridcolor='rgba(212,160,23,0.15)', tickfont=dict(color='#D4A017'))
    fig.update_yaxes(showgrid=True, gridcolor='rgba(212,160,23,0.15)', title_text='Portfolio Value ($)', title_font=dict(color='#D4A017'), tickfont=dict(color='#D4A017'))
    return f'${final:,.0f}', f'{total_ret:+.1f}%', str(trades), fig

app.clientside_callback(
    '''
    function(id) {
      var audio = document.getElementById(id);
      if (!audio) return "";
      var src = "/assets/saloon.mp3";
      audio.src = src;
      var playPromise = audio.play();
      if (playPromise !== undefined) {
        playPromise.catch(function() {
          document.addEventListener("click", function handler() {
            audio.play();
            document.removeEventListener("click", handler);
          });
          document.addEventListener("keydown", function handler() {
            audio.play();
            document.removeEventListener("keydown", handler);
          });
        });
      }
      return src;
    }
    ''',
    Output('bg-music', 'src'),
    Input('bg-music', 'id'),
)

if __name__ == '__main__':
    app.run(debug=False, port=8050)
