# 🛒 Data Retail 360

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python">
  <img src="https://img.shields.io/badge/SQL-Server-red?style=for-the-badge&logo=microsoftsqlserver">
  <img src="https://img.shields.io/badge/PowerBI-Dashboard-yellow?style=for-the-badge&logo=powerbi">
  <img src="https://img.shields.io/badge/Pandas-Data_Analysis-purple?style=for-the-badge&logo=pandas">
  <img src="https://img.shields.io/badge/Machine_Learning-Forecasting-green?style=for-the-badge&logo=scikitlearn">
  <img src="https://img.shields.io/badge/Status-Completed-success?style=for-the-badge">
</p>

---

# 📌 Overview

**Data Retail 360** es una solución integral de analítica de datos orientada al sector retail, diseñada para transformar datos transaccionales en información estratégica para la toma de decisiones.

Este proyecto integra procesos de **extracción, transformación, análisis exploratorio, minería de datos, predicción y visualización**, permitiendo analizar comportamiento de ventas, patrones de compra, desempeño de productos y métricas clave del negocio.

El objetivo principal es construir una visión **360° del negocio retail**, centralizando análisis comerciales, operativos y predictivos en una sola arquitectura analítica.

---

# 🎯 Objetivos del Proyecto

- Centralizar información de ventas retail.
- Automatizar procesos ETL.
- Analizar comportamiento histórico de ventas.
- Identificar productos de alto rendimiento.
- Detectar patrones de compra frecuentes.
- Generar modelos predictivos de demanda.
- Crear dashboards ejecutivos.
- Mejorar decisiones comerciales basadas en datos.

---

# 🏗️ Arquitectura del Proyecto

```text
Raw Data
   │
   ▼
ETL Pipeline
   │
   ▼
Data Cleaning & Validation
   │
   ▼
Exploratory Data Analysis
   │
   ▼
Feature Engineering
   │
   ▼
Business KPIs
   │
   ▼
Machine Learning / Forecasting
   │
   ▼
Market Basket Analysis
   │
   ▼
Dashboard / Visualization
   │
   ▼
Business Insights
```

---

# ⚙️ Tecnologías Utilizadas

| Tecnología | Uso |
|-----------|------|
| Python | Procesamiento y análisis de datos |
| Pandas | Manipulación de datasets |
| NumPy | Operaciones numéricas |
| Matplotlib | Visualización |
| SQL Server | Base de datos |
| PyODBC | Conexión SQL |
| Scikit-Learn | Modelos predictivos |
| MLXtend | Reglas de asociación |
| Power BI | Dashboard ejecutivo |
| GitHub | Versionamiento |

---

# 📂 Estructura del Proyecto

```bash
Data-Retail-360/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── external/
│
├── notebooks/
│   ├── 01_EDA.ipynb
│   ├── 02_ETL.ipynb
│   ├── 03_Market_Basket.ipynb
│   └── 04_Forecasting.ipynb
│
├── src/
│   ├── extraction.py
│   ├── transformation.py
│   ├── cleaning.py
│   ├── kpi_analysis.py
│   ├── forecasting.py
│   └── basket_analysis.py
│
├── dashboard/
│   └── retail_dashboard.pbix
│
├── images/
│
├── requirements.txt
└── README.md
```

---

# 🔄 Flujo ETL

### 1. Extracción
Carga de datos desde SQL Server y fuentes transaccionales.

### 2. Transformación
- Limpieza de nulos
- Conversión de formatos
- Normalización
- Homologación de variables
- Validación de integridad

### 3. Carga
Almacenamiento de datos procesados para análisis y visualización.

---

# 📊 KPIs Analizados

- Total Revenue
- Sales Growth %
- Average Ticket
- Top Selling Products
- Units Sold
- Profit Margin
- Customer Frequency
- Inventory Turnover
- Order Volume
- Monthly Sales Trend
- Category Contribution
- Purchase Frequency
- Conversion Metrics

---

# 🔎 Exploratory Data Analysis (EDA)

Se realizaron análisis para identificar:

- Tendencias de ventas.
- Distribución de clientes.
- Categorías más rentables.
- Productos con baja rotación.
- Comportamientos estacionales.
- Outliers.
- Segmentos de mayor impacto.

---

# 🤖 Machine Learning & Forecasting

Implementación de modelos predictivos para estimación de demanda y comportamiento comercial.

### Técnicas utilizadas:
- Feature Engineering
- Time Series Analysis
- Forecasting Models
- Trend Detection
- Seasonality Analysis
- Predictive Evaluation

---

# 🛍️ Market Basket Analysis

Aplicación de minería de reglas de asociación para descubrir productos comprados frecuentemente en conjunto.

### Algoritmos usados:
- Apriori
- Association Rules

### Métricas evaluadas:
- Support
- Confidence
- Lift

Esto permite:
- Cross-selling
- Product Bundling
- Layout Optimization
- Recomendaciones comerciales

---

# 📈 Dashboard Ejecutivo

Dashboard diseñado para toma de decisiones con enfoque gerencial.

Incluye:

- KPIs dinámicos
- Segmentación por categoría
- Tendencias mensuales
- Forecast de ventas
- Productos líderes
- Comparativos históricos
- Insights accionables

---

# 📌 Hallazgos de Negocio

Algunos insights generados:

- Identificación de productos altamente rentables.
- Patrones de compra recurrentes.
- Estacionalidad en ventas.
- Oportunidades de cross-selling.
- Optimización de decisiones comerciales.
- Reducción de análisis manual.
- Mayor visibilidad del comportamiento del cliente.

---

# 🚀 Instalación

Clonar repositorio:

```bash
git clone https://github.com/tuusuario/Data-Retail-360.git
cd Data-Retail-360
```

Crear entorno virtual:

```bash
python -m venv venv
```

Activar entorno:

### Windows
```bash
venv\Scripts\activate
```

### Mac / Linux
```bash
source venv/bin/activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

---

# ▶️ Ejecución

Ejecutar notebooks:

```bash
jupyter notebook
```

O scripts principales:

```bash
python src/extraction.py
python src/transformation.py
python src/forecasting.py
```

---

# 📷 Capturas del Proyecto

Agregar screenshots aquí:

```bash
images/dashboard.png
images/forecast.png
images/market_basket.png
```

Ejemplo:

```md
![Dashboard](images/dashboard.png)
```

---

# 📌 Roadmap

- [x] ETL Pipeline
- [x] SQL Integration
- [x] Data Cleaning
- [x] Exploratory Analysis
- [x] KPI Engine
- [x] Forecasting
- [x] Market Basket Analysis
- [x] Dashboard BI
- [ ] Deployment Web App
- [ ] Authentication Layer
- [ ] Cloud Integration
- [ ] Real-Time Analytics

---

# 💼 Aplicaciones de Negocio

Este proyecto puede ser usado en:

- Retail Analytics
- Inventory Optimization
- Customer Segmentation
- Demand Forecasting
- Business Intelligence
- Sales Optimization
- Data Science Portfolio
- Executive Reporting

---

# 👨‍💻 Autor

**Ian Lozano Ruiz**  
Electronic Engineer | Data Scientist | Analytics | BI | Machine Learning

---

# 📜 Licencia

Este proyecto se encuentra bajo licencia MIT.

---

# ⭐ Conclusión

**Data Retail 360** consolida una arquitectura analítica orientada a transformar datos retail en inteligencia de negocio, combinando automatización, análisis avanzado, predicción y visualización ejecutiva para generar una visión completa del rendimiento comercial.

---

<p align="center">
  Made with ❤️ using Python, SQL, Power BI & Data Science
</p>
