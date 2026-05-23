# 'dataset' holds the input data for this script
import pandas as pd
from pmdarima.arima import auto_arima

df = dataset.copy()

df["Periodo"] = pd.to_datetime(df["Periodo"])

if "Sum of Total_Ventas" in df.columns:
    df = df.rename(columns={"Sum of Total_Ventas": "Ventas"})
elif "Total_Ventas" in df.columns:
    df = df.rename(columns={"Total_Ventas": "Ventas"})

df = df[["Periodo", "Ventas"]]
df = df.groupby("Periodo", as_index=False)["Ventas"].sum()
df = df.sort_values("Periodo")
df = df.set_index("Periodo")

modelo = auto_arima(
    df["Ventas"],
    start_p=0,
    d=1,
    start_q=0,
    max_p=5,
    max_d=5,
    max_q=5,
    start_P=0,
    D=1,
    start_Q=0,
    max_P=5,
    max_D=5,
    max_Q=5,
    m=12,
    seasonal=True,
    error_action="warn",
    trace=False,
    suppress_warnings=True,
    stepwise=True,
    random_state=20,
    n_fits=50
)

forecast = modelo.predict(n_periods=20)

future_dates = pd.date_range(
    start=df.index[-1] + pd.offsets.MonthBegin(1),
    periods=20,
    freq="MS"
)

forecast_df = pd.DataFrame({"Ventas": forecast}, index=future_dates)

df["Tipo_Data"] = "Histórico"
df["Indicador"] = "🔵"

forecast_df["Tipo_Data"] = "Forecast"
forecast_df["Indicador"] = "🟠"

tabla_final = pd.concat([df, forecast_df])
tabla_final = tabla_final.reset_index()
tabla_final.columns = ["Periodo", "Ventas", "Tipo_Data", "Indicador"]

tabla_final