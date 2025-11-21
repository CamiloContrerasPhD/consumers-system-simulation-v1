"""
Gestor de Tiempo del Motor de Simulación
Orquesta el avance del tiempo y el decaimiento de energía
"""

from typing import List
from models.world_config import WorldConfig
from models.agent import Agent


class TimeManager:
    """Gestiona el tiempo de la simulación y los efectos temporales"""
    
    def __init__(self, world_config: WorldConfig):
        self.world_config = world_config
    
    def advance_tick(self, agents: List[Agent]) -> bool:
        """
        Avanza un tick en el tiempo.
        Retorna True si es un nuevo día (7 AM)
        """
        old_hour = self.world_config.current_hour
        self.world_config.advance_time()
        
        # Aplicar decaimiento de energía a todos los agentes
        self._apply_energy_decay(agents)
        
        # Verificar si es hora de planificar el día (7 AM)
        is_morning = (self.world_config.current_hour == 7 and old_hour != 7)
        
        # Resetear agentes colapsados
        self._reset_collapsed_agents(agents)
        
        return is_morning
    
    def _apply_energy_decay(self, agents: List[Agent]):
        """Aplica el decaimiento natural de energía"""
        for agent in agents:
            if not agent.is_collapsed():
                # Decaimiento base por hora
                base_decay = 2.0
                
                # Decaimiento adicional si está trabajando
                if agent.current_location == agent.work_location and agent.work_location:
                    base_decay += 5.0
                
                # Decaimiento adicional si tiene poca comida
                if agent.grocery_level < 20:
                    base_decay += 3.0
                
                agent.decay_energy(base_decay)
    
    def _reset_collapsed_agents(self, agents: List[Agent]):
        """Resetea agentes que han colapsado (energía = 0)"""
        for agent in agents:
            if agent.is_collapsed():
                agent.reset_agent()
                # Registrar evento
                day, hour, minute = self.world_config.get_current_time()
                agent.memory.add_event(
                    timestamp=(day, hour, minute),
                    event_type="Collapse",
                    description=f"{agent.name} colapsó por falta de energía y regresó a casa",
                    location=agent.home_location
                )
    
    def get_time_string(self) -> str:
        """Retorna una representación string del tiempo actual"""
        day, hour, minute = self.world_config.get_current_time()
        days = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        day_name = days[self.world_config.get_day_of_week()]
        return f"{day_name}, Día {day}, {hour:02d}:{minute:02d}"





