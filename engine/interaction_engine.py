"""
Motor de Interacciones
Gestiona la física del mundo y los encuentros entre agentes
"""

from typing import List, Dict, Set, Tuple, Optional
from models.agent import Agent
from models.location import Location
from models.world_config import WorldConfig
import math


class InteractionEngine:
    """Gestiona interacciones espaciales y físicas entre agentes"""
    
    def __init__(self, world_config: WorldConfig):
        self.world_config = world_config
    
    def detect_proximity(self, agent: Agent, all_agents: List[Agent], 
                        threshold: float = 1.0) -> List[Agent]:
        """
        Detecta agentes cercanos basándose en coordenadas.
        Retorna lista de agentes dentro del umbral de distancia.
        """
        nearby_agents = []
        
        for other_agent in all_agents:
            if other_agent.agent_id == agent.agent_id:
                continue
            
            distance = self._calculate_distance(agent.coordinates, other_agent.coordinates)
            if distance <= threshold:
                nearby_agents.append(other_agent)
        
        return nearby_agents
    
    def detect_same_location(self, agent: Agent, all_agents: List[Agent]) -> List[Agent]:
        """Detecta agentes en la misma ubicación exacta"""
        same_location_agents = []
        
        for other_agent in all_agents:
            if (other_agent.agent_id != agent.agent_id and
                other_agent.current_location == agent.current_location):
                same_location_agents.append(other_agent)
        
        return same_location_agents
    
    def validate_movement(self, agent: Agent, target_coordinates: Tuple[int, int],
                         locations: Dict[str, Location]) -> Tuple[bool, float]:
        """
        Valida si un agente puede moverse a las coordenadas objetivo.
        Retorna (es_válido, costo_energía)
        """
        # Verificar límites del mapa
        x, y = target_coordinates
        if (x < 0 or x >= self.world_config.width or
            y < 0 or y >= self.world_config.height):
            return False, 0.0
        
        # Calcular distancia
        distance = self._calculate_distance(agent.coordinates, target_coordinates)
        
        # Calcular costo de energía (costo base por unidad de distancia)
        energy_cost = distance * 5.0  # 5 puntos de energía por unidad
        
        # Verificar si el agente tiene suficiente energía
        if agent.energy < energy_cost:
            return False, energy_cost
        
        return True, energy_cost
    
    def move_agent(self, agent: Agent, target_coordinates: Tuple[int, int],
                  locations: Dict[str, Location]) -> bool:
        """
        Mueve un agente a las coordenadas objetivo.
        Retorna True si el movimiento fue exitoso.
        """
        is_valid, energy_cost = self.validate_movement(agent, target_coordinates, locations)
        
        if not is_valid:
            return False
        
        # Remover agente de ubicación actual
        if agent.current_location in locations:
            locations[agent.current_location].leave(agent.agent_id)
        
        # Actualizar coordenadas
        agent.coordinates = target_coordinates
        agent.consume_energy("walk")
        
        # Verificar si llegó a alguna ubicación conocida
        new_location = self._find_location_at_coordinates(target_coordinates, locations)
        if new_location:
            if new_location.enter(agent.agent_id):
                agent.current_location = new_location.name
        
        return True
    
    def _calculate_distance(self, coord1: Tuple[int, int], coord2: Tuple[int, int]) -> float:
        """Calcula la distancia euclidiana entre dos coordenadas"""
        x1, y1 = coord1
        x2, y2 = coord2
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    
    def _find_location_at_coordinates(self, coordinates: Tuple[int, int],
                                     locations: Dict[str, Location]) -> Optional[Location]:
        """Encuentra una ubicación en las coordenadas dadas"""
        for location in locations.values():
            if location.coordinates == coordinates:
                return location
        return None
    
    def get_agents_at_location(self, location_name: str, 
                              all_agents: List[Agent]) -> List[Agent]:
        """Retorna todos los agentes presentes en una ubicación"""
        return [agent for agent in all_agents 
                if agent.current_location == location_name]





