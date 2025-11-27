"""
Página de Tutorial
Guía completa sobre cómo usar la aplicación y configurar campañas de marketing
"""

import streamlit as st

st.set_page_config(
    page_title="Tutorial - Sistema Multi-Agente",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Tutorial: Cómo Aplicar y Usar Campañas de Marketing")
st.markdown("---")

# Introducción
st.markdown("""
### 🎯 ¿Qué hace este sistema?

Este sistema simula el comportamiento de **consumidores inteligentes** (agentes con IA) 
que toman decisiones de compra basadas en:
- 💰 Su dinero disponible
- ⚡ Su nivel de energía
- 🍔 Su necesidad de comida
- 🎯 Campañas de marketing activas
- 📝 Su memoria y hábitos previos

Las **campañas de marketing** crean descuentos temporales que influyen en las decisiones 
de los agentes para comprar en ciertas ubicaciones.
""")

st.markdown("---")

# Paso 1: Inicialización
st.subheader("📍 Paso 1: Inicializar la Simulación")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    **¿Qué debes hacer?**
    
    1. 👉 **Ve a la página principal** (usa el menú lateral)
    2. 👉 **Busca el panel lateral izquierdo** (Command Center)
    3. 👉 **Haz clic en el botón "🔄 Inicializar Simulación"**
    4. ✅ Verás un mensaje confirmando que la simulación se inicializó
    
    **¿Qué esperar?**
    - Se crearán **3 agentes** (María, David, Lisa) con diferentes personalidades
    - Se crearán **5 ubicaciones** (Casa, Coffee Shop, Grocery Store, Chicken Shop, Oficina)
    - El reloj comenzará en **Día 0, 7:00 AM**
    - Todos los agentes empezarán en casa
    """)

with col2:
    st.info("""
    💡 **Tip:**
    
    Si no ves los botones, asegúrate de que la barra lateral esté visible.
    """)

st.markdown("---")

# Paso 2: Configurar Campaña
st.subheader("🎯 Paso 2: Configurar una Campaña de Marketing")

st.markdown("""
**¿Qué debes hacer?**

En el panel lateral de la página principal, dentro de la sección **"Campaign Manager"**, encontrarás:
""")

# Mostrar ejemplo visual de la configuración
with st.expander("📋 Ver campos de configuración de campaña", expanded=True):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **1️⃣ Target Location**
        - Selecciona la tienda donde aplicar el descuento
        - Ejemplo: "Chicken Shop"
        """)
    
    with col2:
        st.markdown("""
        **2️⃣ Discount Strategy**
        - Usa el slider para elegir el % (0-50%)
        - Ejemplo: 20% de descuento
        """)
    
    with col3:
        st.markdown("""
        **3️⃣ Day of Week**
        - Selecciona qué día aplica
        - Ejemplo: "Miércoles"
        """)
    
    col4, col5 = st.columns(2)
    
    with col4:
        st.markdown("""
        **4️⃣ Start Time**
        - Usa el slider para elegir la hora (0-23)
        - Ejemplo: 12 (mediodía)
        """)
    
    with col5:
        st.markdown("""
        **5️⃣ End Time**
        - Usa el slider para elegir la hora final (0-23)
        - Ejemplo: 14 (2:00 PM)
        """)

st.markdown("""
**Ejemplo de configuración:**
- 📍 **Target Location**: Chicken Shop
- 💰 **Discount Strategy**: 20%
- 📅 **Day**: Miércoles
- ⏰ **Time Window**: 12:00 - 14:00

Esto significa: *"20% de descuento en Chicken Shop los miércoles de 12:00 a 14:00"*
""")

st.markdown("---")

# Paso 3: Aplicar Campaña
st.subheader("✅ Paso 3: Desplegar la Campaña")

st.markdown("""
**¿Qué debes hacer?**

1. 👉 Completa todos los campos anteriores
2. 👉 **Haz clic en el botón "Deploy Campaign"** (botón grande en el panel lateral)
3. ✅ Verás un mensaje de éxito y la campaña aparecerá en "Active Campaigns"
""")

st.success("""
✅ **Campaña desplegada exitosamente**

La campaña ya está activa en el sistema. Se aplicará automáticamente cuando:
- El día de la semana coincida (ej: Miércoles)
- La hora actual esté en el rango configurado (ej: entre 12:00 y 14:00)
""")

st.markdown("---")

# Paso 4: Ejecutar Simulación
st.subheader("▶️ Paso 4: Controlar la Simulación")

