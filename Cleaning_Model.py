from mesa import Agent, Model, DataCollector
from mesa.space import MultiGrid
from mesa.time import StagedActivation

# Retornar el número de celdas sucias
def getDirtyCells(model):
    """
    Objetivo: Retorna la cantidad de celdas sucias en la cuadrícula
    Parámetros: model ----- Modelo del sistema multiagente
    Valor de retorno: dirtyCells ----- Cantidad de celdas que quedan sucias actualmente
    """
    return model.dirtyCells

# Agente de limpieza (Aspiradora)
class CleaningAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.nextState = None
        self.moves = 0

    # Si la celda está sucia, límpiala (elimínala del diccionario)
    def isCellDirty(self, agentPosition):
        if agentPosition in self.model.dirtyCellsDic:
            del self.model.dirtyCellsDic[agentPosition]
            self.model.dirtyCells -= 1
            return True
        return False

    # Mover el agente si la celda elegida está disponible
    def moveAgent(self, possibleStep):
        self.nextState = possibleStep
        self.model.grid.move_agent(self, self.nextState)
        self.moves += 1

    # No mover el agente si la celda elegida está ocupada
    def notMoveAgent(self):
        self.nextState = self.pos

    def step(self):
        canMove = False
        # Si la celda actual no está sucia, verifica para moverse
        if not self.isCellDirty(self.pos):
            possibleSteps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
            possibleStep = self.random.choice(possibleSteps)
            if not self.model.grid.out_of_bounds(possibleStep):
                cellContent = self.model.grid.get_cell_list_contents(possibleStep)
                # Si no hay otro agente en la celda de destino, se puede mover
                if not cellContent:
                    canMove = True
        if canMove:
            self.moveAgent(possibleStep)
        else:
            self.notMoveAgent()

    def advance(self):
        # Mueve el agente a su siguiente posición
        self.model.grid.move_agent(self, self.nextState)

class Dirt(Agent):
    """Representación de una unidad de suciedad en la celda."""
    
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

class CleaningModel(Model):
    def __init__(self, width, height, dirtpercentage, numAgents, maxsteps):
        self.grid = MultiGrid(width, height, False)
        self.dirtyCells = int(((width * height) * dirtpercentage) / 100)
        self.dirtyCellsDic = {}
        self.numSteps = 0
        self.maxsteps = maxsteps  # Tiempo máximo de simulación
        self.schedule = StagedActivation(self)
        self.running = True

        # Crear celdas sucias
        count = 0
        while count < self.dirtyCells:
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            if (x, y) not in self.dirtyCellsDic:
                self.dirtyCellsDic[(x, y)] = True
                count += 1

        # Crear agentes de limpieza
        for uniqueId in range(numAgents):
            agt = CleaningAgent(uniqueId, self)
            self.schedule.add(agt)
            self.grid.place_agent(agt, (1, 1))

        self.datacollector = DataCollector(
            model_reporters={"Dirty cells": getDirtyCells},
            agent_reporters={"Moves": "moves"}
        )

    def step(self):
        # Avanza la simulación por un paso y detiene si se cumplen las condiciones
        if self.dirtyCells > 0 and self.numSteps < self.maxsteps:
            self.numSteps += 1
            self.datacollector.collect(self)
            self.schedule.step()
        else:
            self.running = False

