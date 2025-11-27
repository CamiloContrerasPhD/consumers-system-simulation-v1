"""
Tomador de Decisiones
Gestiona las llamadas al LLM y clasifica las intenciones
"""

from typing import Dict, List, Optional, Tuple
from models.agent import Agent
from models.world_config import WorldConfig
from cognition.prompt_builder import PromptBuilder
from cognition.llm_client import LLMClient
import json
import concurrent.futures


class DecisionMaker:
    """
    Gestiona las decisiones de los agentes usando el LLM.
    Separa la lógica en tres tipos de llamadas:
    1. Daily Planner: Se ejecuta a las 7:00 AM
    2. Action Reactor: Se ejecuta cada hora
    3. Conversation Generator: Se activa cuando hay agentes cerca
    """
    
    def __init__(self, world_config: WorldConfig, locations: Dict, llm_client: LLMClient):
        self.world_config = world_config
        self.locations = locations
        self.llm_client = llm_client
        self.prompt_builder = PromptBuilder(world_config, locations)
    
    def plan_daily_activities(self, agent: Agent) -> Dict:
        """
        Daily Planner: Genera el plan del día (ejecutado a las 7 AM).
        Retorna el plan diario como diccionario.
        """
        prompt = self.prompt_builder.build_daily_planner_prompt(agent)
        
        try:
            response = self.llm_client.call(prompt)
            plan_data = self._parse_json_response(response)
            
            if "plan" in plan_data:
                agent.daily_plan = plan_data["plan"]
                agent.is_planning_day = True
                return plan_data
            else:
                return {"plan": [], "reasoning": "No se pudo generar un plan válido"}
        
        except Exception as e:
            print(f"Error al planificar día para {agent.name}: {e}")
            return {"plan": [], "reasoning": f"Error: {str(e)}"}
    
    def decide_action(self, agent: Agent, current_plan_item: Optional[Dict] = None) -> Dict:
        """
        Action Reactor: Decide qué hacer ahora (ejecutado cada hora).
        Retorna una decisión de acción como diccionario.
        """
        prompt = self.prompt_builder.build_action_reactor_prompt(agent, current_plan_item)
        
        try:
            response = self.llm_client.call(prompt)
            decision = self._parse_json_response(response)
            
            # Validar estructura de decisión
            if "action" not in decision:
                decision = {"action": "rest", "reasoning": "Decisión inválida, descansando"}
            
            return decision
        
        except Exception as e:
            print(f"Error al decidir acción para {agent.name}: {e}")
            return {
                "action": "rest",
                "target_location": None,
                "target_product": None,
                "reasoning": f"Error: {str(e)}"
            }
    
    def generate_conversation(self, agent: Agent, other_agent: Agent) -> Dict:
        """
        Conversation Generator: Genera un diálogo entre dos agentes.
        Retorna el diálogo generado.
        """
        prompt = self.prompt_builder.build_conversation_prompt(agent, other_agent)
        
        try:
            response = self.llm_client.call(prompt)
            conversation = self._parse_json_response(response)
            
            return conversation
        
        except Exception as e:
            print(f"Error al generar conversación entre {agent.name} y {other_agent.name}: {e}")
            return {
                "dialogue": f"{agent.name}: Hola, {other_agent.name}!",
                "topic": "saludo",
                "relationship_change": 0.0,
                "reasoning": f"Error: {str(e)}"
            }
    
    def plan_daily_parallel(self, agents: List[Agent]) -> Dict[str, Dict]:
        """
        Planifica el día para múltiples agentes en paralelo.
        Retorna un diccionario {agent_id: plan}
        """
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            future_to_agent = {
                executor.submit(self.plan_daily_activities, agent): agent
                for agent in agents
            }
            
            results = {}
            for future in concurrent.futures.as_completed(future_to_agent):
                agent = future_to_agent[future]
                try:
                    plan = future.result()
                    results[agent.agent_id] = plan
                except Exception as e:
                    print(f"Error al planificar para {agent.name}: {e}")
                    results[agent.agent_id] = {"plan": [], "reasoning": str(e)}
            
            return results
    
    def decide_actions_parallel(self, agents: List[Agent], 
                                plan_items: Optional[Dict[str, Dict]] = None) -> Dict[str, Dict]:
        """
        Decide acciones para múltiples agentes en paralelo.
        Retorna un diccionario {agent_id: decision}
        """
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            future_to_agent = {
                executor.submit(
                    self.decide_action,
                    agent,
                    plan_items.get(agent.agent_id) if plan_items else None
                ): agent
                for agent in agents
            }
            
            results = {}
            for future in concurrent.futures.as_completed(future_to_agent):
                agent = future_to_agent[future]
                try:
                    decision = future.result()
                    results[agent.agent_id] = decision
                except Exception as e:
                    print(f"Error al decidir para {agent.name}: {e}")
                    results[agent.agent_id] = {"action": "rest", "reasoning": str(e)}
            
            return results
    
    def _parse_json_response(self, response: str) -> Dict:
        """
        Parsea la respuesta del LLM extrayendo JSON.
        Maneja casos donde el LLM puede incluir texto adicional.
        """
        # Intentar extraer JSON del texto
        response = response.strip()
        
        # Buscar inicio de JSON
        start_idx = response.find('{')
        end_idx = response.rfind('}') + 1
        
        if start_idx != -1 and end_idx > start_idx:
            json_str = response[start_idx:end_idx]
            try:
                return json.loads(json_str)
            except json.JSONDecodeError as e:
                print(f"Error al parsear JSON: {e}")
                print(f"Texto recibido: {json_str}")
                return {}
        
        # Si no se encontró JSON, retornar diccionario vacío
        return {}