st.markdown("""
**¿Qué debes hacer?**

En el **Command Center** del panel lateral encontrarás los controles:

1. 👉 **"Play"**: Inicia/continúa la simulación automáticamente
2. 👉 **"Pause"**: Pausa la simulación
3. 👉 **"Next Hour"**: Avanza 1 hora manualmente
4. 👉 **"Skip to Campaign Day"**: Avanza directo al día de la campaña configurada

**¿Qué esperar?**
- El reloj avanzará automáticamente (si usas Play)
- Los agentes tomarán decisiones usando IA
- Verás eventos aparecer en tiempo real en el panel de eventos
""")

st.markdown("---")

# Paso 5: Qué Observar
st.subheader("👀 Paso 5: ¿Qué Debes Esperar Cuando la Campaña Esté Activa?")

with st.expander("📊 Ejemplo: Campaña de 20% en Chicken Shop (Miércoles 12:00-14:00)", expanded=True):
    st.markdown("""
    **Escenario:**
    - ⏰ **Miércoles, 12:00 PM** (hora de inicio de la campaña)
    - 📍 Campaña activa: "Chicken Shop: 20% descuento"
    
    **Lo que verás en el Event Feed:**
    ```
    ⏰ Miércoles, Día 2, 12:00 | 🎯 Campaña ACTIVA: 20% descuento en Chicken Shop
    ⏰ Miércoles, Día 2, 13:00 | 🛒 David compró chicken en Chicken Shop ($9.60)
    ⏰ Miércoles, Día 2, 13:00 | 🛒 María compró chicken en Chicken Shop ($9.60)
    ```
    
    **Nota importante:** 
    - Precio original: $12.00
    - Con 20% descuento: $9.60 ✅
    - Los agentes **ahorraron $2.40** gracias a la campaña
    
    **Lo que verás en Market Intelligence:**
    - 📈 **Sales Impact**: "Chicken Shop" tendrá un aumento de ventas durante las horas de la campaña
    - 📊 **Loyalty Matrix**: Los agentes que compraron durante la campaña aparecerán con más visitas a "Chicken Shop"
    """)

st.markdown("---")

# Qué Observar en Cada Panel
st.subheader("🔍 Paso 6: Qué Observar en Cada Panel")

tab_info1, tab_info2, tab_info3, tab_info4 = st.tabs([
    "🗺️ Urban Heatmap", 
    "📝 Event Feed", 
    "📊 Market Intelligence",
    "👥 Agent Telemetry"
])

with tab_info1:
    st.markdown("""
    **🗺️ Urban Heatmap**
    
    - **Buildings**: Verás cuadrados de colores:
      - 🟢 Verde = Residential (Residencias)
      - 🟠 Naranja = Commerce (Comercios)
      - 🔵 Azul = Offices (Oficinas)
    - **Agents**: Puntos pequeños de colores representando agentes
    
    **Durante una campaña activa:**
    - Verás agentes moviéndose hacia la ubicación con descuento (naranja)
    - La ubicación con campaña activa se destacará con un círculo brillante
    """)

with tab_info2:
    st.markdown("""
    **📝 Event Feed (Feed de Eventos)**
    
    Aquí verás todos los eventos de la simulación en tiempo real:
    
    - **🛒 Compras**: "David compró chicken en Chicken Shop ($9.60)"
    - **💬 Conversaciones**: "Lisa está hablando con Sophie en la Plaza"
    - **🎯 Campañas**: "Campaña ACTIVA: 20% descuento en Chicken Shop..."
    - **⚠️ Alertas**: "¡Alerta! Inventario de energía crítico para Agent David"
    
    **Durante una campaña activa, espera ver:**
    - Más eventos de compra en la ubicación con descuento
    - Precios con descuento aplicado (ej: $9.60 en lugar de $12.00)
    - Agentes moviéndose hacia esa ubicación
    """)

with tab_info3:
    st.markdown("""
    **📊 Market Intelligence (Inteligencia de Mercado)**
    
    **1. Sales Impact (Impacto en Ventas):**
    - Gráficos de barras mostrando ventas con/sin promoción
    - Comparación de ventas antes/durante/después de la campaña
    - Durante una campaña, verás un **aumento en las ventas** de la ubicación con descuento
    
    **2. Loyalty Matrix (Matriz de Lealtad):**
    - Heatmap mostrando visitas por agente y ubicación
    - Los agentes que respondieron a la campaña mostrarán más visitas a esa ubicación
    - Colores más intensos = más visitas
    
    **3. Social Graph (Grafo Social):**
    - Muestra relaciones entre agentes (conexiones sociales)
    - Si los agentes se encuentran durante la campaña, pueden conversar y mejorar sus relaciones
    """)

