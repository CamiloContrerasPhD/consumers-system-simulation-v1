# Multi-Agent Simulation System

AI-powered consumer behavior simulation system implemented with Python and Streamlit. Uses the DeepSeek API for agent decision-making.

## 📋 Features

- 🤖 **Intelligent Agents**: Agents with personality, dynamic needs, and memory
- 🗺️ **Simulated World**: Grid with locations (shops, work, residences) and products
- 💰 **Economic System**: Purchases, dynamic pricing, and marketing campaigns
- 🧠 **LLM-Powered Decision Making**: Uses DeepSeek API for autonomous decisions
- 📊 **Real-Time Visualization**: Interactive map, sales charts, loyalty analysis
- 💬 **Social Interactions**: Conversations between agents that affect relationships

## 🏗️ Architecture

The system is divided into 4 main modules:

### I. Data Modeling Module (`models/`)
- **WorldConfig**: Global world configuration (map, time, marketing)
- **Location**: Locations with inventory, prices, and capacity
- **Agent**: Consumer entities with profile, state, and memory
- **MemoryStream**: Memory system for events and reflections

### II. Simulation Engine Module (`engine/`)
- **TimeManager**: Temporal orchestrator and energy decay
- **InteractionEngine**: World physics and proximity detection
- **TransactionSystem**: Purchase and economy management

### III. Cognition Module (`cognition/`)
- **LLMClient**: Client for the DeepSeek API
- **PromptBuilder**: Contextualized prompt constructor
- **DecisionMaker**: Decision manager (Planner, Reactor, Conversationalist)
- **ResponseParser**: LLM decision translator to executable actions

### IV. Visualization Module (`app.py`)
- Streamlit interface with interactive map
- Real-time event feed
- Analysis dashboard (sales, loyalty, social relationships)
- Control panel and configuration

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- DeepSeek API Key (get one at [deepseek.com](https://www.deepseek.com))

### Installation Steps

1. **Clone the repository**:
```bash
git clone <repository-url>
cd "Consumers System"
```

2. **Create virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**:
```bash
# Windows (PowerShell)
$env:DEEPSEEK_API_KEY="your_api_key_here"

# Linux/Mac
export DEEPSEEK_API_KEY="your_api_key_here"

# Or create a .env file with:
# DEEPSEEK_API_KEY=your_api_key_here
```

5. **Run the application**:
```bash
streamlit run app.py
```

The application will open at `http://localhost:8501`

## 📖 Usage

### Basic Initialization

1. Click **"Initialize Simulation"** in the sidebar
2. The system will create default agents and locations
3. Use **"Execute Next Hour"** to advance the simulation
4. Observe agent behavior in real-time

### Load Custom Configuration

You can load a JSON file with your own configuration:

```json
{
  "world": {
    "width": 10,
    "height": 10
  },
  "locations": [
    {
      "name": "Coffee Shop",
      "x": 3,
      "y": 3,
      "type": "Restaurant",
      "capacity": 10,
      "products": [
        {
          "name": "coffee",
          "price": 5.0,
          "stock": 100,
          "satisfies_need": "energy"
        }
      ]
    }
  ],
  "agents": [
    {
      "id": "agent_1",
      "name": "María",
      "age": 28,
      "profession": "Engineer",
      "traits": ["extrovert", "health_conscious"],
      "money": 500.0,
      "energy": 100.0,
      "home": "home",
      "work": "office"
    }
  ],
  "marketing": [
    {
      "location_name": "Coffee Shop",
      "discount_percent": 20,
      "day_of_week": 2,
      "start_hour": 12,
      "end_hour": 14
    }
  ]
}
```

See `config_example.json` for a complete example.

### Configure Marketing Campaigns

1. In the sidebar, select the location
2. Define the discount percentage
3. Select the day of the week and time range
4. Click **"Deploy Campaign"**

## 🔄 Simulation Flow

Each simulation tick (hour) executes:

1. **Time Advancement**: Clock advances and energy decay is applied
2. **Daily Planning**: At 7 AM, agents plan their day using the LLM
3. **Decision Making**: Each agent decides their action using the LLM (parallel)
4. **Action Execution**: Movements, purchases, rest, etc. are executed
5. **Social Interactions**: Agents in the same location can converse
6. **UI Update**: Charts and maps are updated

## 📊 Visualizations

### World Map
- **Locations**: Blue squares with names
- **Agents**: Circles colored by energy level (red=low, green=high)
- **Coordinates**: 10x10 grid system by default

### Analysis Dashboard
- **Sales Chart**: Total revenue by location
- **Loyalty Matrix**: Heatmap of visits by agent and location
- **Social Graph**: Visualization of relationships between agents

### Event Feed
- Real-time log of all actions
- Conversations between agents
- System events

## 🔧 Advanced Configuration

### Customize Agents

Agents have the following configurable attributes:
- **Personality**: `extrovert`, `introvert`, `health_conscious`, `impulsive`, `thrifty`, etc.
- **Needs**: Energy (0-100), Money, Grocery level (0-100)
- **Relationships**: Affinity with other agents (-1.0 to 1.0)

### Customize Locations

Locations can be:
- **Residence**: Residence
- **Work**: Workplace
- **Restaurant**: Restaurant
- **Shop**: Shop
- **Grocery**: Grocery store

Each location can have multiple products with prices and stock.

## 🐛 Troubleshooting

### Error: "DEEPSEEK_API_KEY not configured"
- Make sure you've configured the environment variable correctly
- Verify that the API key is valid

### Agents are not making decisions
- Check your internet connection
- Review console logs for API errors
- Make sure you have credits in your DeepSeek account

### Simulation is slow
- Reduce the number of agents
- Adjust `max_workers` in `DecisionMaker` if you have many agents
- Consider using a faster model

## 📝 Technical Notes

- **Parallel Execution**: Agent decisions are processed in parallel using `ThreadPoolExecutor`
- **Error Handling**: The system has robust error handling for LLM failures
- **Action Validation**: All actions are validated before execution
- **Persistent Memory**: Events are stored in `MemoryStream` for LLM context

## 🤝 Contributing

Contributions are welcome. Please:
1. Fork the project
2. Create a branch for your feature
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

Based on multi-agent simulation research (mention specific paper if known).

## 📧 Contact

For questions or suggestions, please open an issue in the repository.
