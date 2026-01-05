import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from logic import CalculadoraOperaciones

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Gestor de Operaciones",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- ESTILOS CSS PERSONALIZADOS (PARA LIMPIEZA VISUAL) ---
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .block-container {padding-top: 2rem;}
            div[data-testid="stMetric"] {
                background-color: #f0f2f6;
                padding: 15px;
                border-radius: 10px;
                text-align: center;
            }
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# --- MENÚ LATERAL ---
with st.sidebar:
    st.header("Navegación")
    opcion = st.radio(
        "Seleccione Módulo:",
        ["🏠 Inicio", "📦 Punto Óptimo (EOQ)", "⚖️ Balance de Línea"]
    )
    st.markdown("---")
    st.info("Herramienta de Optimización v1.0")

# --- LÓGICA DE PÁGINAS ---

if opcion == "🏠 Inicio":
    st.title("Sistema de Optimización Industrial")
    st.markdown("""
    Bienvenido. Seleccione una herramienta en el menú lateral para comenzar.
    
    * **Punto Óptimo (EOQ):** Minimización de costos de inventario.
    * **Balance de Línea:** Cálculo de eficiencia y estaciones de trabajo.
    """)

elif opcion == "📦 Punto Óptimo (EOQ)":
    st.title("Optimizador de Punto de Pedido")
    st.markdown("Cálculo del lote económico para minimizar costos totales.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        d = st.number_input("Demanda Anual (D)", min_value=1.0, value=1000.0, step=10.0)
    with col2:
        s = st.number_input("Costo de Ordenar (S)", min_value=1.0, value=50.0, step=5.0)
    with col3:
        h = st.number_input("Costo de Mantener (H)", min_value=0.1, value=2.5, step=0.1)
        
    if st.button("Calcular Óptimo", type="primary"):
        q, c_total, n_ordenes = CalculadoraOperaciones.calcular_eoq(d, s, h)
        
        st.markdown("---")
        st.subheader("Resultados")
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Cantidad Óptima (Q*)", f"{q} u.")
        m2.metric("Costo Total Anual", f"${c_total}")
        m3.metric("Órdenes por Año", f"{n_ordenes}")
        
        # Gráfica Simple
        st.subheader("Visualización de Costos")
        try:
            rango_q = np.linspace(max(1, q - q*0.5), q + q*0.5, 100)
            costos = [(x/2)*h + (d/x)*s for x in rango_q]
            
            fig, ax = plt.subplots(figsize=(6, 3))
            ax.plot(rango_q, costos, color='#0068c9', linewidth=2)
            ax.axvline(x=q, color='red', linestyle='--', label=f'Q* = {q}')
            ax.set_xlabel("Cantidad de Pedido (Q)")
            ax.set_ylabel("Costo Total")
            ax.grid(True, alpha=0.3)
            ax.legend()
            st.pyplot(fig)
        except Exception as e:
            st.error("Error al generar gráfica.")

elif opcion == "⚖️ Balance de Línea":
    st.title("Balance de Línea de Producción")
    st.markdown("Determine la eficiencia y el número de estaciones necesarias.")
    
    c1, c2 = st.columns(2)
    with c1:
        tiempo_disp = st.number_input("Tiempo Disponible (min)", value=480.0)
    with c2:
        demanda = st.number_input("Demanda (unidades)", value=120.0)
        
    st.markdown("### Tiempos de las Tareas")
    tareas_input = st.text_area("Ingrese los tiempos separados por coma (ej: 2.5, 3.0, 1.5)", "5, 3, 4, 2, 6")
    
    if st.button("Calcular Balance", type="primary"):
        try:
            # Convertir texto a lista de floats
            lista_tiempos = [float(x.strip()) for x in tareas_input.split(',')]
            
            res = CalculadoraOperaciones.balance_linea(lista_tiempos, tiempo_disp, demanda)
            
            if res:
                st.markdown("---")
                st.subheader("Análisis de Línea")
                
                k1, k2, k3, k4 = st.columns(4)
                k1.metric("Takt Time", f"{res['takt_time']} min/u")
                k2.metric("Estaciones Min.", f"{res['estaciones_min']}")
                k3.metric("Eficiencia", f"{res['eficiencia']}%")
                k4.metric("Tiempo Ocioso", f"{res['tiempo_ocio']}%")
                
                st.success(f"Se requieren teóricamente **{res['estaciones_min']} estaciones** para cumplir con la demanda.")
            else:
                st.error("Verifique que los valores sean mayores a 0.")
        except ValueError:
            st.error("Error en formato de tareas. Asegúrese de usar solo números separados por comas.")