with tab_info4:
    st.markdown("""
    **👥 Agent Telemetry (Telemetría de Agentes)**
    
    Aquí puedes ver el estado detallado de cada agente:
    
    - **⚡ Energía**: Barra de progreso (0-100)
    - **💰 Wallet**: Saldo actual (disminuye con compras)
    - **🍔 Grocery Level**: Nivel de comida en casa (0-100)
    - **📍 Location**: Dónde está el agente ahora
    - **🧠 Reasoning**: Razón de sus decisiones (generado por IA)
    
    **Durante una campaña activa:**
    - El dinero de los agentes disminuirá si compran
    - Verás compras en el inventario (ej: {"chicken": 1})
    - La energía puede aumentar si comen lo comprado
    - El reasoning mostrará menciones del descuento
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
       - Revisa Agent Telemetry para ver el dinero disponible
    
    3. **Energía crítica**: 
       - Si un agente está muy cansado (energía baja), puede priorizar descansar sobre comprar
       - Verás alertas en el Event Feed si la energía es crítica
    
    4. **Avanza el tiempo**: 
       - Si configuraste Miércoles pero estás en Lunes, necesitas avanzar ~48 horas
       - Usa "Skip to Campaign Day" para ir directo
    """)

st.markdown("---")

# Resumen de Flujo Completo
st.subheader("📋 Resumen: Flujo Completo")

st.markdown("""
**Pasos completos para usar una campaña:**

1. ✅ **Inicializar** → Ve a la página principal y haz clic en "🔄 Inicializar Simulación"
2. ⚙️ **Configurar** → En Campaign Manager, configura tu campaña
3. 💾 **Desplegar** → Haz clic en "Deploy Campaign"
4. ▶️ **Ejecutar** → Usa "Skip to Campaign Day" o "Next Hour" para avanzar
5. 👀 **Observar** → Ve el Urban Heatmap, Event Feed y Market Intelligence
6. 📈 **Analizar** → Compara ventas antes/durante/después de la campaña

**Ejemplo de cronograma:**
```
Día 0, Lunes 07:00 → Inicializas simulación
Día 0, Lunes 07:00 → Configuras campaña (20% en Chicken Shop, Miércoles 12:00-14:00)
Día 0, Lunes 07:00 → Desplegas campaña
Día 0, Lunes 07:00 → Usas "Skip to Campaign Day" (avanza 53 horas)
Día 2, Miércoles 12:00 → ¡Campaña ACTIVA! Verás mensaje en Event Feed
Día 2, Miércoles 12:00-14:00 → Los agentes compran con descuento
Día 2, Miércoles 14:00 → Campaña termina, pero los efectos continúan
```
""")

st.markdown("---")

# Preguntas Frecuentes
st.subheader("❓ Preguntas Frecuentes")

with st.expander("Ver preguntas frecuentes", expanded=False):
    st.markdown("""
    **Q: ¿Por qué no veo que los agentes compren durante la campaña?**
    
    A: Verifica que:
    - El día de la semana coincida
    - La hora esté en el rango configurado
    - Los agentes tengan suficiente dinero (revisa Agent Telemetry)
    - Los agentes tengan hambre o necesiten comprar
    
    ---
    
    **Q: ¿Cómo sé si la campaña está activa ahora?**
    
    A: En el Command Center verás el estado de la campaña. También verás un mensaje en el Event Feed cuando la campaña se active.
    
    ---
    
    **Q: ¿Puedo tener múltiples campañas activas al mismo tiempo?**
    
    A: Actualmente el sistema soporta una campaña a la vez. Si despliegas una nueva campaña, reemplazará la anterior.
    
    ---
    
    **Q: ¿Los agentes recuerdan las campañas pasadas?**
    
    A: Sí, los agentes tienen memoria. Si una campaña fue exitosa, pueden desarrollar preferencias por esa ubicación y visitarla más frecuentemente incluso después de la campaña.
    """)

st.markdown("---")

# CTA Final
st.success("""
🎉 **¡Listo para comenzar!**

Ahora que entiendes cómo funciona el sistema, puedes:

1. **Volver a la página principal** usando el menú lateral
2. **Inicializar la simulación** desde el Command Center
3. **Configurar tu primera campaña** de marketing
4. **Observar** cómo los agentes responden a tus campañas

**¡Experimenta con diferentes descuentos, horarios y ubicaciones para ver qué funciona mejor!**

💡 **Tip**: Puedes volver a este tutorial en cualquier momento usando el menú lateral.
""")



