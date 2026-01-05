import math

class CalculadoraOperaciones:
    
    @staticmethod
    def calcular_eoq(demanda, costo_ordenar, costo_mantener):
        """
        Calcula el Lote Económico de Compra (EOQ).
        Retorna: (Q_optimo, Costo_Total, Numero_Ordenes)
        """
        if demanda <= 0 or costo_ordenar <= 0 or costo_mantener <= 0:
            return 0, 0, 0
            
        # Fórmula EOQ: Raiz((2 * D * S) / H)
        q_optimo = math.sqrt((2 * demanda * costo_ordenar) / costo_mantener)
        
        # Costo Total Esperado (simplificado)
        # Costo Mantener Total + Costo Ordenar Total
        costo_total = (q_optimo / 2) * costo_mantener + (demanda / q_optimo) * costo_ordenar
        
        # Número de órdenes al año
        num_ordenes = demanda / q_optimo
        
        return round(q_optimo, 2), round(costo_total, 2), round(num_ordenes, 2)

    @staticmethod
    def balance_linea(tiempos_tareas, tiempo_disponible, unidades_requeridas):
        """
        Calcula métricas básicas de Balance de Línea.
        tiempos_tareas: Lista de tiempos de cada actividad (ej. [2.5, 3.0, 1.5])
        tiempo_disponible: Tiempo total disponible en el periodo (minutos/horas)
        unidades_requeridas: Demanda en ese periodo
        """
        if not tiempos_tareas or unidades_requeridas <= 0 or tiempo_disponible <= 0:
            return None
            
        tiempo_total_tareas = sum(tiempos_tareas)
        
        # 1. Takt Time = Tiempo Disponible / Demanda
        takt_time = tiempo_disponible / unidades_requeridas
        
        # 2. Número Teórico de Estaciones = Suma Tiempos / Takt Time
        n_estaciones_teorico = tiempo_total_tareas / takt_time
        n_estaciones_real = math.ceil(n_estaciones_teorico) # Redondear hacia arriba siempre
        
        # 3. Eficiencia = Suma Tiempos / (N_Estaciones * Takt Time)
        # Nota: Usamos N real para eficiencia real
        if n_estaciones_real * takt_time == 0:
            eficiencia = 0
        else:
            eficiencia = (tiempo_total_tareas / (n_estaciones_real * takt_time)) * 100
            
        return {
            "takt_time": round(takt_time, 2),
            "estaciones_min": n_estaciones_real,
            "eficiencia": round(eficiencia, 2),
            "tiempo_ocio": round(100 - eficiencia, 2),
            "suma_tiempos": round(tiempo_total_tareas, 2)
        }