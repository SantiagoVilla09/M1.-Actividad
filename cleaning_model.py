# cleaning_model.py
import mesa
import numpy as np
import pandas as pd

class CleaningAgent(mesa.Agent):
    """Robot de limpieza reactivo."""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.moves = 0  # Contador de movimientos realizados por el agente

    def step(self):
        # Obtener el contenido de la celda actual
        cell_content = self.model.grid.get_cell_list_contents([self.pos])
        
        # Buscar suciedad en la celda actual
        dirt_objects = [obj for obj in cell_content if isinstance(obj, Dirt)]
        if dirt_objects:
            # Si la celda está sucia, eliminar el objeto de suciedad
            self.model.grid.remove_agent(dirt_objects[0])
        else:
            # Buscar en las celdas vecinas para ver si hay alguna con suciedad
            possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
            dirty_neighbors = [
                cell for cell in possible_steps 
                if any(isinstance(obj, Dirt) for obj in self.model.grid.get_cell_list_contents([cell]))
            ]
            
            if dirty_neighbors:
                # Si hay celdas vecinas sucias, moverse a una de ellas
                new_position = self.random.choice(dirty_neighbors)
            else:
                # Si no hay celdas vecinas sucias, moverse a una celda aleatoria
                new_position = self.random.choice(possible_steps)
            
            # Mover el agente a la nueva posición
            self.model.grid.move_agent(self, new_position)
            self.moves += 1  # Incrementa el contador de movimientos

class Dirt(mesa.Agent):
    """Representación de una unidad de suciedad en la celda."""
    
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

class CleaningModel(mesa.Model):
    """Modelo de la simulación de robots de limpieza en un área MxN."""

    def __init__(self, N, width, height, dirt_percentage, max_time):
        super().__init__()
        self.num_agents = N
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.schedule = mesa.time.RandomActivation(self)
        self.max_time = max_time
        self.current_time = 0

        # Generar las celdas sucias aleatoriamente y crear agentes de suciedad
        for x in range(width):
            for y in range(height):
                if self.random.random() < dirt_percentage:
                    dirt = Dirt(f"dirt-{x}-{y}", self)
                    self.grid.place_agent(dirt, (x, y))

        # Crear agentes y colocarlos en la posición inicial (1, 1)
        for i in range(self.num_agents):
            agent = CleaningAgent(i, self)
            self.schedule.add(agent)
            self.grid.place_agent(agent, (1, 1))  # Coloca al agente en [1,1]

        # DataCollector para recolectar datos
        self.datacollector = mesa.DataCollector(
            model_reporters={
                "Porcentaje_Celdas_Limpias": lambda model: (
                    sum(1 for agent in model.schedule.agents if isinstance(agent, Dirt)) / (width * height)
                ),
                "Movimientos_Totales": lambda model: sum(
                    agent.moves for agent in model.schedule.agents if isinstance(agent, CleaningAgent)
                ),
            }
        )

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
        self.current_time += 1
