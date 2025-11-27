"""
Módulo de Configuración Global del Mundo
Define el estado del mundo y sus parámetros principales
"""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple
from datetime import datetime, time


@dataclass
class WorldConfig:
    """Configuración global del mundo de simulación"""
    
    # Mapa y Grid
    width: int = 10  # Ancho del mapa
    height: int = 10  # Alto del mapa
    
    # Reloj del Sistema
    current_day: int = 0
    current_hour: int = 7  # Inicia a las 7:00 AM
    current_minute: int = 0
    tick_duration_minutes: int = 60  # Cada tick = 1 hora
    
    # Variables de Marketing
    marketing_campaigns: List[Dict] = field(default_factory=list)
    # Formato: {"location_name": "Chicken Shop", "discount_percent": 20, "day_of_week": 2, "start_hour": 12, "end_hour": 14}
    
    # Grid de ubicaciones (matriz de coordenadas)
    grid: List[List[None]] = field(default_factory=lambda: [[None for _ in range(10)] for _ in range(10)])
    
    def get_current_time(self) -> Tuple[int, int, int]:
        """Retorna (día, hora, minuto) actual"""
        return (self.current_day, self.current_hour, self.current_minute)
    
    def get_day_of_week(self) -> int:
        """Retorna el día de la semana (0=Lunes, 6=Domingo)"""
        return self.current_day % 7
    
    def advance_time(self):
        """Avanza el tiempo según tick_duration_minutes"""
        self.current_minute += self.tick_duration_minutes
        
        if self.current_minute >= 60:
            self.current_minute = 0
            self.current_hour += 1
            
        if self.current_hour >= 24:
            self.current_hour = 0
            self.current_day += 1
    
    def is_marketing_active(self, location_name: str) -> bool:
        """Verifica si hay una campaña de marketing activa para una ubicación"""
        day_of_week = self.get_day_of_week()
        current_time = self.current_hour
        
        for campaign in self.marketing_campaigns:
            if (campaign.get("location_name") == location_name and
                campaign.get("day_of_week") == day_of_week and
                campaign.get("start_hour", 0) <= current_time < campaign.get("end_hour", 24)):
                return True
        return False
    
    def get_discount(self, location_name: str) -> float:
        """Retorna el porcentaje de descuento activo para una ubicación (0.0 a 1.0)"""
        if self.is_marketing_active(location_name):
            for campaign in self.marketing_campaigns:
                if campaign.get("location_name") == location_name:
                    return campaign.get("discount_percent", 0) / 100.0
        return 0.0



