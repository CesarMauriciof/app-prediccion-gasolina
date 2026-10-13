from pathlib import Path
import warnings
import joblib
import numpy as np
import pandas as pd
import streamlit as st
from scipy import stats

# Silenciar advertencias de diferencias menores en versiones de scikit-learn
warnings.filterwarnings("ignore")

# Configuración de la interfaz web
st.set_page_config(
    page_title="Predicción Precio Gasolina",
    page_icon="⛽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Función para cargar el modelo de forma robusta
@st.cache_resource
def cargar_modelo():
    base_dir = Path(__file__).resolve().parent
    candidatos = [
        base_dir / "modelo_gasolina.pkl",
        base_dir / "app-web-predeccion-gasolina" / "modelo_gasolina.pkl",
        Path("modelo_gasolina.pkl"),
        Path("app-web-predeccion-gasolina") / "modelo_gasolina.pkl",
    ]
    for ruta in candidatos:
        if ruta.exists():
            return joblib.load(ruta)
    raise FileNotFoundError(
        "No se encontró 'modelo_gasolina.pkl'. Asegúrate de que el archivo esté en la carpeta del proyecto."
    )

try:
    paquete = cargar_modelo()
except Exception as e:
    st.error(f"❌ Error al cargar el modelo: {e}")
    st.stop()

modelo = paquete["modelo"]
scaler = paquete["scaler"]
features = paquete["features"]
sigma, XtX_inv, gl = paquete["sigma"], paquete["XtX_inv"], paquete["gl"]
rangos = paquete["rangos"]
t_95 = stats.t.ppf(0.975, gl)

# Diccionario de etiquetas descriptivas y paso sugerido
etiquetas = {
    "Precio_Petroleo_USD_Barril": ("Precio del petróleo (USD/barril)", 0.5),
    "Tipo_Cambio_USD_COP": ("Tipo de cambio (COP por USD)", 10.0),
    "Demanda_miles_barriles_dia": ("Demanda (miles de barriles/día)", 10.0),
    "Produccion_OPEP_millones_dia": ("Producción OPEP (millones de barriles/día)", 0.1),
    "Inflacion_Porcentaje": ("Inflación (%)", 0.1),
    "PIB_Porcentaje": ("Crecimiento del PIB (%)", 0.1),
    "Impuestos_Combustibles_Porcentaje": ("Impuestos a combustibles (%)", 0.5),
}

# Barra lateral con información y utilidades
with st.sidebar:
    st.header("⚙️ Opciones y Presets")
    st.write("Puedes cargar escenarios predefinidos para probar el modelo rápidamente:")

    numericas = [f for f in features if f != "Eventos_Geopoliticos"]

    # Inicializar valores en session_state si no existen
    for f in numericas:
        if f not in st.session_state:
            st.session_state[f] = float(round(rangos[f]["median"], 2))
    if "Eventos_Geopoliticos" in features and "Eventos_Geopoliticos" not in st.session_state:
        st.session_state["Eventos_Geopoliticos"] = "No"

    if st.button("🔄 Valores Promedio (Mediana)", use_container_width=True):
        for f in numericas:
            st.session_state[f] = float(round(rangos[f]["median"], 2))
        st.session_state["Eventos_Geopoliticos"] = "No"
        st.rerun()

    if st.button("📈 Escenario Petróleo Alto ($90+)", use_container_width=True):
        st.session_state["Precio_Petroleo_USD_Barril"] = 90.0
        st.session_state["Tipo_Cambio_USD_COP"] = 4300.0
        st.session_state["Inflacion_Porcentaje"] = 5.2
        st.session_state["Eventos_Geopoliticos"] = "Sí"
        st.rerun()

    if st.button("📉 Escenario Petróleo Bajo ($35)", use_container_width=True):
        st.session_state["Precio_Petroleo_USD_Barril"] = 35.0
        st.session_state["Tipo_Cambio_USD_COP"] = 3100.0
        st.session_state["Inflacion_Porcentaje"] = 2.1
        st.session_state["Eventos_Geopoliticos"] = "No"
        st.rerun()

    st.divider()
    mostrar_cop = st.checkbox("Mostrar estimación en Pesos Colombianos (COP)", value=True)
    st.info("💡 Este modelo de regresión lineal estima el precio minorista del combustible basándose en variables macroeconómicas del mes.")

# Encabezado principal
st.title("⛽ Predicción del Precio Mensual de la Gasolina")
st.markdown(
    "Ingresa las condiciones económicas, energéticas y geopolíticas del mes para estimar el precio esperado en **USD/galón**."
)

st.subheader("📊 Variables de Entrada")

col_left, col_right = st.columns(2)
valores = {}

for i, f in enumerate(numericas):
    nombre, paso = etiquetas.get(f, (f, 0.1))
    r = rangos[f]
    columna_actual = col_left if (i % 2 == 0) else col_right
    
    with columna_actual:
        valores[f] = st.number_input(
            label=nombre,
            key=f,
            step=paso,
            help=f"Rango de entrenamiento: mín {r['min']:.2f} — máx {r['max']:.2f} (mediana: {r['median']:.2f})",
        )

if "Eventos_Geopoliticos" in features:
    with col_left:
        evento = st.radio(
            "¿Hubo eventos geopolíticos relevantes este mes?",
            options=["No", "Sí"],
            key="Eventos_Geopoliticos",
            horizontal=True,
            help="Conflictos bélicos, sanciones o interrupciones en rutas comerciales de suministro."
        )
        valores["Eventos_Geopoliticos"] = 1 if evento == "Sí" else 0

st.divider()

# Botón de predicción
if st.button("🚀 Calcular Predicción", type="primary", use_container_width=True):
    datos = pd.DataFrame([valores])[features]
    x_s = scaler.transform(datos)
    x0 = np.concatenate([[1.0], x_s[0]])
    pred = float(modelo.predict(x_s)[0])
    h = float(x0 @ XtX_inv @ x0)
    m_conf = t_95 * sigma * np.sqrt(h)
    m_pred = t_95 * sigma * np.sqrt(1 + h)

    st.subheader("🎯 Resultado de la Predicción")

    if mostrar_cop and "Tipo_Cambio_USD_COP" in valores:
        tasa = valores["Tipo_Cambio_USD_COP"]
        pred_cop = pred * tasa
        conf_cop_min = (pred - m_conf) * tasa
        conf_cop_max = (pred + m_conf) * tasa

        res_col1, res_col2 = st.columns(2)
        with res_col1:
            st.metric(
                label="Precio Estimado (USD)",
                value=f"${pred:.2f} USD/galón",
            )
        with res_col2:
            st.metric(
                label="Precio Equivalente (COP)",
                value=f"${pred_cop:,.0f} COP/galón".replace(",", "."),
            )
    else:
        st.metric(
            label="Precio Estimado",
            value=f"${pred:.2f} USD/galón",
        )

    # Intervalos estadísticos
    c1, c2 = st.columns(2)
    with c1:
        st.info(
            f"**Intervalo de confianza 95%**\n\n"
            f"**{pred - m_conf:.2f}** – **{pred + m_conf:.2f}** USD/galón\n\n"
            f"*(Indica el valor medio esperado para este conjunto de condiciones)*"
        )
    with c2:
        st.info(
            f"**Intervalo de predicción 95%**\n\n"
            f"**{pred - m_pred:.2f}** – **{pred + m_pred:.2f}** USD/galón\n\n"
            f"*(Indica el rango probable del precio de un mes particular)*"
        )

    # Alerta de valores atípicos fuera de rango
    fuera = [
        etiquetas.get(f, (f,))[0]
        for f in numericas
        if not (rangos[f]["min"] <= valores[f] <= rangos[f]["max"])
    ]
    if fuera:
        st.warning(
            "⚠️ **Atención:** Las siguientes variables están fuera del rango histórico de entrenamiento, por lo que la predicción tiene mayor incertidumbre:\n\n- "
            + "\n- ".join(fuera)
        )

# Panel colapsable de métricas del modelo
with st.expander("📈 Métricas de Desempeño del Modelo"):
    m = paquete["metricas"]
    a, b, c = st.columns(3)
    a.metric("R² (Validación Cruzada)", f"{m['R2_cv']:.3f}")
    b.metric("RMSE", f"{m['RMSE']:.3f}")
    c.metric("MAE", f"{m['MAE']:.3f}")

    st.write(f"• **R² en prueba (30%):** `{m['R2_prueba']:.3f}` | **MSE:** `{m['MSE']:.4f}`")
    nombres_features = [
        etiquetas.get(f, (f,))[0] if f in etiquetas else "Eventos geopolíticos"
        for f in features
    ]
    st.write("**Variables consideradas:** " + ", ".join(nombres_features))
