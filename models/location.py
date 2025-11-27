"""
Módulo de Ubicaciones
Define las ubicaciones en el mundo (tiendas, trabajo, residencias)
"""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional


@dataclass
class Location:
    """Representa una ubicación en el mundo"""
    
    name: str
    coordinates: Tuple[int, int]  # (x, y)
    location_type: str  # "Residence", "Work", "Restaurant", "Shop", "Grocery"
    capacity: int = 10  # Cuántos agentes caben simultáneamente
    
    # Inventario y Precios
    inventory: Dict[str, Dict] = field(default_factory=dict)
    # Formato: {"product_name": {"price": 10.0, "stock": 100, "satisfies_need": "energy"}}
    
    # Estadísticas
    total_sales: float = 0.0
    visit_count: int = 0
    agents_present: List[str] = field(default_factory=list)  # IDs de agentes actualmente aquí
    
    def add_product(self, product_name: str, price: float, stock: int = 100, satisfies_need: str = "energy"):
        """Añade un producto al inventario de la ubicación"""
        self.inventory[product_name] = {
            "price": price,
            "stock": stock,
            "satisfies_need": satisfies_need
        }
    
    def get_base_price(self, product_name: str) -> Optional[float]:
        """Retorna el precio base de un producto"""
        if product_name in self.inventory:
            return self.inventory[product_name]["price"]
        return None
    
    def can_enter(self) -> bool:
        """Verifica si la ubicación tiene capacidad disponible"""
        return len(self.agents_present) < self.capacity
    
    def enter(self, agent_id: str) -> bool:
        """Intenta que un agente entre a la ubicación"""
        if self.can_enter() and agent_id not in self.agents_present:
            self.agents_present.append(agent_id)
            self.visit_count += 1
            return True
        return False
    
    def leave(self, agent_id: str):
        """Remueve un agente de la ubicación"""
        if agent_id in self.agents_present:
            self.agents_present.remove(agent_id)
    
    def has_product(self, product_name: str) -> bool:
        """Verifica si la ubicación tiene stock del producto"""
        if product_name in self.inventory:
            return self.inventory[product_name]["stock"] > 0
        return False
    
    def purchase(self, product_name: str, quantity: int = 1) -> Optional[float]:
        """Procesa una compra y retorna el precio total, o None si no hay stock"""
        if product_name in self.inventory and self.inventory[product_name]["stock"] >= quantity:
            price = self.inventory[product_name]["price"] * quantity
            self.inventory[product_name]["stock"] -= quantity
            self.total_sales += price
            return price
        return None
    
    def get_coordinates(self) -> Tuple[int, int]:
        """Retorna las coordenadas de la ubicación"""
        return self.coordinates






