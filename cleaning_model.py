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
        # Si la celda está sucia, límpiala
        if self.model.dirty_cells[self.pos]:
            self.model.dirty_cells[self.pos] = False
        else:
            # Moverse a una celda vecina aleatoria
            possible_steps = self.model.grid.get_neighborhood(
                self.pos, moore=True, include_center=False
            )
            new_position = self.random.choice(possible_steps)
            if self.model.grid.is_cell_empty(new_position):
                self.model.grid.move_agent(self, new_position)
            self.moves += 1  # Incrementa el contador de movimientos

class CleaningModel(mesa.Model):
    """Modelo de la simulación de robots de limpieza en un área MxN."""

    def __init__(self, N, width, height, dirt_percentage, max_time):
        super().__init__()
        self.num_agents = N
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.schedule = mesa.time.RandomActivation(self)
        self.max_time = max_time
        self.current_time = 0

        # Generar las celdas sucias aleatoriamente
        self.dirty_cells = {
            (x, y): (self.random.random() < dirt_percentage)
            for x in range(width)
            for y in range(height)
        }

        # Crear agentes y colocarlos en la posición inicial (1, 1)
        for i in range(self.num_agents):
            agent = CleaningAgent(i, self)
            self.schedule.add(agent)
            self.grid.place_agent(agent, (1, 1))  # Coloca al agente en [1,1]

        # DataCollector para recolectar datos
        self.datacollector = mesa.DataCollector(
            model_reporters={
                "Porcentaje_Celdas_Limpias": lambda model: (
                    sum(not dirty for dirty in model.dirty_cells.values())
                    / len(model.dirty_cells)
                ),
                "Movimientos_Totales": lambda model: sum(
                    agent.moves for agent in model.schedule.agents
                ),
            }
        )

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
        self.current_time += 1
