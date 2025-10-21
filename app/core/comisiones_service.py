from datetime import datetime, timedelta
from app import models

class ComisionesService:
    def __init__(self):
        pass

    def calcular_comisiones_vendedor(self, vendedor_id, fecha_inicio, fecha_fin):
        ventas_periodo = models.get_ventas_by_vendedor_and_date_range(
            vendedor_id, fecha_inicio, fecha_fin
        )

        total_ventas = sum(venta['monto'] for venta in ventas_periodo)
        total_transacciones = len(ventas_periodo)

        current_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        reglas_activas = models.get_active_reglas_comision(current_date)

        porcentaje_comision_aplicado = 0.0
        comision_a_pagar = 0.0
        regla_aplicada_nombre = "Ninguna"

        if total_ventas > 0:
            reglas_activas.sort(key=lambda r: r.get('umbral_ventas_min', 0), reverse=True)

            for regla in reglas_activas:
                umbral_min = regla.get('umbral_ventas_min', 0)
                umbral_max = regla.get('umbral_ventas_max', float('inf'))
                porcentaje = regla.get('porcentaje', 0.0)
                
                if umbral_min <= total_ventas <= umbral_max:
                    porcentaje_comision_aplicado = porcentaje
                    regla_aplicada_nombre = regla.get('nombre_regla', f"Regla {regla['_id']}")
                    break 

            comision_a_pagar = total_ventas * (porcentaje_comision_aplicado / 100)

        return {
            'total_ventas': total_ventas,
            'total_transacciones': total_transacciones,
            'porcentaje_comision_aplicado': porcentaje_comision_aplicado,
            'comision_a_pagar': comision_a_pagar,
            'regla_aplicada': regla_aplicada_nombre
        }

comisiones_service = ComisionesService()