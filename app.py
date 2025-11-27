"""
Aplicación Principal de Simulación Multi-Agente
Interfaz Streamlit para visualización y control
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os
from typing import Dict, List, Optional
from datetime import datetime
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Importar módulos del sistema
from models.world_config import WorldConfig
from models.location import Location
from models.agent import Agent
from engine.time_manager import TimeManager
from engine.interaction_engine import InteractionEngine
from engine.transaction_system import TransactionSystem
from cognition.llm_client import LLMClient
from cognition.decision_maker import DecisionMaker
from cognition.response_parser import ResponseParser


# ============ SISTEMA DE TRADUCCIONES (i18n) ============

TRANSLATIONS = {
    "es": {
        # General
        "page_title": "Sistema de Simulación Multi-Agente",
        "subtitle": "Simulación de comportamiento de consumidores con IA",
        "title": "MarketSim AI Behavioral Lab",
        
        # Language selector
        "language": "Idioma",
        "spanish": "Español",
        "english": "English",
        
        # API Configuration
        "api_config": "Configuración de API",
        "api_key_input": "DeepSeek API Key",
        "api_key_placeholder": "Ingresa tu API key aquí...",
        "api_key_save": "Guardar API Key",
        "api_key_clear": "Limpiar",
        "api_key_saved": "✅ API Key guardada (solo para esta sesión)",
        "api_key_cleared": "API Key eliminada",
        "use_env_key": "Usar API Key del archivo .env",
        "api_connected": "DeepSeek API Conectada",
        "api_not_connected": "DeepSeek API No Conectada",
        "api_key_missing": "⚠️ DEEPSEEK_API_KEY no configurada. El sistema funcionará en modo simulado.",
        
        # Sidebar
        "command_center": "🎮 Command Center",
        "setup": "⚙️ Setup",
        "initialize_simulation": "🔄 Inicializar Simulación",
        "load_config": "📁 Cargar Configuración",
        "upload_json": "Subir JSON de configuración",
        "active_campaigns": "📊 Campañas Activas",
        "no_active_campaigns": "No hay campañas activas",
        "campaign_manager": "📊 Campaign Manager",
        "create_campaign": "Crear Nueva Campaña",
        "target_location": "Ubicación Objetivo",
        "discount_strategy": "Estrategia de Descuento (%)",
        "day_of_week": "Día de la Semana",
        "start_time": "Hora de Inicio",
        "end_time": "Hora de Fin",
        "time_window": "Ventana de Tiempo",
        "deploy_campaign": "🚀 Desplegar Campaña",
        "campaign_status": "📊 Estado de la Campaña",
        "campaign_active": "🟢 **Campaña ACTIVA**",
        "campaign_inactive": "🔴 **Campaña INACTIVA**",
        "simulation_controls": "🎮 Controles de Simulación",
        "play": "▶️ Play",
        "pause": "⏸️ Pause",
        "next_hour": "⏩ Siguiente Hora",
        "skip_to_campaign": "⏭️ Saltar a",
        "clear_log": "🗑️ Limpiar Log",
        "day": "Día",
        "hour": "Hora",
        "active": "Activa",
        "inactive": "Inactiva",
        "cancel": "Cancelar",
        "discount": "descuento",
        
        # Days of week
        "monday": "Lunes",
        "tuesday": "Martes",
        "wednesday": "Miércoles",
        "thursday": "Jueves",
        "friday": "Viernes",
        "saturday": "Sábado",
        "sunday": "Domingo",
        
        # Main content
        "quick_metrics": "📊 Métricas Rápidas (KPIs Globales)",
        "active_agents": "Agentes Activos",
        "total_spending": "Gasto Total Hoy",
        "active_campaigns_label": "Campañas Activas",
        
        # Tabs
        "tab_live_monitor": "🗺️ Monitoreo en Vivo",
        "tab_campaign_manager": "📊 Gestor de Campañas",
        "tab_market_intelligence": "📈 Inteligencia de Mercado",
        "tab_agent_telemetry": "👥 Telemetría de Agentes",
        
        # Events
        "day_start": "🌅 Inicio de nuevo día - Los agentes están planificando sus actividades",
        "campaign_active_msg": "🎯 Campaña ACTIVA: {}% descuento en {} (Horario: {:02d}:00-{:02d}:00)",
        "simulation_not_initialized": "⚠️ Simulación no inicializada correctamente",
        
        # Charts
        "urban_heatmap": "Urban Heatmap",
        "sales_chart": "Ventas Totales por Ubicación",
        "loyalty_matrix": "Matriz de Lealtad - Visitas por Agente y Ubicación",
        "social_graph": "Relaciones Sociales - Afinidad entre Agentes",
        "no_sales_data": "No hay datos de ventas aún",
        "no_loyalty_data": "No hay datos de lealtad aún",
        "no_social_data": "No hay relaciones sociales registradas aún",
        
        # Agent telemetry
        "agent_telemetry": "Telemetría de Agente (Feed de Eventos)",
        "agent_details": "👤 Agente {} ({} años, {})",
        "wallet": "Billetera",
        "energy": "Energía",
        "grocery_level": "Nivel de Comestibles",
        "location": "Ubicación",
        "coordinates": "Coordenadas",
        "inventory": "Inventario",
        "inventory_empty": "Vacío",
        "reasoning": "🧠 Razonamiento",
        "personality": "Personalidad",
        "waiting_decisions": "Esperando próximas decisiones...",
        
        # Welcome
        "welcome": "👈 Usa el panel lateral para inicializar la simulación",
        "welcome_title": "Bienvenido al Sistema de Simulación Multi-Agente",
        "welcome_description": "Este sistema simula el comportamiento de consumidores usando IA.",
        "features_title": "**Características:**",
        "feature_agents": "🤖 Agentes con personalidad y necesidades dinámicas",
        "feature_world": "🗺️ Mundo con ubicaciones y productos",
        "feature_economy": "💰 Sistema económico con campañas de marketing",
        "feature_llm": "🧠 Toma de decisiones mediante LLM (DeepSeek)",
        "feature_visualization": "📊 Visualización en tiempo real",
        "steps_title": "**Pasos para comenzar:**",
        "step1": "1. Configura tu API key de DeepSeek (en el panel lateral o archivo .env)",
        "step2": "2. Haz clic en \"Inicializar Simulación\" en el panel lateral",
        "step3": "3. Usa \"Ejecutar Siguiente Hora\" para avanzar la simulación",
        "step4": "4. Observa el comportamiento de los agentes en tiempo real",
    },
    "en": {
        # General
        "page_title": "Multi-Agent Simulation System",
        "subtitle": "AI-powered consumer behavior simulation",
        "title": "MarketSim AI Behavioral Lab",
        
        # Language selector
        "language": "Language",
        "spanish": "Español",
        "english": "English",
        
        # API Configuration
        "api_config": "API Configuration",
        "api_key_input": "DeepSeek API Key",
        "api_key_placeholder": "Enter your API key here...",
        "api_key_save": "Save API Key",
        "api_key_clear": "Clear",
        "api_key_saved": "✅ API Key saved (session only)",
        "api_key_cleared": "API Key cleared",
        "use_env_key": "Use API Key from .env file",
        "api_connected": "DeepSeek API Connected",
        "api_not_connected": "DeepSeek API Not Connected",
        "api_key_missing": "⚠️ DEEPSEEK_API_KEY not configured. The system will run in simulated mode.",
        
        # Sidebar
        "command_center": "🎮 Command Center",
        "setup": "⚙️ Setup",
        "initialize_simulation": "🔄 Initialize Simulation",
        "load_config": "📁 Load Configuration",
        "upload_json": "Upload JSON configuration file",
        "active_campaigns": "📊 Active Campaigns",
        "no_active_campaigns": "No active campaigns",
        "campaign_manager": "📊 Campaign Manager",
        "create_campaign": "Create New Campaign",
        "target_location": "Target Location",
        "discount_strategy": "Discount Strategy (%)",
        "day_of_week": "Day of Week",
        "start_time": "Start Time",
        "end_time": "End Time",
        "time_window": "Time Window",
        "deploy_campaign": "🚀 Deploy Campaign",
        "campaign_status": "📊 Campaign Status",
        "campaign_active": "🟢 **Campaign ACTIVE**",
        "campaign_inactive": "🔴 **Campaign INACTIVE**",
        "simulation_controls": "🎮 Simulation Controls",
        "play": "▶️ Play",
        "pause": "⏸️ Pause",
        "next_hour": "⏩ Next Hour",
        "skip_to_campaign": "⏭️ Skip to",
        "clear_log": "🗑️ Clear Log",
        "day": "Day",
        "hour": "Hour",
        "active": "Active",
        "inactive": "Inactive",
        "cancel": "Cancel",
        "discount": "discount",
        
        # Days of week
        "monday": "Monday",
        "tuesday": "Tuesday",
        "wednesday": "Wednesday",
        "thursday": "Thursday",
        "friday": "Friday",
        "saturday": "Saturday",
        "sunday": "Sunday",
        
        # Main content
        "quick_metrics": "📊 Quick Metrics (Global KPIs)",
        "active_agents": "Active Agents",
        "total_spending": "Total Spending Today",
        "active_campaigns_label": "Active Campaigns",
        
        # Tabs
        "tab_live_monitor": "🗺️ Live Monitor",
        "tab_campaign_manager": "📊 Campaign Manager",
        "tab_market_intelligence": "📈 Market Intelligence",
        "tab_agent_telemetry": "👥 Agent Telemetry",
        
        # Events
        "day_start": "🌅 Start of new day - Agents are planning their activities",
        "campaign_active_msg": "🎯 Campaign ACTIVE: {}% discount at {} (Time: {:02d}:00-{:02d}:00)",
        "simulation_not_initialized": "⚠️ Simulation not properly initialized",
        
        # Charts
        "urban_heatmap": "Urban Heatmap",
        "sales_chart": "Total Sales by Location",
        "loyalty_matrix": "Loyalty Matrix - Visits by Agent and Location",
        "social_graph": "Social Relationships - Affinity between Agents",
        "no_sales_data": "No sales data yet",
        "no_loyalty_data": "No loyalty data yet",
        "no_social_data": "No social relationships registered yet",
        
        # Agent telemetry
        "agent_telemetry": "Agent Telemetry (Event Feed)",
        "agent_details": "👤 Agent {} ({} years old, {})",
        "wallet": "Wallet",
        "energy": "Energy",
        "grocery_level": "Grocery Level",
        "location": "Location",
        "coordinates": "Coordinates",
        "inventory": "Inventory",
        "inventory_empty": "Empty",
        "reasoning": "🧠 Reasoning",
        "personality": "Personality",
        "waiting_decisions": "Waiting for upcoming decisions...",
        
        # Welcome
        "welcome": "👈 Use the sidebar to initialize the simulation",
        "welcome_title": "Welcome to the Multi-Agent Simulation System",
        "welcome_description": "This system simulates consumer behavior using AI.",
        "features_title": "**Features:**",
        "feature_agents": "🤖 Agents with personality and dynamic needs",
        "feature_world": "🗺️ World with locations and products",
        "feature_economy": "💰 Economic system with marketing campaigns",
        "feature_llm": "🧠 Decision making through LLM (DeepSeek)",
        "feature_visualization": "📊 Real-time visualization",
        "steps_title": "**Steps to get started:**",
        "step1": "1. Configure your DeepSeek API key (in sidebar or .env file)",
        "step2": "2. Click \"Initialize Simulation\" in the sidebar",
        "step3": "3. Use \"Execute Next Hour\" to advance the simulation",
        "step4": "4. Observe agent behavior in real-time",
    }
}


def get_translation(key: str, *args) -> str:
    """Get translation for current language"""
    lang = st.session_state.get("language", "es")
    text = TRANSLATIONS.get(lang, TRANSLATIONS["es"]).get(key, key)
    if args:
        try:
            return text.format(*args)
        except:
            return text
    return text


def t(key: str, *args) -> str:
    """Shortcut for get_translation"""
    return get_translation(key, *args)


def get_day_names() -> List[str]:
    """Get list of day names in current language"""
    return [t("monday"), t("tuesday"), t("wednesday"), t("thursday"), 
            t("friday"), t("saturday"), t("sunday")]


def get_day_map() -> Dict[str, int]:
    """Get mapping of day names to numbers"""
    day_names = get_day_names()
    return {day: idx for idx, day in enumerate(day_names)}


# ============ CONFIGURACIÓN INICIAL ============

# Initialize language (default: Spanish)
if "language" not in st.session_state:
    st.session_state.language = "es"

# Initialize user API key
if "user_api_key" not in st.session_state:
    st.session_state.user_api_key = None

# Initialize API key source preference
if "api_key_source" not in st.session_state:
    st.session_state.api_key_source = "user"  # "user" or "env"

# Configuración de la página
st.set_page_config(
    page_title=t("page_title"),
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar estado de sesión
if "world_config" not in st.session_state:
    st.session_state.world_config = None
if "locations" not in st.session_state:
    st.session_state.locations = {}
if "agents" not in st.session_state:
    st.session_state.agents = []
if "simulation_running" not in st.session_state:
    st.session_state.simulation_running = False
if "event_log" not in st.session_state:
    st.session_state.event_log = []
if "llm_client" not in st.session_state:
    st.session_state.llm_client = None
if "decision_maker" not in st.session_state:
    st.session_state.decision_maker = None
if "response_parser" not in st.session_state:
    st.session_state.response_parser = None
if "last_campaign_check" not in st.session_state:
    st.session_state.last_campaign_check = {}  # Para rastrear campañas activas


# ============ FUNCIÓN PARA OBTENER API KEY ============

def get_api_key() -> Optional[str]:
    """Get API key prioritizing user input over .env"""
    # Priority 1: User-provided API key
    if st.session_state.user_api_key:
        return st.session_state.user_api_key
    
    # Priority 2: .env file (only if user hasn't set preference)
    if st.session_state.api_key_source == "env":
        return os.getenv("DEEPSEEK_API_KEY")
    
    # Check if .env key exists
    env_key = os.getenv("DEEPSEEK_API_KEY")
    if env_key:
        # If .env exists and no user key, use .env
        return env_key
    
    return None


def initialize_simulation():
    """Inicializa la simulación con configuración básica"""
    # Crear configuración del mundo
    world_config = WorldConfig(width=10, height=10)
    
    # Crear ubicaciones básicas
    locations = {
        "home": Location(
            name="Casa",
            coordinates=(0, 0),
            location_type="Residence",
            capacity=5
        ),
        "Coffee Shop": Location(
            name="Coffee Shop",
            coordinates=(3, 3),
            location_type="Restaurant",
            capacity=10
        ),
        "Grocery Store": Location(
            name="Grocery Store",
            coordinates=(5, 5),
            location_type="Grocery",
            capacity=15
        ),
        "Chicken Shop": Location(
            name="Chicken Shop",
            coordinates=(7, 7),
            location_type="Restaurant",
            capacity=8
        ),
        "office": Location(
            name="Oficina",
            coordinates=(2, 2),
            location_type="Work",
            capacity=20
        )
    }
    
    # Añadir productos a las ubicaciones
    locations["Coffee Shop"].add_product("coffee", price=5.0, stock=100, satisfies_need="energy")
    locations["Coffee Shop"].add_product("sandwich", price=8.0, stock=50, satisfies_need="energy")
    locations["Grocery Store"].add_product("groceries", price=30.0, stock=200, satisfies_need="energy")
    locations["Chicken Shop"].add_product("chicken", price=12.0, stock=80, satisfies_need="energy")
    
    # Crear agentes básicos
    agents = [
        Agent(
            agent_id="agent_1",
            name="María",
            age=28,
            profession="Ingeniera",
            personality_traits=["extrovert", "health_conscious"],
            money=500.0,
            energy=100.0,
            home_location="home",
            work_location="office",
            coordinates=(0, 0),
            current_location="home"
        ),
        Agent(
            agent_id="agent_2",
            name="David",
            age=35,
            profession="Diseñador",
            personality_traits=["introvert", "thrifty"],
            money=600.0,
            energy=100.0,
            home_location="home",
            work_location="office",
            coordinates=(0, 0),
            current_location="home"
        ),
        Agent(
            agent_id="agent_3",
            name="Lisa",
            age=25,
            profession="Estudiante",
            personality_traits=["impulsive", "social"],
            money=300.0,
            energy=100.0,
            home_location="home",
            work_location=None,
            coordinates=(0, 0),
            current_location="home"
        )
    ]
    
    # Configurar campaña de marketing
    world_config.marketing_campaigns = [
        {
            "location_name": "Chicken Shop",
            "discount_percent": 20,
            "day_of_week": 2,  # Miércoles
            "start_hour": 12,
            "end_hour": 14
        }
    ]
    
    # Inicializar motores
    time_manager = TimeManager(world_config)
    interaction_engine = InteractionEngine(world_config)
    transaction_system = TransactionSystem(world_config)
    
    # Inicializar cliente LLM
    api_key = get_api_key()
    if api_key:
        llm_client = LLMClient(api_key=api_key)
        decision_maker = DecisionMaker(world_config, locations, llm_client)
        response_parser = ResponseParser(
            world_config, locations, interaction_engine, transaction_system
        )
    else:
        llm_client = None
        decision_maker = None
        response_parser = None
        st.warning(t("api_key_missing"))
    
    # Guardar en session state
    st.session_state.world_config = world_config
    st.session_state.locations = locations
    st.session_state.agents = agents
    st.session_state.time_manager = time_manager
    st.session_state.interaction_engine = interaction_engine
    st.session_state.transaction_system = transaction_system
    st.session_state.llm_client = llm_client
    st.session_state.decision_maker = decision_maker
    st.session_state.response_parser = response_parser


def load_config_from_json(uploaded_file):
    """Carga configuración desde un archivo JSON"""
    try:
        data = json.load(uploaded_file)
        
        # Crear world_config
        world_config = WorldConfig(
            width=data.get("world", {}).get("width", 10),
            height=data.get("world", {}).get("height", 10)
        )
        
        # Crear ubicaciones
        locations = {}
        for loc_data in data.get("locations", []):
            location = Location(
                name=loc_data["name"],
                coordinates=(loc_data["x"], loc_data["y"]),
                location_type=loc_data.get("type", "Shop"),
                capacity=loc_data.get("capacity", 10)
            )
            for product in loc_data.get("products", []):
                location.add_product(
                    product["name"],
                    product["price"],
                    product.get("stock", 100),
                    product.get("satisfies_need", "energy")
                )
            locations[loc_data["name"]] = location
        
        # Crear agentes
        agents = []
        for agent_data in data.get("agents", []):
            agent = Agent(
                agent_id=agent_data["id"],
                name=agent_data["name"],
                age=agent_data["age"],
                profession=agent_data["profession"],
                personality_traits=agent_data.get("traits", []),
                money=agent_data.get("money", 500.0),
                energy=agent_data.get("energy", 100.0),
                home_location=agent_data.get("home", "home"),
                work_location=agent_data.get("work"),
                coordinates=(0, 0),
                current_location=agent_data.get("home", "home")
            )
            agents.append(agent)
        
        # Configurar marketing
        world_config.marketing_campaigns = data.get("marketing", [])
        
        # Actualizar session state
        st.session_state.world_config = world_config
        st.session_state.locations = locations
        st.session_state.agents = agents
        
        st.success(f"✅ Configuración cargada: {len(locations)} ubicaciones, {len(agents)} agentes")
        return True
    
    except Exception as e:
        st.error(f"Error al cargar configuración: {e}")
        return False


def execute_tick():
    """Ejecuta un tick de simulación (avanza una hora)"""
    world_config = st.session_state.world_config
    agents = st.session_state.agents
    locations = st.session_state.locations
    time_manager = st.session_state.time_manager
    interaction_engine = st.session_state.interaction_engine
    decision_maker = st.session_state.decision_maker
    response_parser = st.session_state.response_parser
    
    if not all([world_config, agents, time_manager, interaction_engine]):
        st.error(t("simulation_not_initialized"))
        return
    
    # 1. Avanzar tiempo
    is_morning = time_manager.advance_tick(agents)
    
    # 2. Si es la mañana (7 AM), planificar el día
    if is_morning and decision_maker:
        st.session_state.event_log.append({
            "time": time_manager.get_time_string(),
            "type": "system",
            "message": t("day_start")
        })
        
        # Planificar día para todos los agentes en paralelo
        plans = decision_maker.plan_daily_parallel(agents)
        for agent in agents:
            if agent.agent_id in plans:
                agent.daily_plan = plans[agent.agent_id].get("plan", [])
    
    # 3. Verificar si alguna campaña se activó o desactivó
    day, hour, minute = world_config.get_current_time()
    current_time_key = f"{day}_{hour}"
    
    for campaign in world_config.marketing_campaigns:
        location_name = campaign.get("location_name")
        campaign_key = f"{location_name}_{current_time_key}"
        is_active = world_config.is_marketing_active(location_name)
        
        # Solo registrar si la campaña está activa y no la registramos en esta hora
        if is_active and campaign_key not in st.session_state.last_campaign_check:
            st.session_state.last_campaign_check[campaign_key] = True
            st.session_state.event_log.append({
                "time": time_manager.get_time_string(),
                "type": "system",
                "message": t("campaign_active_msg", 
                           campaign.get('discount_percent', 0), 
                           location_name,
                           campaign.get('start_hour', 0),
                           campaign.get('end_hour', 24))
            })
    
    # Limpiar checks antiguos (mantener solo las últimas 24 horas)
    keys_to_remove = [k for k in st.session_state.last_campaign_check.keys() 
                     if not k.endswith(current_time_key) and 
                     int(k.split('_')[-2]) < day - 1]
    for key in keys_to_remove:
        del st.session_state.last_campaign_check[key]
    
    # 3. Para cada agente, decidir acción
    day, hour, minute = world_config.get_current_time()
    
    if decision_maker and response_parser:
        # Decidir acciones en paralelo
        decisions = decision_maker.decide_actions_parallel(agents)
        
        # Ejecutar decisiones
        for agent in agents:
            if agent.agent_id in decisions:
                decision = decisions[agent.agent_id]
                success, message = response_parser.parse_and_execute_decision(agent, decision)
                
                if success:
                    st.session_state.event_log.append({
                        "time": time_manager.get_time_string(),
                        "type": "action",
                        "agent": agent.name,
                        "message": message
                    })
    
    # 4. Detectar y procesar interacciones sociales
    if interaction_engine:
        for agent in agents:
            nearby_agents = interaction_engine.detect_same_location(agent, agents)
            
            if nearby_agents and decision_maker:
                # Generar conversación con el primer agente cercano
                other_agent = nearby_agents[0]
                conversation = decision_maker.generate_conversation(agent, other_agent)
                
                # Actualizar relaciones
                relationship_change = conversation.get("relationship_change", 0.0)
                agent.update_relationship(other_agent.agent_id, relationship_change)
                other_agent.update_relationship(agent.agent_id, relationship_change)
                
                # Registrar evento
                day, hour, minute = world_config.get_current_time()
                agent.memory.add_event(
                    timestamp=(day, hour, minute),
                    event_type="Chat",
                    description=conversation.get("dialogue", ""),
                    location=agent.current_location,
                    other_agent_id=other_agent.agent_id
                )
                
                other_agent.memory.add_event(
                    timestamp=(day, hour, minute),
                    event_type="Chat",
                    description=conversation.get("dialogue", ""),
                    location=agent.current_location,
                    other_agent_id=agent.agent_id
                )
                
                st.session_state.event_log.append({
                    "time": time_manager.get_time_string(),
                    "type": "chat",
                    "agent": agent.name,
                    "other_agent": other_agent.name,
                    "message": conversation.get("dialogue", "")
                })
    
    # 5. Limitar tamaño del log
    if len(st.session_state.event_log) > 100:
        st.session_state.event_log = st.session_state.event_log[-100:]


def create_map_visualization():
    """Crea visualización del mapa con agentes y ubicaciones"""
    world_config = st.session_state.world_config
    agents = st.session_state.agents
    locations = st.session_state.locations
    
    if not world_config or not agents:
        return None
    
    # Crear DataFrame para ubicaciones
    loc_data = []
    for loc in locations.values():
        x, y = loc.coordinates
        loc_data.append({
            "x": x,
            "y": y,
            "name": loc.name,
            "type": loc.location_type,
            "size": loc.capacity
        })
    
    # Crear DataFrame para agentes
    agent_data = []
    for agent in agents:
        x, y = agent.coordinates
        agent_data.append({
            "x": x,
            "y": y,
            "name": agent.name,
            "energy": agent.energy,
            "money": agent.money
        })
    
    # Crear gráfico
    fig = go.Figure()
    
    # Añadir ubicaciones con colores según tipo
    if loc_data:
        loc_df = pd.DataFrame(loc_data)
        
        # Colores según tipo de ubicación
        type_colors = {
            "Residence": "#28a745",      # Verde - Residencial
            "Restaurant": "#fd7e14",     # Naranja - Comercio
            "Shop": "#fd7e14",           # Naranja - Comercio
            "Grocery": "#fd7e14",        # Naranja - Comercio
            "Work": "#007bff",           # Azul - Oficinas
            "Office": "#007bff"          # Azul - Oficinas
        }
        
        # Verificar si hay campañas activas para resaltar ubicaciones
        active_campaign_location = None
        if world_config.marketing_campaigns:
            campaign = world_config.marketing_campaigns[0]
            is_active_day = (campaign.get("day_of_week") == world_config.get_day_of_week())
            is_active_hour = (campaign.get("start_hour", 0) <= world_config.current_hour < campaign.get("end_hour", 24))
            if is_active_day and is_active_hour:
                active_campaign_location = campaign.get("location_name")
        
        for _, row in loc_df.iterrows():
            color = type_colors.get(row["type"], "#6c757d")
            size = row["size"] * 3 + 15
            
            # Resaltar ubicación con campaña activa
            show_circle = False
            if active_campaign_location and row["name"] == active_campaign_location:
                color = "#ff00ff"  # Rosa/brillante para campaña activa
                show_circle = True
            
            fig.add_trace(go.Scatter(
                x=[row["x"]],
                y=[row["y"]],
                mode="markers+text",
                marker=dict(
                    size=size,
                    color=color,
                    symbol="square",
                    line=dict(width=3 if show_circle else 2, color="white" if show_circle else "black"),
                    opacity=0.9
                ),
                text=[row["name"]],
                textposition="middle center",
                name="Buildings",
                hovertemplate=f"<b>{row['name']}</b><br>Type: {row['type']}<br>Coordinates: ({row['x']}, {row['y']})<extra></extra>",
                showlegend=False if _ > 0 else True
            ))
            
            # Añadir círculo brillante para campaña activa
            if show_circle:
                fig.add_trace(go.Scatter(
                    x=[row["x"]],
                    y=[row["y"]],
                    mode="markers",
                    marker=dict(
                        size=size + 15,
                        color="rgba(255, 0, 255, 0.3)",
                        line=dict(width=2, color="#ff00ff"),
                        symbol="circle"
                    ),
                    name="Active Campaign",
                    hovertemplate=f"<b>OFERTA ACTIVA ({campaign.get('discount_percent', 0)}%)</b><extra></extra>",
                    showlegend=True
                ))
    
    # Añadir agentes como puntos de colores
    if agent_data:
        agent_df = pd.DataFrame(agent_data)
        
        # Colores según nivel de energía
        def get_agent_color(energy):
            if energy > 70:
                return "#28a745"  # Verde
            elif energy > 30:
                return "#ffc107"  # Amarillo
            else:
                return "#dc3545"  # Rojo
        
        agent_colors = agent_df["energy"].apply(get_agent_color)
        
        fig.add_trace(go.Scatter(
            x=agent_df["x"],
            y=agent_df["y"],
            mode="markers+text",
            marker=dict(
                size=12,
                color=agent_colors,
                line=dict(width=2, color="white"),
                opacity=0.9
            ),
            text=agent_df["name"],
            textposition="middle center",
            textfont=dict(size=8, color="white"),
            name="Agents",
            hovertemplate="<b>%{text}</b><br>Hambre: Alta<br>Dinero: $%{customdata:.2f}<br>Coordenadas: (%{x}, %{y})<extra></extra>",
            customdata=agent_df["money"]
        ))
    
    fig.update_layout(
        title="Urban Heatmap - Agents and Locations",
        xaxis_title="X",
        yaxis_title="Y",
        xaxis=dict(range=[-1, world_config.width + 1], showgrid=True, gridcolor="rgba(255,255,255,0.1)"),
        yaxis=dict(range=[-1, world_config.height + 1], showgrid=True, gridcolor="rgba(255,255,255,0.1)"),
        height=700,
        showlegend=True,
        legend=dict(
            title="Legend",
            itemsizing="constant",
            orientation="v",
            x=1.02,
            y=1,
            bgcolor="rgba(0,0,0,0)",
            bordercolor="rgba(255,255,255,0.2)"
        ),
        hovermode='closest',
        template="plotly_dark"
    )
    
    return fig


def create_sales_chart():
    """Crea gráfico de ventas por ubicación"""
    locations = st.session_state.locations
    
    if not locations:
        return None
    
    sales_data = []
    for loc in locations.values():
        sales_data.append({
            "Location": loc.name,
            "Total Sales": loc.total_sales,
            "Visits": loc.visit_count
        })
    
    df = pd.DataFrame(sales_data)
    
    fig = px.bar(
        df,
        x="Location",
        y="Total Sales",
        title="Ventas Totales por Ubicación",
        labels={"Total Sales": "Ventas ($)", "Location": "Ubicación"}
    )
    
    return fig


def create_loyalty_matrix():
    """Crea matriz de lealtad (visitas repetidas por agente)"""
    agents = st.session_state.agents
    locations = st.session_state.locations
    
    if not agents or not locations:
        return None
    
    # Crear matriz de visitas
    loyalty_data = []
    for agent in agents:
        for loc_name in locations.keys():
            visits = len([
                e for e in agent.memory.get_events_at_location(loc_name, limit=1000)
                if e.event_type == "Purchase" or e.event_type == "Move"
            ])
            loyalty_data.append({
                "Agent": agent.name,
                "Location": loc_name,
                "Visits": visits
            })
    
    df = pd.DataFrame(loyalty_data)
    
    if df.empty:
        return None
    
    pivot_df = df.pivot(index="Agent", columns="Location", values="Visits").fillna(0)
    
    fig = px.imshow(
        pivot_df,
        labels=dict(x="Ubicación", y="Agente", color="Visitas"),
        title="Matriz de Lealtad - Visitas por Agente y Ubicación",
        aspect="auto",
        color_continuous_scale="Blues"
    )
    
    return fig


def create_social_graph():
    """Crea gráfico de relaciones sociales"""
    agents = st.session_state.agents
    
    if not agents:
        return None
    
    edges = []
    for agent in agents:
        for other_id, affinity in agent.relationships.items():
            other_agent = next((a for a in agents if a.agent_id == other_id), None)
            if other_agent:
                edges.append({
                    "from": agent.name,
                    "to": other_agent.name,
                    "affinity": affinity
                })
    
    if not edges:
        return None
    
    # Crear gráfico de red simple con Plotly
    df_edges = pd.DataFrame(edges)
    
    # Crear nodos
    nodes = pd.DataFrame({
        "name": [a.name for a in agents],
        "energy": [a.energy for a in agents]
    })
    
    # Visualización simplificada como gráfico de barras de afinidad
    fig = px.bar(
        df_edges,
        x="from",
        y="affinity",
        color="to",
        title="Relaciones Sociales - Afinidad entre Agentes",
        labels={"from": "Agente", "affinity": "Afinidad", "to": "Con"},
        barmode="group"
    )
    
    return fig


    
    # Paso 1: Inicialización
    st.subheader("📍 Paso 1: Inicializar la Simulación")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        **¿Qué debes hacer?**
        
        1. 👉 **Busca el panel lateral izquierdo** (si está oculto, haz clic en la flecha ⬅️ en la esquina superior)
        2. 👉 **Haz clic en el botón "🔄 Inicializar Simulación"**
        3. ✅ Verás un mensaje confirmando que la simulación se inicializó
        
        **¿Qué esperar?**
        - Se crearán **3 agentes** (María, David, Lisa) con diferentes personalidades
        - Se crearán **5 ubicaciones** (Casa, Coffee Shop, Grocery Store, Chicken Shop, Oficina)
        - El reloj comenzará en **Día 0, 7:00 AM**
        - Todos los agentes empezarán en casa
        """)
    
    with col2:
        st.info("""
        💡 **Tip:**
        
        Si no ves los botones en el panel lateral, asegúrate de que la barra lateral esté visible.
        """)
    
    st.markdown("---")
    
    # Paso 2: Configurar Campaña
    st.subheader("🎯 Paso 2: Configurar una Campaña de Marketing")
    
    st.markdown("""
    **¿Qué debes hacer?**
    
    En el panel lateral, dentro de la sección **"📊 Variables de Marketing"**, encontrarás:
    """)
    
    # Mostrar ejemplo visual de la configuración
    with st.expander("📋 Ver campos de configuración de campaña", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            **1️⃣ Ubicación con descuento**
            - Selecciona la tienda donde aplicar el descuento
            - Ejemplo: "Chicken Shop"
            """)
        
        with col2:
            st.markdown("""
            **2️⃣ Porcentaje de descuento**
            - Usa el slider para elegir el % (0-50%)
            - Ejemplo: 20% de descuento
            """)
        
        with col3:
            st.markdown("""
            **3️⃣ Día de la semana**
            - Selecciona qué día aplica
            - Ejemplo: "Miércoles"
            """)
        
        col4, col5 = st.columns(2)
        
        with col4:
            st.markdown("""
            **4️⃣ Hora de inicio**
            - Usa el slider para elegir la hora (0-23)
            - Ejemplo: 12 (mediodía)
            """)
        
        with col5:
            st.markdown("""
            **5️⃣ Hora de fin**
            - Usa el slider para elegir la hora final (0-23)
            - Ejemplo: 14 (2:00 PM)
            """)
    
    st.markdown("""
    **Ejemplo de configuración:**
    - 📍 **Ubicación**: Chicken Shop
    - 💰 **Descuento**: 20%
    - 📅 **Día**: Miércoles
    - ⏰ **Horario**: 12:00 - 14:00
    
    Esto significa: *"20% de descuento en Chicken Shop los miércoles de 12:00 a 14:00"*
    """)
    
    st.markdown("---")
    
    # Paso 3: Aplicar Campaña
    st.subheader("✅ Paso 3: Aplicar la Campaña")
    
    st.markdown("""
    **¿Qué debes hacer?**
    
    1. 👉 Completa todos los campos anteriores
    2. 👉 **Haz clic en el botón "💾 Aplicar Campaña"** (botón verde en el panel lateral)
    3. ✅ Verás un mensaje de éxito: *"✅ Campaña aplicada: 20% en Chicken Shop los Miércoles"*
    """)
    
    st.success("""
    ✅ **Campaña aplicada exitosamente**
    
    La campaña ya está activa en el sistema. Se aplicará automáticamente cuando:
    - El día de la semana coincida (ej: Miércoles)
    - La hora actual esté en el rango configurado (ej: entre 12:00 y 14:00)
    """)
    
    st.markdown("---")
    
    # Paso 4: Ejecutar Simulación
    st.subheader("▶️ Paso 4: Ejecutar la Simulación")
    
    st.markdown("""
    **¿Qué debes hacer?**
    
    En el panel lateral, dentro de la sección **"🎮 Control"**:
    
    1. 👉 **Haz clic en "⏩ Ejecutar Siguiente Hora"** para avanzar 1 hora
    2. 👉 O **"🔄 Avanzar 5 Horas"** para avanzar más rápido
    3. 👀 **Observa los cambios** en las pestañas principales
    
    **¿Qué esperar al ejecutar?**
    - El reloj avanzará (ej: de 7:00 AM → 8:00 AM)
    - Los agentes tomarán decisiones automáticamente usando IA
    - Verás eventos aparecer en la pestaña **"📝 Eventos"**
    """)
    
    st.markdown("---")
    
    # Paso 5: Qué Observar
    st.subheader("👀 Paso 5: ¿Qué Debes Esperar Cuando la Campaña Esté Activa?")
    
    st.markdown("""
    Cuando la simulación llegue al día y hora configurados de tu campaña, verás:
    """)
    
    # Ejemplo de escenario
    with st.expander("📊 Ejemplo: Campaña de 20% en Chicken Shop (Miércoles 12:00-14:00)", expanded=True):
        st.markdown("""
        **Escenario:**
        - ⏰ **Miércoles, 12:00 PM** (hora de inicio de la campaña)
        - 📍 Campaña activa: "Chicken Shop: 20% descuento"
        
        **Lo que verás en la pestaña "📝 Eventos":**
        ```
        ⏰ Miércoles, Día 2, 13:00 | 👤 María: María compró chicken en Chicken Shop por $9.60
        ⏰ Miércoles, Día 2, 13:00 | 👤 David: David compró chicken en Chicken Shop por $9.60
        ```
        
        **Nota importante:** 
        - Precio original: $12.00
        - Con 20% descuento: $9.60 ✅
        - Los agentes **ahorraron $2.40** gracias a la campaña
        
        **Lo que verás en la pestaña "📊 Análisis":**
        - 📈 **Gráfico de Ventas**: "Chicken Shop" tendrá un aumento de ventas durante las horas de la campaña
        - 📊 **Matriz de Lealtad**: Los agentes que compraron durante la campaña aparecerán con más visitas a "Chicken Shop"
        """)
    
    st.markdown("---")
    
    # Qué Observar en Cada Pestaña
    st.subheader("🔍 Paso 6: Qué Observar en Cada Pestaña")
    
    tab_info1, tab_info2, tab_info3, tab_info4 = st.tabs([
        "🗺️ Pestaña Mapa", 
        "📝 Pestaña Eventos", 
        "📊 Pestaña Análisis",
        "👥 Pestaña Agentes"
    ])
    
    with tab_info1:
        st.markdown("""
        **🗺️ Pestaña Mapa**
        
        - **Ubicaciones**: Verás cuadrados azules con nombres (ej: "Chicken Shop", "Coffee Shop")
        - **Agentes**: Verás círculos coloreados:
          - 🟢 Verde = Energía alta (>70)
          - 🟡 Amarillo = Energía media (30-70)
          - 🔴 Rojo = Energía baja (<30)
        
        **Durante una campaña activa:**
        - Verás agentes moviéndose hacia la ubicación con descuento
        - Múltiples agentes pueden estar en la misma ubicación simultáneamente
        """)
    
    with tab_info2:
        st.markdown("""
        **📝 Pestaña Eventos (Feed en Tiempo Real)**
        
        Aquí verás todos los eventos de la simulación en tiempo real:
        
        - **⏰ Acciones**: "María compró chicken en Chicken Shop por $9.60"
        - **💬 Conversaciones**: "María → David: [diálogo generado por IA]"
        - **ℹ️ Sistema**: "Inicio de nuevo día - Los agentes están planificando"
        
        **Durante una campaña activa, espera ver:**
        - Más eventos de compra en la ubicación con descuento
        - Precios con descuento aplicado (ej: $9.60 en lugar de $12.00)
        - Agentes moviéndose hacia esa ubicación
        """)
    
    with tab_info3:
        st.markdown("""
        **📊 Pestaña Análisis (Dashboard)**
        
        **1. Gráfico de Ventas:**
        - Muestra los ingresos totales por ubicación
        - Durante una campaña, verás un **aumento en las ventas** de la ubicación con descuento
        - Compara ventas antes/durante/después de la campaña
        
        **2. Matriz de Lealtad:**
        - Heatmap mostrando visitas por agente y ubicación
        - Los agentes que respondieron a la campaña mostrarán más visitas a esa ubicación
        - Colores más intensos = más visitas
        
        **3. Grafo Social:**
        - Muestra relaciones entre agentes (afinidad)
        - Si los agentes se encuentran durante la campaña, pueden conversar y mejorar sus relaciones
        """)
    
    with tab_info4:
        st.markdown("""
        **👥 Pestaña Agentes**
        
        Aquí puedes ver el estado detallado de cada agente:
        
        - **⚡ Energía**: Barra de progreso (0-100)
        - **💰 Dinero**: Saldo actual (disminuye con compras)
        - **🍔 Comestibles**: Nivel de comida en casa (0-100)
        - **📍 Ubicación**: Dónde está el agente ahora
        - **📝 Plan del Día**: Itinerario generado por IA
        
        **Durante una campaña activa:**
        - El dinero de los agentes disminuirá si compran
        - Verás compras en el inventario (ej: {"chicken": 1})
        - La energía puede aumentar si comen lo comprado
        """)
    
    st.markdown("---")
    
    # Consejos y Mejores Prácticas
    st.subheader("💡 Consejos y Mejores Prácticas")
    
    col_tip1, col_tip2 = st.columns(2)
    
    with col_tip1:
        st.info("""
        **🎯 Tips para Campañas Efectivas:**
        
        1. **Horarios estratégicos**: 
           - 12:00-14:00 (hora de almuerzo) es buen momento
           - 17:00-19:00 (hora de cena) también funciona
        
        2. **Porcentajes de descuento:**
           - 10-15%: Efectivo para agentes "thrifty"
           - 20-30%: Más atractivo para todos
           - >30%: Puede generar mucha demanda
        
        3. **Días de la semana:**
           - Miércoles (medio de semana): Bueno para experimentar
           - Viernes: Los agentes pueden tener más dinero
        """)
    
    with col_tip2:
        st.warning("""
        **⚠️ Cosas a Considerar:**
        
        1. **Los agentes tienen memoria**: 
           - Si una campaña es muy exitosa, los agentes pueden desarrollar hábitos
           - Verás más visitas repetidas después de campañas exitosas
        
        2. **Dinero limitado**: 
           - Si un agente no tiene suficiente dinero, no comprará aunque haya descuento
           - Revisa la pestaña "👥 Agentes" para ver el dinero disponible
        
        3. **Energía**: 
           - Si un agente está muy cansado (energía baja), puede priorizar descansar sobre comprar
        """)
    
    st.markdown("---")
    
    # Resumen de Flujo Completo
    st.subheader("📋 Resumen: Flujo Completo")
    
    st.markdown("""
    **Pasos completos para usar una campaña:**
    
    1. ✅ **Inicializar** → Haz clic en "🔄 Inicializar Simulación"
    2. ⚙️ **Configurar** → En el panel lateral, configura tu campaña:
       - Selecciona ubicación
       - Define descuento (%)
       - Elige día y horario
    3. 💾 **Aplicar** → Haz clic en "💾 Aplicar Campaña"
    4. ▶️ **Ejecutar** → Haz clic en "⏩ Ejecutar Siguiente Hora" repetidamente
    5. 👀 **Observar** → Ve a las pestañas "📝 Eventos" y "📊 Análisis" para ver resultados
    6. 📈 **Analizar** → Compara ventas antes/durante/después de la campaña
    
    **Ejemplo de cronograma:**
    ```
    Día 0, 07:00 → Inicializas simulación
    Día 0, 08:00 → Configuras campaña (20% en Chicken Shop, Miércoles 12:00-14:00)
    Día 0, 09:00 → Aplicas campaña
    Día 0-2, varias horas → Ejecutas simulación (avanzas el tiempo)
    Día 2, 12:00 → ¡Campaña activa! Los agentes comienzan a comprar con descuento
    Día 2, 13:00 → Más compras con descuento
    Día 2, 14:00 → Campaña termina, pero los efectos continúan
    ```
    """)
    
    st.markdown("---")
    
    # Preguntas Frecuentes
    st.subheader("❓ Preguntas Frecuentes")
    
    faq_expander = st.expander("Ver preguntas frecuentes", expanded=False)
    
    with faq_expander:
        st.markdown("""
        **Q: ¿Por qué no veo que los agentes compren durante la campaña?**
        
        A: Verifica que:
        - El día de la semana coincida (ej: si configuraste Miércoles, debe ser miércoles en la simulación)
        - La hora esté en el rango configurado (ej: entre 12:00 y 14:00)
        - Los agentes tengan suficiente dinero
        - Los agentes tengan hambre o necesiten comprar
        
        ---
        
        **Q: ¿Puedo tener múltiples campañas activas al mismo tiempo?**
        
        A: Actualmente el sistema soporta una campaña a la vez. Si aplicas una nueva campaña, reemplazará la anterior.
        
        ---
        
        **Q: ¿Cómo sé si la campaña está activa ahora?**
        
        A: En la parte superior verás la hora actual. Compara:
        - Día actual vs día configurado en la campaña
        - Hora actual vs rango horario de la campaña
        
        ---
        
        **Q: ¿Por qué los precios no tienen descuento?**
        
        A: Asegúrate de que:
        - La campaña esté aplicada (verás mensaje de éxito)
        - El día y hora coincidan con la configuración
        - Estés viendo eventos de la ubicación correcta
        
        ---
        
        **Q: ¿Los agentes recuerdan las campañas pasadas?**
        
        A: Sí, los agentes tienen memoria. Si una campaña fue exitosa, pueden desarrollar preferencias por esa ubicación y visitarla más frecuentemente incluso después de la campaña.
        """)
    
    st.markdown("---")
    
    # CTA Final
    st.success("""
    🎉 **¡Listo para comenzar!**
    
    Ahora que entiendes cómo funciona el sistema, puedes:
    
    1. Volver a la pestaña **"🗺️ Mapa"** para comenzar
    2. Usar el panel lateral para configurar tu primera campaña
    3. Observar cómo los agentes responden a tus campañas de marketing
    
    **¡Experimenta con diferentes descuentos, horarios y ubicaciones para ver qué funciona mejor!**
    """)


# ============ INTERFAZ STREAMLIT ============

# Título principal moderno
st.markdown(f"""
<div style="padding: 1rem 0;">
    <h1 style="font-size: 2.5rem; font-weight: 700; color: #1f77b4; margin-bottom: 0.2rem;">
        {t("title")}
    </h1>
    <p style="font-size: 1.1rem; color: #666; margin-top: 0;">
        {t("subtitle")}
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar - Command Center & Global KPIs
with st.sidebar:
    # Selector de idioma AL INICIO del sidebar
    lang_options = {"🇪🇸 Español": "es", "🇬🇧 English": "en"}
    selected_lang_display = st.selectbox(
        t("language"),
        options=list(lang_options.keys()),
        index=0 if st.session_state.language == "es" else 1,
        key="lang_selector"
    )
    new_lang = lang_options[selected_lang_display]
    if new_lang != st.session_state.language:
        st.session_state.language = new_lang
        st.rerun()
    
    st.markdown("---")
    st.markdown(f"### {t('command_center')}")
    
    # Estado de conexión API
    current_api_key = get_api_key()
    api_connected = current_api_key and st.session_state.llm_client
    status_color = "#d4edda" if api_connected else "#f8d7da"
    status_dot_color = "#28a745" if api_connected else "#dc3545"
    status_text = t("api_connected") if api_connected else t("api_not_connected")
    
    st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 0.5rem; padding: 0.5rem; background-color: {status_color}; border-radius: 0.5rem; margin-bottom: 1rem;">
        <div style="width: 10px; height: 10px; background-color: {status_dot_color}; border-radius: 50%;"></div>
        <span>{status_text}</span>
    </div>
    """, unsafe_allow_html=True)
    
    # API Key Configuration Section
    st.markdown("---")
    st.markdown(f"### 🔑 {t('api_config')}")
    
    # User API Key Input
    user_api_key = st.text_input(
        t("api_key_input"),
        value=st.session_state.user_api_key if st.session_state.user_api_key else "",
        type="password",
        placeholder=t("api_key_placeholder"),
        help="Your API key is stored only in this browser session and will be cleared when you refresh the page."
    )
    
    col_save, col_clear = st.columns(2)
    with col_save:
        if st.button(t("api_key_save"), use_container_width=True):
            if user_api_key and user_api_key.strip():
                st.session_state.user_api_key = user_api_key.strip()
                st.session_state.api_key_source = "user"
                st.success(t("api_key_saved"))
                st.rerun()
    
    with col_clear:
        if st.button(t("api_key_clear"), use_container_width=True):
            st.session_state.user_api_key = None
            st.session_state.api_key_source = "env"
            st.info(t("api_key_cleared"))
            st.rerun()
    
    # Option to use .env file (only if it exists)
    env_api_key = os.getenv("DEEPSEEK_API_KEY")
    if env_api_key:
        use_env = st.checkbox(
            t("use_env_key"),
            value=st.session_state.api_key_source == "env" and not st.session_state.user_api_key,
            help="Use the API key from your .env file instead of the one entered above."
        )
        if use_env and not st.session_state.user_api_key:
            st.session_state.api_key_source = "env"
        elif not use_env and st.session_state.user_api_key:
            st.session_state.api_key_source = "user"
    
    # Fecha y Hora
    if st.session_state.world_config:
        world_config = st.session_state.world_config
        day_names = [t("monday"), t("tuesday"), t("wednesday"), t("thursday"), 
                    t("friday"), t("saturday"), t("sunday")]
        day_name = day_names[world_config.get_day_of_week()]
        st.markdown(f"""
        <div style="padding: 0.5rem; background-color: #f0f2f6; border-radius: 0.5rem; margin-bottom: 1rem;">
            <strong>{t('day')}:</strong> {day_name} | <strong>{t('hour')}:</strong> {world_config.current_hour:02d}:{world_config.current_minute:02d}
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Inicialización
    st.markdown(f"#### {t('setup')}")
    
    # Inicialización
    if st.button(t("initialize_simulation"), use_container_width=True):
        initialize_simulation()
        st.rerun()
    
    # Cargar configuración
    st.subheader(f"{t('load_config')}")
    uploaded_file = st.file_uploader(t("upload_json"), type=["json"])
    if uploaded_file is not None:
        if load_config_from_json(uploaded_file):
            # Reinicializar motores después de cargar
            world_config = st.session_state.world_config
            locations = st.session_state.locations
            
            st.session_state.time_manager = TimeManager(world_config)
            st.session_state.interaction_engine = InteractionEngine(world_config)
            st.session_state.transaction_system = TransactionSystem(world_config)
            
            api_key = get_api_key()
            if api_key:
                llm_client = LLMClient(api_key=api_key)
                st.session_state.llm_client = llm_client
                st.session_state.decision_maker = DecisionMaker(world_config, locations, llm_client)
                st.session_state.response_parser = ResponseParser(
                    world_config, locations,
                    st.session_state.interaction_engine,
                    st.session_state.transaction_system
                )
            st.rerun()
    
    # Active Campaigns
    st.markdown("---")
    st.markdown(f"### {t('active_campaigns')}")
    
    if st.session_state.world_config and st.session_state.world_config.marketing_campaigns:
        campaign = st.session_state.world_config.marketing_campaigns[0]
        current_day_of_week = st.session_state.world_config.get_day_of_week()
        current_hour = st.session_state.world_config.current_hour
        
        is_active_day = (campaign.get("day_of_week") == current_day_of_week)
        is_active_hour = (campaign.get("start_hour", 0) <= current_hour < campaign.get("end_hour", 24))
        is_active = is_active_day and is_active_hour
        
        day_names = get_day_names()
        campaign_day_name = day_names[campaign.get("day_of_week", 0)]
        
        status_color = "🟢" if is_active else "🔴"
        status_text = t("active") if is_active else t("inactive")
        
        st.markdown(f"{status_color} **{status_text}**")
        st.markdown(f"**{campaign.get('location_name', '')}** | {campaign.get('discount_percent', 0)}%")
        st.caption(f"{campaign_day_name} {campaign.get('start_hour', 0):02d}:00 - {campaign.get('end_hour', 24):02d}:00")
    else:
        st.info(t("no_active_campaigns"))
    
    # Campaign Manager
    st.markdown("---")
    st.markdown(f"### {t('campaign_manager')}")
    
    if st.session_state.world_config:
        st.markdown(f"#### {t('create_campaign')}")
        discount_location = st.selectbox(
            t("target_location"),
            options=list(st.session_state.locations.keys()),
            index=0 if st.session_state.locations else None
        )
        discount_percent = st.slider(t("discount_strategy"), 0, 50, 20)
        discount_day = st.selectbox(
            t("day_of_week"),
            options=get_day_names(),
            index=2
        )
        discount_start = st.slider(t("start_time"), 0, 23, 12)
        discount_end = st.slider(t("end_time"), 0, 23, 14)
        st.markdown(f"**{t('time_window')}:** {discount_day} {discount_start:02d}:00 - {discount_end:02d}:00")
        
        if st.button(t("deploy_campaign"), use_container_width=True, type="primary"):
            day_names_list = get_day_names()
            campaign_day = day_names_list.index(discount_day) if discount_day in day_names_list else 2
            
            st.session_state.world_config.marketing_campaigns = [{
                "location_name": discount_location,
                "discount_percent": discount_percent,
                "day_of_week": campaign_day,
                "start_hour": discount_start,
                "end_hour": discount_end
            }]
            
            # Calcular cuántos días faltan para llegar al día de la campaña
            current_day_of_week = st.session_state.world_config.get_day_of_week()
            days_until_campaign = (campaign_day - current_day_of_week) % 7
            if days_until_campaign == 0:
                # Ya estamos en el día correcto, verificar si la hora es correcta
                current_hour = st.session_state.world_config.current_hour
                if discount_start <= current_hour < discount_end:
                    st.success(f"✅ Campaña aplicada y ACTIVA AHORA: {discount_percent}% en {discount_location} (Horario: {discount_start:02d}:00-{discount_end:02d}:00)")
                else:
                    st.success(f"✅ Campaña aplicada: {discount_percent}% en {discount_location} los {discount_day}s (Horario: {discount_start:02d}:00-{discount_end:02d}:00)\n⚠️ Espera hasta las {discount_start:02d}:00 para que se active")
            else:
                st.success(f"✅ Campaña aplicada: {discount_percent}% en {discount_location} los {discount_day}s (Horario: {discount_start:02d}:00-{discount_end:02d}:00)\n⏰ Faltan {days_until_campaign} día(s) para que se active. Usa 'Avanzar 5 Horas' repetidamente o 'Avanzar Hasta Día' para llegar más rápido.")
        
        # Mostrar estado actual de la campaña
        if st.session_state.world_config and st.session_state.world_config.marketing_campaigns:
            campaign = st.session_state.world_config.marketing_campaigns[0]
            current_day_of_week = st.session_state.world_config.get_day_of_week()
            current_hour = st.session_state.world_config.current_hour
            current_day = st.session_state.world_config.current_day
            
            is_active_day = (campaign.get("day_of_week") == current_day_of_week)
            is_active_hour = (campaign.get("start_hour", 0) <= current_hour < campaign.get("end_hour", 24))
            is_active = is_active_day and is_active_hour
            
            day_names = get_day_names()
            campaign_day_name = day_names[campaign.get("day_of_week", 0)]
            
            st.markdown("---")
            st.subheader(t("campaign_status"))
            
            if is_active:
                st.success(f"{t('campaign_active')}\n\n📍 {campaign.get('location_name')}: {campaign.get('discount_percent')}% {t('discount')}\n⏰ {t('hour')}: {campaign.get('start_hour', 0):02d}:00 - {campaign.get('end_hour', 24):02d}:00")
            else:
                st.info(f"{t('campaign_inactive')}\n\n📍 {campaign.get('location_name')}: {campaign.get('discount_percent')}% {t('discount')}\n📅 {t('day')}: {campaign_day_name}\n⏰ {t('hour')}: {campaign.get('start_hour', 0):02d}:00 - {campaign.get('end_hour', 24):02d}:00")
    
    # Simulation Controls
    st.markdown("---")
    st.markdown(f"### {t('simulation_controls')}")
    
    if st.session_state.world_config:
        col_play, col_pause = st.columns(2)
        with col_play:
            if st.button(t("play"), use_container_width=True):
                st.session_state.simulation_running = True
                st.rerun()
        with col_pause:
            if st.button(t("pause"), use_container_width=True):
                st.session_state.simulation_running = False
        
        if st.button(t("next_hour"), use_container_width=True):
            execute_tick()
            st.rerun()
        
        # Botón para avanzar hasta el día de la campaña configurada
        if st.session_state.world_config.marketing_campaigns:
            campaign = st.session_state.world_config.marketing_campaigns[0]
            campaign_day = campaign.get("day_of_week", 0)
            current_day_of_week = st.session_state.world_config.get_day_of_week()
            current_day = st.session_state.world_config.current_day
            
            # Calcular cuántos días faltan para llegar al día de la campaña
            days_needed = (campaign_day - current_day_of_week) % 7
            day_names = get_day_names()
            campaign_day_name = day_names[campaign_day]
            location_name = campaign.get("location_name", "ubicación")
            
            # Solo mostrar el botón si no estamos en el día de la campaña o si estamos en el día pero fuera del horario
            is_campaign_day = (campaign_day == current_day_of_week)
            current_hour = st.session_state.world_config.current_hour
            start_hour = campaign.get("start_hour", 0)
            is_in_time_range = (start_hour <= current_hour < campaign.get("end_hour", 24))
            
            if not is_campaign_day or (is_campaign_day and not is_in_time_range):
                hours_to_advance = days_needed * 24
                # Si estamos en el día correcto pero fuera del horario, ajustar horas
                if is_campaign_day and current_hour < start_hour:
                    hours_to_advance = start_hour - current_hour
                elif is_campaign_day and current_hour >= campaign.get("end_hour", 24):
                    # Si ya pasó el horario hoy, avanzar al próximo día de campaña
                    hours_to_advance = 7 * 24 - (24 - current_hour) + start_hour
                    campaign_day_name = day_names[campaign_day]  # Mismo día la próxima semana
                
                button_text = f"{t('skip_to_campaign')} {campaign_day_name} {start_hour:02d}:00"
                if st.button(button_text, use_container_width=True):
                    # Usar barra de progreso para mostrar avance
                    progress_bar = st.progress(0)
                    total_hours = hours_to_advance
                    for i in range(hours_to_advance):
                        execute_tick()
                        # Actualizar progreso cada 5 horas para no sobrecargar
                        if (i + 1) % 5 == 0 or i == hours_to_advance - 1:
                            progress_bar.progress((i + 1) / total_hours)
                    st.rerun()
        
        if st.button(t("clear_log"), use_container_width=True):
            st.session_state.event_log = []
            st.rerun()

# Panel Principal - Global KPIs
if st.session_state.world_config:
    world_config = st.session_state.world_config
    time_manager = st.session_state.time_manager
    
    # Métricas Rápidas (KPIs Globales)
    st.markdown("### 📊 Métricas Rápidas (KPIs Globales)")
    col1, col2, col3 = st.columns(3)
    with col1:
        active_agents = len([a for a in st.session_state.agents if not a.is_collapsed()])
        total_agents = len(st.session_state.agents)
        st.metric("Active Agents", f"{active_agents}/{total_agents}", delta=None)
    with col2:
        total_spending = sum(loc.total_sales for loc in st.session_state.locations.values())
        st.metric("Total Spending Today", f"${total_spending:.2f}", delta=None)
    with col3:
        active_campaigns = len(world_config.marketing_campaigns) if world_config.marketing_campaigns else 0
        campaign_text = ""
        if world_config.marketing_campaigns:
            campaign = world_config.marketing_campaigns[0]
            campaign_text = f" ({campaign.get('location_name', '')})"
        st.metric("Active Campaigns", f"{active_campaigns}{campaign_text}", delta=None)
    
    st.markdown("---")
    
    # Tabs principales
    tab1, tab2, tab3, tab4 = st.tabs([
        "🗺️ Live Monitor", 
        "📊 Campaign Manager", 
        "📈 Market Intelligence",
        "👥 Agent Telemetry"
    ])
    
    with tab1:
        col_left, col_right = st.columns([2, 1])
        
        with col_left:
            st.markdown("### Urban Heatmap")
            fig_map = create_map_visualization()
            if fig_map:
                # Mejorar visualización del mapa
                fig_map.update_layout(
                    plot_bgcolor='#0e1117',
                    paper_bgcolor='#0e1117',
                    font=dict(color='white'),
                    height=700
                )
                st.plotly_chart(fig_map, use_container_width=True)
            else:
                st.info("Inicializa la simulación para ver el mapa")
        
        with col_right:
            st.markdown("### Agent Telemetry (Feed de Eventos)")
            
            # Mostrar alertas primero
            agents = st.session_state.agents
            for agent in agents:
                if agent.energy < 20:
                    st.error(f"⚠️ **Alerta!** Inventario de energía crítico para Agent {agent.name}")
            
            st.markdown("---")
            
            # Mostrar últimos eventos
            if st.session_state.event_log:
                for event in reversed(st.session_state.event_log[-15:]):
                    event_type = event.get("type", "info")
                    if event_type == "action":
                        # Extraer información de compra
                        message = event.get('message', '')
                        if 'compró' in message or 'bought' in message:
                            st.markdown(f"🛒 **{event['agent']}**: {message}")
                        else:
                            st.markdown(f"👤 **{event['agent']}**: {message}")
                    elif event_type == "chat":
                        st.markdown(f"💬 **{event['agent']}** está hablando con **{event['other_agent']}** en la {event.get('location', 'Plaza')}")
                        st.caption(f"'{event['message']}'")
                    elif event_type == "system":
                        if "Campaña ACTIVA" in event['message']:
                            st.success(f"🎯 {event['message']}")
                        else:
                            st.info(f"ℹ️ {event['message']}")
            else:
                st.info("No hay eventos registrados aún")
    
    with tab2:
        st.markdown("### Campaign Manager")
        
        if world_config.marketing_campaigns:
            st.markdown("#### Campañas Activas")
            for idx, campaign in enumerate(world_config.marketing_campaigns, 1):
                is_active_day = (campaign.get("day_of_week") == world_config.get_day_of_week())
                is_active_hour = (campaign.get("start_hour", 0) <= world_config.current_hour < campaign.get("end_hour", 24))
                is_active = is_active_day and is_active_hour
                
                day_names = get_day_names()
                campaign_day_name = day_names[campaign.get("day_of_week", 0)]
                
                status_color = "🟢" if is_active else "🔴"
                status_text = t("active") if is_active else t("inactive")
                
                col_status, col_info, col_action = st.columns([1, 3, 1])
                with col_status:
                    st.markdown(f"### {status_color}")
                    st.caption(status_text)
                with col_info:
                    st.markdown(f"**{idx}. {campaign.get('location_name', '')}** | {campaign.get('discount_percent', 0)}% {t('discount')}")
                    st.caption(f"{t('day')}: {campaign_day_name} ({campaign.get('start_hour', 0):02d}:00 - {campaign.get('end_hour', 24):02d}:00)")
                with col_action:
                    if st.button(t("cancel"), key=f"cancel_{idx}"):
                        world_config.marketing_campaigns = []
                        st.rerun()
                st.markdown("---")
        else:
            st.info("No hay campañas activas. Configura una nueva campaña en el sidebar.")
    
    with tab3:
        st.markdown("### Market Intelligence")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Impacto en Ventas (Sales Impact)")
            fig_sales = create_sales_chart()
            if fig_sales:
                st.plotly_chart(fig_sales, use_container_width=True)
            else:
                st.info("No hay datos de ventas aún")
        
        with col2:
            st.markdown("#### Matriz de Lealtad (Loyalty Matrix)")
            fig_loyalty = create_loyalty_matrix()
            if fig_loyalty:
                st.plotly_chart(fig_loyalty, use_container_width=True)
            else:
                st.info("No hay datos de lealtad aún")
        
        st.markdown("#### Grafo Social (Social Graph)")
        fig_social = create_social_graph()
        if fig_social:
            st.plotly_chart(fig_social, use_container_width=True)
        else:
            st.info("No hay relaciones sociales registradas aún")
    
    with tab4:
        st.markdown("### Agent Telemetry")
        
        agents = st.session_state.agents
        if agents:
            for agent in agents:
                # Detectar alertas
                alert_class = ""
                if agent.energy < 20:
                    alert_class = "⚠️ **Alerta!** Inventario de energía crítico para Agent "
                
                with st.expander(f"👤 Agent {agent.name} ({agent.age} años, {agent.profession})"):
                    if agent.energy < 20:
                        st.error(alert_class + agent.name)
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Wallet", f"${agent.money:.2f}")
                        energy_color = "🟢" if agent.energy > 70 else "🟡" if agent.energy > 30 else "🔴"
                        st.metric("Energy", f"{agent.energy:.1f}/100", delta=None, delta_color="off")
                        st.progress(agent.energy / 100.0)
                    
                    with col2:
                        st.metric("Grocery Level", f"{agent.grocery_level:.1f}/100")
                        st.metric("Location", agent.current_location)
                    
                    with col3:
                        st.metric("Coordinates", f"{agent.coordinates}")
                        if agent.inventory:
                            st.write(f"**Inventory**: {dict(agent.inventory)}")
                        else:
                            st.write("**Inventory**: Vacío")
                    
                    # Reasoning
                    st.markdown("---")
                    st.markdown("#### 🧠 Reasoning")
                    if hasattr(agent, 'last_action') and agent.last_action:
                        last_events = agent.memory.get_recent_events(5)
                        if last_events:
                            last_event = last_events[-1]
                            if last_event.event_type == "Purchase":
                                st.write(f"**Reasoning:** Tengo hambre y vi el descuento, cambio de ruta.")
                            elif last_event.event_type == "Move":
                                st.write(f"**Reasoning:** Necesito ir a {last_event.location}.")
                            else:
                                st.write(f"**Reasoning:** {last_event.description}")
                        else:
                            st.write(f"**Reasoning:** Esperando próximas decisiones...")
                    else:
                        st.write(f"**Reasoning:** Esperando próximas decisiones...")
                    
                    st.write(f"**Personality**: {', '.join(agent.personality_traits)}")
        else:
            st.info("No hay agentes configurados")
    
else:
    st.info("👈 Usa el panel lateral para inicializar la simulación")
    st.markdown("""
    ### Bienvenido al Sistema de Simulación Multi-Agente
    
    Este sistema simula el comportamiento de consumidores usando IA.
    
    **Características:**
    - 🤖 Agentes con personalidad y necesidades dinámicas
    - 🗺️ Mundo con ubicaciones y productos
    - 💰 Sistema económico con campañas de marketing
    - 🧠 Toma de decisiones mediante LLM (DeepSeek)
    - 📊 Visualización en tiempo real
    
    **Pasos para comenzar:**
    1. Configura tu API key de DeepSeek en la variable de entorno `DEEPSEEK_API_KEY`
    2. Haz clic en "Inicializar Simulación" en el panel lateral
    3. Usa "Ejecutar Siguiente Hora" para avanzar la simulación
    4. Observa el comportamiento de los agentes en tiempo real
    """)


