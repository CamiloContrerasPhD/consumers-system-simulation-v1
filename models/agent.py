"""
Módulo de Agentes
Define las entidades consumidoras que interactúan en el mundo
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from models.memory_stream import MemoryStream


@dataclass
class Agent:
    """Representa un agente consumidor en la simulación"""
    
    # Perfil estático
    agent_id: str
    name: str
    age: int
    profession: str
    personality_traits: List[str] = field(default_factory=list)
    # Ejemplos: ["extrovert", "health_conscious", "impulsive", "thrifty"]
    
    # Estado dinámico - Sistema de Necesidades
    energy: float = 100.0  # 0-100, decae por hora/actividad
    money: float = 500.0  # Saldo actual
    inventory: Dict[str, int] = field(default_factory=dict)  # Comestibles actuales
    grocery_level: float = 50.0  # Nivel de comestibles en casa (0-100)
    
    # Estado Social
    relationships: Dict[str, float] = field(default_factory=dict)
    # Formato: {agent_id: affinity_score} donde affinity_score es -1.0 a 1.0
    
    # Posición y Estado
    current_location: str = "home"  # ID de ubicación actual
    coordinates: Tuple[int, int] = (0, 0)
    home_location: str = "home"
    work_location: str = ""
    
    # Memoria
    memory: MemoryStream = field(default_factory=MemoryStream)
    
    # Plan del día
    daily_plan: List[Dict] = field(default_factory=list)
    # Formato: [{"time": "08:00", "action": "work", "location": "office"}]
    
    # Estado temporal
    is_planning_day: bool = False
    last_action: Optional[str] = None
    last_action_time: Optional[Tuple[int, int, int]] = None
    
    def decay_energy(self, amount: float = 2.0):
        """Reduce la energía del agente (se llama cada hora)"""
        self.energy = max(0.0, self.energy - amount)
    
    def consume_energy(self, activity_type: str):
        """Consume energía según el tipo de actividad"""
        costs = {
            "walk": 5.0,
            "drive": 1.0,
            "work": 10.0,
            "exercise": 15.0,
            "rest": -10.0,  # Recupera energía
            "eat": -5.0  # Recupera energía
        }
        cost = costs.get(activity_type, 2.0)
        self.energy = max(0.0, min(100.0, self.energy - cost))
    
    def can_move(self, distance: float = 1.0) -> bool:
        """Verifica si el agente tiene energía suficiente para moverse"""
        return self.energy >= 5.0
    
    def spend_money(self, amount: float) -> bool:
        """Intenta gastar dinero, retorna True si fue exitoso"""
        if self.money >= amount:
            self.money -= amount
            return True
        return False
    
    def add_item(self, item_name: str, quantity: int = 1):
        """Añade items al inventario"""
        if item_name in self.inventory:
            self.inventory[item_name] += quantity
        else:
            self.inventory[item_name] = quantity
    
    def consume_item(self, item_name: str, quantity: int = 1) -> bool:
        """Consume items del inventario, retorna True si fue exitoso"""
        if item_name in self.inventory and self.inventory[item_name] >= quantity:
            self.inventory[item_name] -= quantity
            if self.inventory[item_name] == 0:
                del self.inventory[item_name]
            self.grocery_level = min(100.0, self.grocery_level + 10.0 * quantity)
            return True
        return False
    
    def update_relationship(self, other_agent_id: str, change: float):
        """Actualiza la relación con otro agente"""
        if other_agent_id in self.relationships:
            self.relationships[other_agent_id] = max(-1.0, min(1.0, 
                self.relationships[other_agent_id] + change))
        else:
            self.relationships[other_agent_id] = max(-1.0, min(1.0, change))
    
    def get_affinity(self, other_agent_id: str) -> float:
        """Retorna el nivel de afinidad con otro agente (-1.0 a 1.0)"""
        return self.relationships.get(other_agent_id, 0.0)
    
    def is_collapsed(self) -> bool:
        """Verifica si el agente colapsó (energía = 0)"""
        return self.energy <= 0
    
    def reset_agent(self):
        """Resetea el agente después de colapsar"""
        self.energy = 50.0
        self.coordinates = (0, 0)  # Regresa a casa
        self.current_location = self.home_location
    
    def get_state_summary(self) -> Dict:
        """Retorna un resumen del estado actual del agente"""
        return {
            "energy": self.energy,
            "money": self.money,
            "grocery_level": self.grocery_level,
            "location": self.current_location,
            "coordinates": self.coordinates,
            "inventory_count": sum(self.inventory.values())
        }





