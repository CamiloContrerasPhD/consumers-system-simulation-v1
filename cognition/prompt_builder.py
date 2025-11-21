"""
Constructor de Prompts
Ensambla dinámicamente el contexto para enviar a la API del LLM
"""

from typing import Dict, List, Optional
from models.agent import Agent
from models.location import Location
from models.world_config import WorldConfig


class PromptBuilder:
    """Construye prompts contextualizados para el LLM"""
    
    def __init__(self, world_config: WorldConfig, locations: Dict[str, Location]):
        self.world_config = world_config
        self.locations = locations
    
    def build_daily_planner_prompt(self, agent: Agent) -> str:
        """
        Construye el prompt para el planificador diario (ejecutado a las 7 AM).
        Genera el itinerario del día.
        """
        day, hour, minute = self.world_config.get_current_time()
        day_name = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"][
            self.world_config.get_day_of_week()
        ]
        
        # Construir información del agente
        agent_info = f"""
Perfil del Agente:
- Nombre: {agent.name}
- Edad: {agent.age}
- Profesión: {agent.profession}
- Personalidad: {', '.join(agent.personality_traits)}
- Dinero actual: ${agent.money:.2f}
- Energía actual: {agent.energy:.1f}/100
- Nivel de comestibles: {agent.grocery_level:.1f}/100
"""
        
        # Información del mundo
        world_info = self._build_world_info()
        
        # Memoria reciente
        memory_context = agent.memory.get_memory_context(window_hours=48)
        
        # Ubicaciones disponibles
        locations_info = self._build_locations_info()
        
        # Construir prompt completo
        prompt = f"""Eres {agent.name}, un agente consumidor en una simulación.

{agent_info}

{world_info}

{locations_info}

{memory_context}

Tarea: Planifica tu día. Es {day_name}, {hour:02d}:{minute:02d}. 
Genera un plan diario con actividades horarias desde las {hour:02d}:00 hasta las 23:00.

Responde SOLO con un JSON válido en este formato:
{{
    "plan": [
        {{"time": "08:00", "action": "move", "location": "office", "purpose": "ir a trabajar"}},
        {{"time": "12:00", "action": "buy", "location": "Coffee Shop", "product": "coffee", "purpose": "almuerzo"}},
        {{"time": "17:00", "action": "move", "location": "home", "purpose": "regresar a casa"}},
        {{"time": "19:00", "action": "rest", "location": "home", "purpose": "descansar"}}
    ],
    "reasoning": "Breve explicación de las decisiones del plan"
}}

Acciones disponibles:
- "move": Moverte a una ubicación
- "buy": Comprar un producto
- "rest": Descansar y recuperar energía
- "eat": Consumir alimentos del inventario
- "work": Trabajar (si estás en tu lugar de trabajo)

Importante: Sé realista con tu energía y dinero. Considera tus hábitos anteriores."""
        
        return prompt
    
    def build_action_reactor_prompt(self, agent: Agent, current_plan_item: Optional[Dict] = None) -> str:
        """
        Construye el prompt para el reactor de acciones (ejecutado cada hora).
        "¿Sigo el plan o cambio porque tengo hambre/vi un descuento?"
        """
        day, hour, minute = self.world_config.get_current_time()
        
        # Estado actual
        agent_state = agent.get_state_summary()
        
        # Información del mundo
        world_info = self._build_world_info()
        
        # Memoria reciente
        memory_context = agent.memory.get_memory_context(window_hours=24)
        
        # Ubicaciones cercanas con descuentos
        nearby_discounts = self._get_active_discounts()
        
        # Agentes cercanos
        nearby_agents = self._get_nearby_agents_info(agent)
        
        # Plan actual
        plan_info = ""
        if current_plan_item:
            plan_info = f"\nPlan actual para esta hora: {current_plan_item.get('action', 'none')} - {current_plan_item.get('purpose', '')}"
        elif agent.daily_plan:
            plan_info = "\nTienes un plan diario, pero no hay actividad específica para esta hora."
        
        prompt = f"""Eres {agent.name}, un agente consumidor en una simulación.

Estado Actual:
- Energía: {agent_state['energy']:.1f}/100
- Dinero: ${agent_state['money']:.2f}
- Comestibles: {agent_state['grocery_level']:.1f}/100
- Ubicación actual: {agent_state['location']}
- Coordenadas: {agent_state['coordinates']}
- Inventario: {agent_state['inventory_count']} items

{world_info}

{nearby_discounts}

{nearby_agents}

{plan_info}

{memory_context}

Tarea: Decide qué hacer AHORA (a las {hour:02d}:{minute:02d}).

Consideraciones:
- Tu energía es {agent_state['energy']:.1f}/100. Si es baja, considera descansar o comer.
- Tu dinero es ${agent_state['money']:.2f}. Gasta sabiamente.
- Hay descuentos activos en algunas tiendas (mencionados arriba).
- Puedes seguir tu plan o adaptarte a la situación actual.

Responde SOLO con un JSON válido en este formato:
{{
    "action": "buy|move|rest|eat|work|chat",
    "target_location": "nombre_de_ubicación o null",
    "target_product": "nombre_producto o null (solo si action=buy)",
    "target_agent": "id_agente o null (solo si action=chat)",
    "reasoning": "Breve explicación de tu decisión",
    "urgency": "high|medium|low"
}}"""
        
        return prompt
    
    def build_conversation_prompt(self, agent: Agent, other_agent: Agent) -> str:
        """
        Construye el prompt para generar conversaciones entre agentes.
        Se activa cuando hay agentes en la misma ubicación.
        """
        affinity = agent.get_affinity(other_agent.agent_id)
        relationship = "positiva" if affinity > 0.3 else "neutral" if affinity > -0.3 else "negativa"
        
        conversation_history = agent.memory.get_conversation_history(
            other_agent.agent_id, limit=5
        )
        
        history_text = ""
        if conversation_history:
            history_text = "\nHistorial de conversaciones previas:\n"
            for event in conversation_history:
                history_text += f"- {event.description}\n"
        
        prompt = f"""Eres {agent.name}, un agente consumidor en una simulación.

Te encuentras con {other_agent.name} ({other_agent.age} años, {other_agent.profession}).
Tu relación con {other_agent.name} es {relationship} (afinidad: {affinity:.2f}).

{history_text}

Estado actual:
- Tu energía: {agent.energy:.1f}/100
- Tu dinero: ${agent.money:.2f}
- Ubicación: {agent.current_location}

Genera un diálogo corto y natural entre tú y {other_agent.name}.

Responde SOLO con un JSON válido en este formato:
{{
    "dialogue": "El texto del diálogo que dices",
    "topic": "el_tema_de_la_conversación",
    "relationship_change": 0.1,
    "reasoning": "Breve explicación del diálogo"
}}

relationship_change puede ser positivo (acercamiento), negativo (alejamiento), o cercano a 0 (neutral)."""
        
        return prompt
    
    def _build_world_info(self) -> str:
        """Construye información sobre el estado del mundo"""
        day, hour, minute = self.world_config.get_current_time()
        day_name = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"][
            self.world_config.get_day_of_week()
        ]
        return f"\nEstado del Mundo:\n- Fecha: {day_name}, Día {day}, {hour:02d}:{minute:02d}\n"
    
    def _build_locations_info(self) -> str:
        """Construye información sobre las ubicaciones disponibles"""
        info = "\nUbicaciones Disponibles:\n"
        for location in self.locations.values():
            products = ", ".join(location.inventory.keys()) if location.inventory else "ninguno"
            info += f"- {location.name} ({location.location_type}) en {location.coordinates}\n"
            info += f"  Productos: {products}\n"
        return info
    
    def _get_active_discounts(self) -> str:
        """Retorna información sobre descuentos activos"""
        discounts = []
        for location in self.locations.values():
            if self.world_config.is_marketing_active(location.name):
                discount = self.world_config.get_discount(location.name)
                discounts.append(f"- {location.name}: {discount*100:.0f}% de descuento")
        
        if discounts:
            return "\nDescuentos Activos:\n" + "\n".join(discounts)
        return "\nNo hay descuentos activos en este momento."
    
    def _get_nearby_agents_info(self, agent: Agent) -> str:
        """Retorna información sobre agentes cercanos (se completará con la lista de agentes)"""
        # Este método se puede expandir cuando se pase la lista completa de agentes
        return "\nAgentes cercanos: (información disponible si hay interacciones)"





