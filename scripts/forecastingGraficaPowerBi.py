import pandas as pd
import matplotlib.pyplot as plt
from pmdarima.arima import auto_arima, ADFTest

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

# modelo
modelo = auto_arima(
    df["Ventas"],  # 🔥 importante: pasar solo la serie, no todo el df
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
    suppress_warnings=True,  # 🔥 estaba mal escrito
    stepwise=True,
    random_state=20,
    n_fits=50
)

# forecast futuro
forecast = modelo.predict(n_periods=20)

future_dates = pd.date_range(
    start=df.index[-1] + pd.offsets.MonthBegin(1),
    periods=20,
    freq="MS"
)

forecast_df = pd.DataFrame(
    {"Forecast": forecast},
    index=future_dates
)

# ----------- GRÁFICO BONITO -----------
plt.figure(figsize=(10, 5))

# histórico
plt.plot(
    df.index,
    df["Ventas"],
    label="Histórico",
    linewidth=2
)

# forecast
plt.plot(
    forecast_df.index,
    forecast_df["Forecast"],
    linestyle="--",
    linewidth=2,
    label="Pronóstico"
)

# sombrear zona de forecast
plt.axvspan(
    forecast_df.index[0],
    forecast_df.index[-1],
    alpha=0.1
)

# título y labels
plt.title("Pronóstico de Ventas (ARIMA)", fontsize=12)
plt.xlabel("Fecha")
plt.ylabel("Ventas")

# grid suave
plt.grid(alpha=0.3)

# leyenda
plt.legend()

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()