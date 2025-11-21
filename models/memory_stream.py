"""
Sistema de Memoria para Agentes
Almacena eventos y reflexiones para formar hábitos
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from datetime import datetime


@dataclass
class MemoryEvent:
    """Representa un evento en la memoria"""
    timestamp: Tuple[int, int, int]  # (day, hour, minute)
    event_type: str  # "Purchase", "Chat", "Move", "Eat", "Work", etc.
    description: str
    location: Optional[str] = None
    other_agent_id: Optional[str] = None
    metadata: Dict = field(default_factory=dict)


@dataclass
class Reflection:
    """Representa una reflexión del agente sobre su comportamiento"""
    timestamp: Tuple[int, int, int]
    summary: str
    insights: List[str]
    habits_identified: List[str]


class MemoryStream:
    """Stream de memoria que almacena eventos y reflexiones"""
    
    def __init__(self, max_events: int = 100):
        self.events: List[MemoryEvent] = []
        self.reflections: List[Reflection] = []
        self.max_events = max_events
    
    def add_event(self, timestamp: Tuple[int, int, int], event_type: str, 
                  description: str, location: Optional[str] = None,
                  other_agent_id: Optional[str] = None, metadata: Dict = None):
        """Añade un evento a la memoria"""
        event = MemoryEvent(
            timestamp=timestamp,
            event_type=event_type,
            description=description,
            location=location,
            other_agent_id=other_agent_id,
            metadata=metadata or {}
        )
        self.events.append(event)
        
        # Mantener solo los últimos max_events
        if len(self.events) > self.max_events:
            self.events = self.events[-self.max_events:]
    
    def add_reflection(self, timestamp: Tuple[int, int, int], summary: str,
                      insights: List[str], habits_identified: List[str]):
        """Añade una reflexión a la memoria"""
        reflection = Reflection(
            timestamp=timestamp,
            summary=summary,
            insights=insights,
            habits_identified=habits_identified
        )
        self.reflections.append(reflection)
    
    def get_recent_events(self, hours: int = 24) -> List[MemoryEvent]:
        """Retorna eventos recientes dentro de las últimas N horas"""
        # Simplificado: retorna los últimos N eventos
        return self.events[-hours:] if hours < len(self.events) else self.events
    
    def get_events_by_type(self, event_type: str, limit: int = 10) -> List[MemoryEvent]:
        """Retorna eventos de un tipo específico"""
        filtered = [e for e in self.events if e.event_type == event_type]
        return filtered[-limit:]
    
    def get_events_at_location(self, location: str, limit: int = 10) -> List[MemoryEvent]:
        """Retorna eventos en una ubicación específica"""
        filtered = [e for e in self.events if e.location == location]
        return filtered[-limit:]
    
    def get_purchase_history(self, limit: int = 20) -> List[MemoryEvent]:
        """Retorna el historial de compras"""
        return self.get_events_by_type("Purchase", limit)
    
    def get_conversation_history(self, other_agent_id: Optional[str] = None, 
                                limit: int = 10) -> List[MemoryEvent]:
        """Retorna el historial de conversaciones"""
        if other_agent_id:
            filtered = [e for e in self.events 
                       if e.event_type == "Chat" and e.other_agent_id == other_agent_id]
        else:
            filtered = self.get_events_by_type("Chat", limit)
        return filtered[-limit:]
    
    def get_memory_context(self, window_hours: int = 48) -> str:
        """Genera un contexto de memoria para prompts del LLM"""
        recent_events = self.get_recent_events(window_hours)
        
        context = "Memoria Reciente:\n"
        for event in recent_events[-10:]:  # Últimos 10 eventos
            day, hour, minute = event.timestamp
            context += f"- Día {day}, {hour:02d}:{minute:02d} - {event.event_type}: {event.description}\n"
        
        if self.reflections:
            latest_reflection = self.reflections[-1]
            context += f"\nÚltima Reflexión:\n{latest_reflection.summary}\n"
            if latest_reflection.habits_identified:
                context += f"Hábitos Identificados: {', '.join(latest_reflection.habits_identified)}\n"
        
        return context



