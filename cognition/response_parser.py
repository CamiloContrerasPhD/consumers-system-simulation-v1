"""
Parser de Respuestas
Traduce las respuestas del LLM en acciones ejecutables
"""

from typing import Dict, Optional, Tuple
from models.agent import Agent
from models.location import Location
from models.world_config import WorldConfig
from engine.interaction_engine import InteractionEngine
from engine.transaction_system import TransactionSystem


class ResponseParser:
    """
    Traduce las decisiones del LLM en acciones ejecutables.
    Maneja errores y alucinaciones del LLM.
    """
    
    def __init__(self, world_config: WorldConfig, locations: Dict[str, Location],
                 interaction_engine: InteractionEngine,
                 transaction_system: TransactionSystem):
        self.world_config = world_config
        self.locations = locations
        self.interaction_engine = interaction_engine
        self.transaction_system = transaction_system
    
    def parse_and_execute_decision(self, agent: Agent, decision: Dict) -> Tuple[bool, str]:
        """
        Parsea una decisión del LLM y la ejecuta.
        Retorna (éxito, mensaje)
        """
        action = decision.get("action", "rest").lower()
        
        # Registrar la decisión
        agent.last_action = action
        day, hour, minute = self.world_config.get_current_time()
        agent.last_action_time = (day, hour, minute)
        
        if action == "buy":
            return self._execute_purchase(agent, decision)
        
        elif action == "move":
            return self._execute_movement(agent, decision)
        
        elif action == "rest":
            return self._execute_rest(agent, decision)
        
        elif action == "eat":
            return self._execute_eat(agent, decision)
        
        elif action == "work":
            return self._execute_work(agent, decision)
        
        elif action == "chat":
            return self._execute_chat(agent, decision)
        
        else:
            return False, f"Acción desconocida: {action}"
    
    def _execute_purchase(self, agent: Agent, decision: Dict) -> Tuple[bool, str]:
        """Ejecuta una acción de compra"""
        target_location_name = decision.get("target_location")
        target_product = decision.get("target_product")
        
        if not target_location_name or not target_product:
            return False, f"Decisión de compra incompleta: falta ubicación o producto"
        
        # Validar que la ubicación existe
        if target_location_name not in self.locations:
            # Intentar encontrar por nombre similar (manejo de alucinaciones)
            similar_location = self._find_similar_location(target_location_name)
            if similar_location:
                target_location_name = similar_location
            else:
                return False, f"Ubicación '{target_location_name}' no existe"
        
        location = self.locations[target_location_name]
        
        # Validar que el producto existe en la ubicación
        if target_product not in location.inventory:
            # Intentar encontrar producto similar
            similar_product = self._find_similar_product(location, target_product)
            if similar_product:
                target_product = similar_product
            else:
                return False, f"Producto '{target_product}' no disponible en {location.name}"
        
        # Ejecutar la compra
        success, message, price = self.transaction_system.execute_purchase(
            agent, location, target_product, quantity=1
        )
        
        if success:
            # Registrar evento
            day, hour, minute = self.world_config.get_current_time()
            agent.memory.add_event(
                timestamp=(day, hour, minute),
                event_type="Purchase",
                description=message,
                location=location.name,
                metadata={"product": target_product, "price": price}
            )
        
        return success, message
    
    def _execute_movement(self, agent: Agent, decision: Dict) -> Tuple[bool, str]:
        """Ejecuta una acción de movimiento"""
        target_location_name = decision.get("target_location")
        
        if not target_location_name:
            return False, "Decisión de movimiento incompleta: falta ubicación destino"
        
        # Validar que la ubicación existe
        if target_location_name not in self.locations:
            similar_location = self._find_similar_location(target_location_name)
            if similar_location:
                target_location_name = similar_location
            else:
                return False, f"Ubicación '{target_location_name}' no existe"
        
        location = self.locations[target_location_name]
        target_coordinates = location.coordinates
        
        # Validar y ejecutar movimiento
        is_valid, energy_cost = self.interaction_engine.validate_movement(
            agent, target_coordinates, self.locations
        )
        
        if not is_valid:
            return False, f"No se puede mover a {location.name}: energía insuficiente o ubicación inválida"
        
        success = self.interaction_engine.move_agent(agent, target_coordinates, self.locations)
        
        if success:
            day, hour, minute = self.world_config.get_current_time()
            agent.memory.add_event(
                timestamp=(day, hour, minute),
                event_type="Move",
                description=f"{agent.name} se movió a {location.name}",
                location=location.name
            )
            return True, f"{agent.name} se movió a {location.name}"
        else:
            return False, f"Error al moverse a {location.name}"
    
    def _execute_rest(self, agent: Agent, decision: Dict) -> Tuple[bool, str]:
        """Ejecuta una acción de descanso"""
        agent.consume_energy("rest")  # Recupera energía
        
        day, hour, minute = self.world_config.get_current_time()
        agent.memory.add_event(
            timestamp=(day, hour, minute),
            event_type="Rest",
            description=f"{agent.name} está descansando",
            location=agent.current_location
        )
        
        return True, f"{agent.name} está descansando (energía: {agent.energy:.1f}/100)"
    
    def _execute_eat(self, agent: Agent, decision: Dict) -> Tuple[bool, str]:
        """Ejecuta una acción de comer"""
        if not agent.inventory:
            return False, f"{agent.name} no tiene comida en el inventario"
        
        # Consumir el primer item disponible
        item_name = list(agent.inventory.keys())[0]
        success = agent.consume_item(item_name, quantity=1)
        
        if success:
            agent.consume_energy("eat")  # Recupera energía al comer
            
            day, hour, minute = self.world_config.get_current_time()
            agent.memory.add_event(
                timestamp=(day, hour, minute),
                event_type="Eat",
                description=f"{agent.name} comió {item_name}",
                location=agent.current_location
            )
            return True, f"{agent.name} comió {item_name} (energía: {agent.energy:.1f}/100)"
        else:
            return False, f"Error al consumir {item_name}"
    
    def _execute_work(self, agent: Agent, decision: Dict) -> Tuple[bool, str]:
        """Ejecuta una acción de trabajo"""
        if agent.current_location != agent.work_location or not agent.work_location:
            return False, f"{agent.name} no está en su lugar de trabajo"
        
        agent.consume_energy("work")
        # Generar ingresos por trabajar (simplificado)
        agent.money += 50.0
        
        day, hour, minute = self.world_config.get_current_time()
        agent.memory.add_event(
            timestamp=(day, hour, minute),
            event_type="Work",
            description=f"{agent.name} trabajó y ganó $50",
            location=agent.work_location
        )
        
        return True, f"{agent.name} trabajó (energía: {agent.energy:.1f}/100, dinero: ${agent.money:.2f})"
    
    def _execute_chat(self, agent: Agent, decision: Dict) -> Tuple[bool, str]:
        """Ejecuta una acción de charla (requiere otro agente)"""
        # Esta acción se manejará externamente cuando se detecten agentes cercanos
        return True, f"{agent.name} quiere chatear (requiere otro agente presente)"
    
    def _find_similar_location(self, location_name: str) -> Optional[str]:
        """Encuentra una ubicación similar (manejo de alucinaciones)"""
        location_name_lower = location_name.lower()
        
        for loc_name in self.locations.keys():
            if location_name_lower in loc_name.lower() or loc_name.lower() in location_name_lower:
                return loc_name
        
        return None
    
    def _find_similar_product(self, location: Location, product_name: str) -> Optional[str]:
        """Encuentra un producto similar en la ubicación"""
        product_name_lower = product_name.lower()
        
        for prod_name in location.inventory.keys():
            if product_name_lower in prod_name.lower() or prod_name.lower() in product_name_lower:
                return prod_name
        
        return None





