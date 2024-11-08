# run.py

from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import NumberInput, Slider
from cleaning_model import CleaningModel, CleaningAgent, Dirt

def agent_and_dirt_portrayal(agent):
    if isinstance(agent, CleaningAgent):
        # Representación de cada agente de limpieza
        return {
            "Shape": "circle",
            "Color": "blue",
            "Filled": "true",
            "Layer": 1,
            "r": 0.5
        }
    elif isinstance(agent, Dirt):
        # Representación de suciedad como círculo marrón
        return {
            "Shape": "circle",
            "Color": "brown",
            "Filled": "true",
            "Layer": 0,
            "r": 0.3
        }

# Configuración de la visualización del grid
width, height = 10, 10
grid = CanvasGrid(agent_and_dirt_portrayal, width, height, 500, 500)

# Crear el servidor para ejecutar la simulación en el navegador
server = ModularServer(
    CleaningModel,
    [grid],
    "Simulación de Robots de Limpieza",
    {
        "N": NumberInput("Número de agentes", value=10),  # Establecido en 10 para asegurarse de tener múltiples agentes
        "width": width,
        "height": height,
        "dirt_percentage": Slider("Porcentaje de celdas sucias", 0.3, 0.1, 1.0, 0.1),
        "max_time": Slider("Tiempo máximo", 100, 10, 1000, 10),
    }
)

# Ejecutar el servidor
server.port = 8521
server.launch()
