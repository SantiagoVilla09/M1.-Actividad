# run.py

from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import NumberInput, Slider
from cleaning_model import CleaningModel, CleaningAgent

def agent_and_cell_portrayal(agent):
    if isinstance(agent, CleaningAgent):
        # Representación de cada agente de limpieza
        return {
            "Shape": "circle",
            "Color": "blue",
            "Filled": "true",
            "Layer": 1,
            "r": 0.5
        }

def dirty_cell_portrayal(model):
    # Representación de las celdas sucias
    portrayal = {}
    for (x, y), is_dirty in model.dirty_cells.items():
        if is_dirty:
            portrayal[(x, y)] = {
                "Shape": "rect",
                "Color": "brown",
                "Filled": "true",
                "Layer": 3,
                "w": 1,
                "h": 1
            }
    return portrayal

# Configuración de la visualización del grid
width, height = 10, 10
grid = CanvasGrid(agent_and_cell_portrayal, width, height, 500, 500)

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

