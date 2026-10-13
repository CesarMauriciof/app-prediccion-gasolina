# ⛽ Aplicación Web: Predicción del Precio de la Gasolina

Esta aplicación web construida con **Streamlit** y **scikit-learn** permite predecir el precio mensual de la gasolina (en USD/galón y COP/galón) a partir de variables macroeconómicas, energéticas y geopolíticas, utilizando un modelo de regresión lineal calibrado con intervalos de confianza y predicción al 95%.
<img width="1352" height="649" alt="WhatsApp Image 2026-10-13 at 1 01 44 PM" src="https://github.com/user-attachments/assets/38616585-b82d-4bfb-8dca-6229b6ab2cf9" />

---

## 🚀 Cómo Ejecutar la Aplicación en Local

### Opción 1: Un solo clic en Windows (Más fácil)
Haz doble clic sobre el archivo:
- `iniciar_app.bat`

El navegador se abrirá automáticamente en `http://localhost:8501`.

---

### Opción 2: Desde la terminal / PowerShell

1. **Activar el entorno virtual:**
   ```powershell
   .\.venv\Scripts\activate
   ```
2. **Iniciar la aplicación:**
   ```powershell
   streamlit run app.py
   ```
3. O directamente con el script PowerShell:
   ```powershell
   .\iniciar_app.ps1
   ```

---

## 🌐 Cómo Publicarla en la Web (Gratis en la Nube)

Puedes desplegar esta aplicación web de manera gratuita para que cualquier persona acceda mediante un enlace público:

### Método Recomendado: Streamlit Community Cloud
1. Sube este proyecto a un repositorio de **GitHub** (ejemplo: `usuario/app-prediccion-gasolina`).
2. Entra a [share.streamlit.io](https://share.streamlit.io) e inicia sesión con GitHub.
3. Haz clic en **"New app"**.
4. Selecciona tu repositorio, rama `main` y el archivo principal: `app.py`.
5. Haz clic en **"Deploy"** ¡y listo! Streamlit instalará automáticamente las dependencias de `requirements.txt` y generará la URL pública.

---

## 📁 Estructura del Proyecto

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
└── .venv/                     # Entorno virtual de Python configurado
```

---

## 📊 Variables del Modelo

| Variable | Descripción | Rango habitual |
| :--- | :--- | :--- |
| **Precio del petróleo** | Precio del crudo en USD/barril | 29.73 – 93.43 USD |
| **Tipo de cambio USD/COP** | Tasa de cambio de COP por dólar | 2,740 – 4,579 COP |
| **Demanda** | Consumo estimado en miles de barriles/día | 9,176 – 10,358 kbd |
| **Inflación** | Tasa de inflación mensual/anual (%) | 1.76% – 6.01% |
| **Crecimiento del PIB** | Crecimiento económico (%) | -1.75% – 6.88% |
| **Impuestos a combustibles** | Carga tributaria sobre el combustible (%) | 18.0% – 30.0% |
| **Eventos Geopolíticos** | Conflictos o tensiones que afecten el suministro | Sí / No (1 / 0) |

---

## 🎯 Métricas del Modelo

- **R² en prueba:** ~0.921
- **R² (Validación Cruzada):** ~0.898
- **RMSE:** ~0.236 USD/galón
- **MAE:** ~0.195 USD/galón
