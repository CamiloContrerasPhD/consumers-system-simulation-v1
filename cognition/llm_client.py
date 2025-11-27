"""
Cliente LLM para DeepSeek API
Gestiona las comunicaciones con la API de DeepSeek
"""

import os
import requests
import json
from typing import Optional


class LLMClient:
    """Cliente para comunicarse con la API de DeepSeek"""
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """
        Inicializa el cliente LLM.
        
        Args:
            api_key: API key de DeepSeek. Si no se proporciona, se lee de DEEPSEEK_API_KEY env var.
            base_url: URL base de la API. Por defecto usa la API de DeepSeek.
        """
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        self.base_url = base_url or "https://api.deepseek.com/v1/chat/completions"
        
        if not self.api_key:
            raise ValueError(
                "API key no proporcionada. "
                "Establece DEEPSEEK_API_KEY como variable de entorno o pásala al constructor."
            )
        
        self.model = "deepseek-chat"  # Modelo por defecto de DeepSeek
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
    
    def call(self, prompt: str, temperature: float = 0.7, max_tokens: int = 1000) -> str:
        """
        Realiza una llamada a la API de DeepSeek.
        
        Args:
            prompt: El prompt a enviar al LLM
            temperature: Temperatura para la generación (0.0-1.0)
            max_tokens: Número máximo de tokens a generar
        
        Returns:
            La respuesta del LLM como string
        """
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "Eres un asistente útil que siempre responde con JSON válido cuando se solicita."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
            "response_format": {"type": "json_object"}  # Fuerza respuesta JSON
        }
        
        try:
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            response.raise_for_status()
            result = response.json()
            
            # Extraer el contenido de la respuesta
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
            else:
                raise ValueError("Respuesta inválida de la API")
        
        except requests.exceptions.RequestException as e:
            print(f"Error en la llamada a la API: {e}")
            # Retornar respuesta por defecto en caso de error
            return json.dumps({
                "action": "rest",
                "reasoning": f"Error de conexión: {str(e)}"
            })
    
    def set_model(self, model: str):
        """Cambia el modelo a usar"""
        self.model = model






