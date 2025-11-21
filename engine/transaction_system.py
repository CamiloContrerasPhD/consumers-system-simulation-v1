"""
Sistema de Transacciones
Gestiona la economía y las compras
"""

from typing import Optional, Tuple
from models.agent import Agent
from models.location import Location
from models.world_config import WorldConfig


class TransactionSystem:
    """Gestiona transacciones económicas y compras"""
    
    def __init__(self, world_config: WorldConfig):
        self.world_config = world_config
    
    def calculate_price(self, location: Location, product_name: str,
                       quantity: int = 1) -> Optional[float]:
        """
        Calcula el precio final de un producto aplicando descuentos.
        Retorna el precio final o None si el producto no existe.
        """
        base_price = location.get_base_price(product_name)
        if base_price is None:
            return None
        
        # Obtener descuento activo de marketing
        discount = self.world_config.get_discount(location.name)
        
        # Aplicar fórmula: FinalPrice = P_base * (1 - Descuento)
        final_price = base_price * quantity * (1 - discount)
        
        return final_price
    
    def validate_purchase(self, agent: Agent, location: Location,
                         product_name: str, quantity: int = 1) -> Tuple[bool, str, Optional[float]]:
        """
        Valida si un agente puede realizar una compra.
        Retorna (es_válido, mensaje_error, precio_final)
        """
        # Verificar si la ubicación tiene el producto
        if not location.has_product(product_name):
            return False, f"{location.name} no tiene stock de {product_name}", None
        
        # Calcular precio
        final_price = self.calculate_price(location, product_name, quantity)
        if final_price is None:
            return False, f"Producto {product_name} no disponible en {location.name}", None
        
        # Verificar si el agente tiene suficiente dinero
        if agent.money < final_price:
            return False, f"{agent.name} no tiene suficiente dinero (tiene ${agent.money:.2f}, necesita ${final_price:.2f})", final_price
        
        return True, "", final_price
    
    def execute_purchase(self, agent: Agent, location: Location,
                        product_name: str, quantity: int = 1) -> Tuple[bool, str, float]:
        """
        Ejecuta una compra si es válida.
        Retorna (éxito, mensaje, precio_pagado)
        """
        is_valid, error_msg, final_price = self.validate_purchase(
            agent, location, product_name, quantity
        )
        
        if not is_valid:
            return False, error_msg, 0.0
        
        # Ejecutar la transacción
        transaction_price = location.purchase(product_name, quantity)
        
        if transaction_price is None:
            return False, "Error al procesar la compra (sin stock)", 0.0
        
        # Actualizar estado del agente
        agent.spend_money(final_price)
        agent.add_item(product_name, quantity)
        
        # Obtener necesidad que satisface
        satisfies_need = location.inventory.get(product_name, {}).get("satisfies_need", "energy")
        if satisfies_need == "energy":
            agent.consume_energy("eat")  # Recupera energía al comer
        
        return True, f"{agent.name} compró {quantity}x {product_name} en {location.name} por ${final_price:.2f}", final_price





