from Cleaning_Model2 import CleaningModel
import matplotlib.pyplot as plt

# Variables iniciales
WIDTH = 30  # Ancho de la cuadrícula
HEIGHT = 30  # Altura de la cuadrícula
PERCENTAGE_DIRTY_CELLS = 50  # Porcentaje de celdas sucias
NUM_AGENTS = [100, 150, 200]  # Diferentes cantidades de agentes a probar
MAX_STEPS = 2000  # Valor de maxsteps (tiempo máximo de simulación)

# Llamar al modelo con diferentes cantidades de agentes
for agent in NUM_AGENTS:
    # Crear una instancia del modelo con los parámetros especificados
    model = CleaningModel(WIDTH, HEIGHT, PERCENTAGE_DIRTY_CELLS, agent, MAX_STEPS)

    # Ejecutar el modelo mientras esté en ejecución
    while model.running:
        model.step()

    # Obtener los datos de celdas sucias a lo largo del tiempo
    dirtyCellsLeft = model.datacollector.get_model_vars_dataframe()

    # Calcular el porcentaje de celdas limpias al final de la simulación
    percentageCleanCells = int((((WIDTH * HEIGHT) - model.dirtyCells) * 100) / (WIDTH * HEIGHT))

    # Obtener los datos de movimientos de los agentes
    agentMoves = model.datacollector.get_agent_vars_dataframe()

    # Calcular los movimientos totales por cada agente al final de la simulación
    allAgentMoves = agentMoves.xs(model.numSteps - 1, level="Step")

    # Gráfica del número de celdas sucias a lo largo del tiempo
    dirtyCellsLeft.plot()
    plt.title("Número de celdas sucias a lo largo del tiempo")
    plt.xlabel("Tiempo (Pasos)")
    plt.ylabel("Número de celdas sucias")
    plt.savefig(f'{agent}_dirty_cells_over_time.png')  # Guardar la gráfica
    plt.close()

    # Gráfica de movimientos totales por agente
    allAgentMoves.plot(kind="bar")
    plt.title("Movimientos totales por agente")
    plt.ylabel("Movimientos (pasos)")
    plt.xlabel("ID del agente")
    plt.savefig(f'{agent}_total_moves_per_agent.png')  # Guardar la gráfica
    plt.close()

    # Imprimir estadísticas finales de la simulación
    print(f"-----Datos iniciales-----")
    print(f"Ocupación de: {WIDTH} * {HEIGHT} espacios")
    print(f"Número de celdas totales: {WIDTH * HEIGHT}")
    print(f"Número de agentes: {agent}")
    print(f"Porcentaje de celdas sucias: {PERCENTAGE_DIRTY_CELLS}%")
    print(f"Tiempo máximo: {MAX_STEPS} pasos")
    print(f"-----Datos finales-----")
    print(f"Tiempo recorrido: {model.numSteps} pasos")
    print(f"Porcentaje de celdas limpias: {percentageCleanCells}%")
