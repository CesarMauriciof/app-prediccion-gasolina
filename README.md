# ⛽ Aplicación Web: Predicción del Precio de la Gasolina

Aplicación web interactiva desarrollada con **Streamlit** para predecir el precio mensual de la gasolina (USD/galón y COP/galón) a partir de variables macroeconómicas y energéticas. La aplicación está desplegada en Streamlit Community Cloud — el enlace público se encuentra en la descripción del repositorio.

Resumen:

- Proyecto end-to-end: recolección y limpieza de datos, análisis exploratorio (EDA), ingeniería de variables, entrenamiento y evaluación de modelos, y despliegue web.
- Modelo entrenado por nosotros: el pipeline incluye preprocesamiento (escalado, codificación), selección de características y validación cruzada.
- Visualizaciones y métricas claras para explicar el desempeño y la robustez del modelo.
- Interfaz interactiva en Streamlit que permite probar escenarios (cambio en precio del petróleo, tipo de cambio, impuestos, eventos geopolíticos, etc.).

Demo en vivo

- Despliegue: Streamlit Community Cloud
- Enlace público: (ver descripción del repositorio)

Qué hice en este proyecto

- Análisis exploratorio de los datos (visualizaciones, detección de outliers, correlaciones).
- Ingeniería de features (lags, normalizaciones, variables dummy para eventos geopolíticos).
- Entrenamiento de modelos con scikit-learn, comparación de alternativas y ajuste de hiperparámetros.
- Validación cruzada y separación robusta entre train/test para evitar fugas de información.
- Serialización del modelo final (modelo + scaler + metadatos) en `modelo_gasolina.pkl`.
- Diseño de la app Streamlit para exposición clara de inputs, resultados y gráficos.

Características principales

- Interfaz amigable con controles para cada variable de entrada.
- Gráficas de sensibilidad y predicciones con intervalos.
- Métricas del modelo presentadas (R², RMSE, MAE) y explicación breve de su interpretación.

Tecnologías

- Python, Streamlit, scikit-learn, pandas, numpy, matplotlib / seaborn
- Empaquetado del modelo: pickle

Cómo ejecutar la aplicación localmente

Opción 1: Un solo clic en Windows
- Haz doble clic sobre el archivo `iniciar_app.bat`.

Opción 2: Desde la terminal / PowerShell
1. Activar el entorno virtual:
```powershell
.\.venv\Scripts\activate
```
2. Iniciar la aplicación:
```powershell
streamlit run app.py
```
3. O usar el script PowerShell:
```powershell
.\iniciar_app.ps1
```

Despliegue en la nube (opcional)

Recomendado: Streamlit Community Cloud
1. Sube este repositorio a GitHub.
2. Entra a https://share.streamlit.io y crea una nueva app apuntando a `app.py` en la rama `main`.

Estructura del proyecto

```text
app-web-predeccion-gasolina/
│
├── app.py                     # Código principal de la aplicación Streamlit
├── modelo_gasolina.pkl        # Modelo entrenado, scaler, métricas y rangos
├── requirements.txt           # Dependencias de Python necesarias
├── iniciar_app.bat            # Lanzador para Windows (1 clic)
├── iniciar_app.ps1            # Lanzador para PowerShell
├── README.md                  # Documentación del proyecto
├── .streamlit/
│   └── config.toml            # Configuración de Streamlit (puerto, tema, etc.)
└── .venv/                     # Entorno virtual de Python (no incluir en el repo)
```

Variables clave del modelo

| Variable | Descripción | Rango habitual |
| :--- | :--- | :--- |
| **Precio del petróleo** | Precio del crudo en USD/barril | 29.73 – 93.43 USD |
| **Tipo de cambio USD/COP** | Tasa de cambio de COP por dólar | 2,740 – 4,579 COP |
| **Demanda** | Consumo estimado en miles de barriles/día | 9,176 – 10,358 kbd |
| **Inflación** | Tasa de inflación mensual/anual (%) | 1.76% – 6.01% |
| **Crecimiento del PIB** | Crecimiento económico (%) | -1.75% – 6.88% |
| **Impuestos a combustibles** | Carga tributaria sobre el combustible (%) | 18.0% – 30.0% |
| **Eventos Geopolíticos** | Conflictos o tensiones que afecten el suministro | Sí / No (1 / 0) |

Métricas del modelo

- R² en prueba: ~0.921
- R² (Validación Cruzada): ~0.898
- RMSE: ~0.236 USD/galón
- MAE: ~0.195 USD/galón

Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.

Contacto

- Autor: CesarMauriciof
- GitHub: https://github.com/CesarMauriciof/app-prediccion-gasolina

---

_P.D.: Si quieres que incluya la URL pública exacta del despliegue (en Streamlit u otro servicio), pásamela y la actualizo en el README._
