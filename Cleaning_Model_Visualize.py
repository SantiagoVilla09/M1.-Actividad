from Cleaning_Model2 import CleaningModel
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import Slider, NumberInput

def agentPortrayal(agent):
    """
    Definir la apariencia de los agentes en la visualización.
    """
    portrayal = {
        "Shape": "circle",  # Forma del agente (círculo)
        "Filled": "true",   # Relleno activado
        "Layer": 0,         # Capa de visualización
        "Color": "blue",    # Color del agente
        "r": 0.6            # Radio del círculo
    }
    return portrayal

# Dimensiones iniciales de la cuadrícula
WIDTH = 12
HEIGHT = 12

# Configuración de la cuadrícula para visualización
grid = CanvasGrid(agentPortrayal, WIDTH, HEIGHT, 650, 650)

# Configuración del servidor con controles interactivos
server = ModularServer(
    CleaningModel,
    [grid],
    "Modelo de Limpieza con Agentes",
    {
        "width": WIDTH,  # Ancho de la cuadrícula
        "height": HEIGHT,  # Altura de la cuadrícula
        "dirtpercentage": Slider("Porcentaje de Celdas Sucias", 10, 0, 100, 5),
        # Slider para ajustar el porcentaje de celdas sucias
        "numAgents": NumberInput("Número de Agentes", value=10),
        # Input para especificar el número de agentes
        "maxsteps": NumberInput("Máximo de Pasos de Simulación", value=100)
        # Input para definir el número máximo de pasos
    }
)
server.port = 8521  # Puerto predeterminado del servidor
server.launch()
