from Environment import *
from Agent import *
from Point import Point

# import pygame
# from pygame.locals import *
# from pygame.color import *
import thinkplot
import random
import numpy as np

from datetime import datetime
import pickle
import pandas as pd


"""
def runSimulation(roomHeight=10,
                  roomWidth=8,
                  barrier={ 'radius': .3, 'pos': Point(-1,0)}, # pos is relative to door center
                  doorWidth=1.5,
                  numAgents=50,
                  agentMass=80,
                  desiredSpeed=4,
                  view=False):
"""
def importData():
    with open("experimentData.pk", "rb") as infile:
        results = pickle.load(infile)
    return results

def saveData():
    with open("experimentData.pk", "wb") as outfile:
        pickle.dump(results, outfile)

def logscalelinspace(start, stop, num=20, dtype=np.float):
    logStart = np.log10(start)
    logStop = np.log10(stop)
    return np.logspace(logStart, logStop, num=num, dtype=dtype)

def testDBExists(simulation, df):
    truth = df['roomHeight'] == simulation['roomHeight']

    for x in simulation:
        truth = truth & df[x] == simulation[x]

    return truth.any()


try:
    results = importData()
except FileNotFoundError:
    columns = ["roomHeight", "roomWidth", "barrier", "barrierRadius", "barrierPos", "doorWidth", "numAgents", "agentMass", "desiredSpeed", "escapeTime"]
    results = pd.DataFrame(columns=columns)


settings = {
    "roomHeight":   20,
    "roomWidth":    10,
    "barrier":      {
                        'radius': logscalelinspace(0.5, 5, num=4),
                        'xOffset': np.array([3,4]),
                        'yOffset': logscalelinspace(0.01,1,num=3)
                    },
    "doorWidth":    logscalelinspace(1.5, 5, num=10),
    "numAgents":    logscalelinspace(50, 500, num=10, dtype=np.int),
    "agentMass":    80,
    "desiredSpeed": logscalelinspace(3, 11, num=10)
}


roomHeight = settings['roomHeight']
roomWidth  = settings['roomWidth']
agentMass  = settings['agentMass']

for numAgents in settings['numAgents']:
    for doorWidth in settings['doorWidth']:
        for radius in settings['barrier']['radius']:
            for xOffset in settings['barrier']['xOffset']:
                for yOffset in settings['barrier']['yOffset']:
                    for desiredSpeed in settings['desiredSpeed']:
                        barrier = {
                            'radius':   radius,
                            'pos':      Point(-(xOffset * radius), yOffset*doorWidth)
                            }


                        simulation_data = {
                        "roomHeight":   roomHeight,
                        "roomWidth":    roomWidth,
                        "barrier":      barrier,
                        "doorWidth":    doorWidth,
                        "numAgents":    numAgents,
                        "agentMass":    agentMass,
                        "desiredSpeed": desiredSpeed
                        }
                        print("running", simulation_data)

                        escapeTime = len(runSimulation(
                                          roomHeight=roomHeight,
                                          roomWidth=roomWidth,
                                          barrier=barrier,
                                          doorWidth=doorWidth,
                                          numAgents=numAgents,
                                          agentMass=agentMass,
                                          desiredSpeed=desiredSpeed,
                                          view=False
                                          ))

                        simulation_data["escapeTime"] = escapeTime
                        simulation_data["barrierRadius"] = barrier['radius']
                        simulation_data["barrierPos"] = str(barrier['pos'])

                        results = results.append(simulation_data, ignore_index=True)
                        saveData()

                        print(simulation_data)
