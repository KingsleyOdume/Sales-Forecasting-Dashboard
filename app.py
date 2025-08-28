import streamlit as st
import pandas as pd
from utils import load_sales, aggregate_monthly, train_test_split, fit_hw, forecast_with_model, evaluate_forecast, make_plotly_history_forecast, matplotlib_summary_plot
import io

st.title('Sales Forecasting Dashboard')
st.markdown('Upload a CSV with columns `date` and `amount` (date format YYYY-MM-DD).')

with st.sidebar:
    st.header('Options')
    uploaded = st.file_uploader('Upload sales CSV', type=['csv'])
    use_sample = st.checkbox('Use sample_sales.csv (generated locally)', value=True)
    test_periods = st.number_input('Test periods (months)', min_value=3, max_value=36, value=12)
    forecast_horizon = st.number_input('Forecast horizon (months)', min_value=1, max_value=36, value=12)

# Load data
if uploaded is not None:
    df = load_sales(uploaded)
elif use_sample:
    try:
        df = load_sales('sample_sales.csv')
    except Exception:
        st.info('Sample data not found. Generating one...')
        import generate_sample_data
        generate_sample_data.generate()
        df = load_sales('sample_sales.csv')
    else:
        st.warning('Please upload a CSV or enable use sample data.')
        st.stop()

monthly = aggregate_monthly(df)
st.subheader('Monthly Sales (aggregated)')
st.dataframe(monthly.tail(50))

# Show matplotlib summary
buf = matplotlib_summary_plot(monthly)
st.image(buf)

# Train/Test split + model
try:
    train, test = train_test_split(monthly, test_periods=test_periods)
except Exception as e:
    st.error(str(e))
    st.stop()

st.subheader('Modeling')
strategy = st.selectbox('Seasonality & Trend model', ['add_add', 'add_mul', 'mul_add', 'mul_mul'])
trend, seasonal = strategy.split('_')
train_series = train.set_index('date')['amount']
model_fit = fit_hw(train_series, seasonal_periods=12, trend=trend, seasonal=seasonal)

# Forecast for test period and horizon
pred_test = forecast_with_model(model_fit, len(test))
metrics = evaluate_forecast(test['amount'].values, pred_test.values)
st.write('Test metrics:', metrics)

# Refit on all data and forecast future
full_fit = fit_hw(monthly.set_index('date')['amount'], seasonal_periods=12, trend=trend, seasonal=seasonal)
future_forecast = forecast_with_model(full_fit, forecast_horizon)
future_index = pd.date_range(start=monthly['date'].iloc[-1] + pd.offsets.MonthBegin(1), periods=forecast_horizon, freq='MS')
forecast_df = pd.DataFrame({'date': future_index, 'forecast': future_forecast.values})

# Plotly figure
fig = make_plotly_history_forecast(monthly, forecast_df)
st.plotly_chart(fig, use_container_width=True)

# Download forecast
csv = forecast_df.to_csv(index=False).encode('utf-8')
st.download_button('Download forecast CSV', data=csv, file_name='forecast.csv', mime='text/csv')

st.info('Done — tweak the options in the sidebar and re-run.')