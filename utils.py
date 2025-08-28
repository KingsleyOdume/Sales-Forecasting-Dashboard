import pandas as pd
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.metrics import mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt
import io
import plotly.graph_objects as go


def load_sales(csv_file_or_df):
    if isinstance(csv_file_or_df, pd.DataFrame):
        df = csv_file_or_df.copy()
    else:
        df = pd.read_csv(csv_file_or_df)
    # Expect columns: date, amount (case-insensitive)
    df.columns = [c.lower() for c in df.columns]
    if 'date' not in df.columns or 'amount' not in df.columns:
        raise ValueError('CSV must contain `date` and `amount` columns')
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    return df


def aggregate_monthly(df):
    df = df.set_index('date')
    monthly = df['amount'].resample('MS').sum().to_frame()
    monthly = monthly.reset_index()
    monthly.columns = ['date', 'amount']
    return monthly


def train_test_split(ts_df, test_periods=12):
    if len(ts_df) <= test_periods + 6:
        raise ValueError('Not enough data for that many test periods')
    train = ts_df.iloc[:-test_periods].copy()
    test = ts_df.iloc[-test_periods:].copy()
    return train, test


def fit_hw(train_series, seasonal_periods=12, trend='add', seasonal='add'):
    # Returns fitted model and forecast for length
    model = ExponentialSmoothing(train_series, trend=trend, seasonal=seasonal, seasonal_periods=seasonal_periods)
    fit = model.fit(optimized=True)
    return fit


def forecast_with_model(fit, steps):
    return fit.forecast(steps)


def evaluate_forecast(true, pred):
    mae = mean_absolute_error(true, pred)
    rmse = np.sqrt(mean_squared_error(true, pred))   # instead of squared=False
    return {'mae': float(mae), 'rmse': float(rmse)}



def make_plotly_history_forecast(ts_df, forecast_df, title='Sales & Forecast'):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=ts_df['date'], y=ts_df['amount'], name='Historical', mode='lines+markers'))
    fig.add_trace(go.Scatter(x=forecast_df['date'], y=forecast_df['forecast'], name='Forecast', mode='lines+markers'))
    if 'lower' in forecast_df.columns and 'upper' in forecast_df.columns:
        fig.add_trace(go.Scatter(x=forecast_df['date'].tolist() + forecast_df['date'][::-1].tolist(),
        y=forecast_df['upper'].tolist() + forecast_df['lower'][::-1].tolist(),
        fill='toself', fillcolor='rgba(0,100,80,0.2)', line=dict(color='rgba(255,255,255,0)'),
        hoverinfo='skip', showlegend=False, name='Confidence'))
    fig.update_layout(title=title, xaxis_title='Date', yaxis_title='Sales')
    return fig


def matplotlib_summary_plot(ts_df):
    fig, ax = plt.subplots(figsize=(8,3))
    ax.plot(ts_df['date'], ts_df['amount'], marker='o')
    ax.set_title('Monthly Sales')
    ax.set_xlabel('Date')
    ax.set_ylabel('Sales')
    plt.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    return buf